import shutil
import tempfile
from io import TextIOWrapper

import librosa
import requests
import soundfile as sf
import torch
import uvicorn
from fastapi import FastAPI
from scipy.spatial.distance import cdist

from pyannote.audio import Audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.core import Segment

model = PretrainedSpeakerEmbedding("speechbrain/spkrec-ecapa-voxceleb", device=torch.device("cpu"))


app = FastAPI()


def download_file(url, dest: TextIOWrapper):
    local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        shutil.copyfileobj(r.raw, dest)

    return local_filename


def resample(wav_file: str, dest_file: TextIOWrapper, sample_rate: int):
    """
    resample wave file
    """
    y, s = librosa.load(wav_file, sr=sample_rate)  # Downsample 44.1kHz to 8kHz
    y_16 = librosa.resample(y, orig_sr=s, target_sr=16000)  # 采样率转化
    sf.write(dest_file, y_16, 16000)


def get_embedding(audio_file, crop_time=5.0, sample_rate=16000):
    audio = Audio(sample_rate=sample_rate, mono=True)
    try:
        speaker = Segment(0.0, crop_time)
        waveform, _ = audio.crop(audio_file, speaker)
    except Exception:
        waveform, _ = audio({"audio": audio_file, "sample_rate": sample_rate})

    embedding = model(waveform[None])
    return embedding


def varify_crop(audio_file_1, audio_file_2, sample_rate=16000, crop_time=10.0):
    embedding_1 = get_embedding(audio_file_1, crop_time, sample_rate)
    embedding_2 = get_embedding(audio_file_2, crop_time, sample_rate)

    distance = cdist(embedding_1, embedding_2, metric="cosine")
    return distance[0][0]


@app.post("/yuyispeech/vector/score")
def score(enroll_audio_url, test_audio_url, sample_rate: int = 16000):
    max_score = 0
    enroll_audio_urls = enroll_audio_url.split("|")
    for enroll_audio_url in enroll_audio_urls:
        enroll_audio_file = tempfile.NamedTemporaryFile(suffix=".wav")
        download_file(enroll_audio_url, enroll_audio_file)
        test_audio_file = tempfile.NamedTemporaryFile(suffix=".wav")
        download_file(test_audio_url, test_audio_file)
        score = 1 - varify_crop(test_audio_file.name, enroll_audio_file.name, sample_rate)
        max_score = max(max_score, score)
        enroll_audio_file.close()
        test_audio_file.close()

    print(enroll_audio_urls, test_audio_url, max_score)
    return {
        "success": True,
        "code": 200,
        "message": {"description": "success"},
        "result": {"score": max_score},
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
