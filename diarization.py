import os
import tempfile
from itertools import permutations

import librosa
import numpy as np
import pandas
import requests
import soundfile as sf

from pyannote.audio import Pipeline

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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",
)


def join_wav_file(infiles, outfile):
    """Remove silence and join wav files"""
    audio1, _ = librosa.load(infiles[0], sr=8000, mono=True)
    audio2, _ = librosa.load(infiles[1], sr=8000, mono=True)
    clip_1 = librosa.effects.trim(audio1, top_db=30)[0]
    clip_2 = librosa.effects.trim(audio2, top_db=30)[0]
    clip = np.append(clip_1, clip_2)
    sf.write(outfile, clip, 8000)


def diarization(wav_file):
    diarization = pipeline(wav_file)

    # 5. print the result
    all_speakers = {}
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        duration = turn.end - turn.start
        if duration < 0.5:
            continue
        if speaker in all_speakers:
            all_speakers[speaker] += duration
        else:
            all_speakers[speaker] = duration

    max_duration = max(all_speakers.values())
    total_duration = sum(all_speakers.values())

    return max_duration, total_duration


def varify(audio_file_1, audio_file_2):
    joint_wav = tempfile.NamedTemporaryFile(suffix=".wav")

    max_duration = 0
    total_duration = 0
    join_wav_file([audio_file_1, audio_file_2], joint_wav.name)
    md, td = diarization(joint_wav.name)
    max_duration += md
    total_duration += td
    rate1 = md / td

    join_wav_file([audio_file_2, audio_file_1], joint_wav.name)
    md, td = diarization(joint_wav.name)
    max_duration += md
    total_duration += td
    rate2 = md / td

    print(f"rate1: {rate1}, rate2: {rate2}")
    joint_wav.close()

    return rate1 >= 0.9 or rate2 > 0.9


def download(url):
    audio_file = url.split("/")[-1]
    if not os.path.exists(audio_file):
        response = requests.get(url, allow_redirects=True)
        open(audio_file, "wb").write(response.content)

    return audio_file


def main():
    data = pandas.read_excel("data.xlsx")
    for i, row in data.iterrows():
        audio_url_1 = row.iloc[1]
        audio_url_2 = row.iloc[2]
        name = row.iloc[0]
        audio_file_1 = download(audio_url_1)
        audio_file_2 = download(audio_url_2)

        same = varify(audio_file_1, audio_file_2)
        print(f"The speaker of {name} is the same: {same}")

    for i, j in permutations(range(data.shape[0]), 2):
        audio_url_1 = data.iloc[i, 1]
        audio_url_2 = data.iloc[j, 2]
        name_1 = data.iloc[i, 0]
        name_2 = data.iloc[j, 0]
        audio_file_1 = download(audio_url_1)
        audio_file_2 = download(audio_url_2)
        same = varify(audio_file_1, audio_file_2)
        print(f"The speakers of {name_1} and {name_2} are the same: {same}")

    audio_url_1 = "http://39.105.167.2:9529/uploads/asrdir/2023/02/23/18702513859_a576340e-b478-4d5b-9fad-55ac0d027983_0.wav"
    audio_url_2 = "http://39.105.167.2:9529/uploads/asrdir/2023/02/23/18702513859_9c0c3dba-29b1-4ba7-baf4-92a834d6f71a_0.wav"
    audio_url_3 = "http://39.105.167.2:9529/uploads/asrdir/2023/02/23/18702513859_4f8d9b38-1315-482c-a029-3148baf0e6b5_0.wav"
    audio_file_1 = download(audio_url_1)
    audio_file_2 = download(audio_url_2)
    audio_file_3 = download(audio_url_3)

    same = varify(audio_file_1, audio_file_2)
    print(f"The speakers of the first two are the same: {same}")

    same = varify(audio_file_2, audio_file_3)
    print(f"The speakers of the second two are the same: {same}")


if __name__ == "__main__":
    main()
