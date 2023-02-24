import os

import pandas
import requests
import torch
from scipy.spatial.distance import cdist

from pyannote.audio import Audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.core import Segment

model = PretrainedSpeakerEmbedding("speechbrain/spkrec-ecapa-voxceleb", device=torch.device("cpu"))

audio = Audio(sample_rate=16000, mono=True)


def varify(audio_url_1, audio_url_2):
    audio_file_1 = audio_url_1.split("/")[-1]
    audio_file_2 = audio_url_2.split("/")[-1]
    if not os.path.exists(audio_file_1):
        response = requests.get(audio_url_1, allow_redirects=True)
        open(audio_file_1, "wb").write(response.content)

    if not os.path.exists(audio_file_2):
        response = requests.get(audio_url_2, allow_redirects=True)
        open(audio_file_2, "wb").write(response.content)

    speaker_1 = Segment(0.0, 3.0)
    waveform1, _ = audio.crop(audio_file_1, speaker_1)
    embedding_1 = model(waveform1[None])

    speaker_2 = Segment(0.0, 3.0)
    waveform_2, _ = audio.crop(audio_file_2, speaker_2)
    embedding_2 = model(waveform_2[None])

    distance = cdist(embedding_1, embedding_2, metric="cosine")
    return distance[0][0]


def main():
    data = pandas.read_excel("data.xlsx")
    for _, row in data.iterrows():
        audio_url_1 = row.iloc[1]
        audio_url_2 = row.iloc[2]
        name = row.iloc[0]
        distance = varify(audio_url_1, audio_url_2)
        print(f"File1: {audio_url_1} File2: {audio_url_2} Name: {name} Distance: {distance}")

    audio_url_1 = data.iloc[0, 1]
    audio_url_2 = data.iloc[1, 2]
    name_1 = data.iloc[0, 0]
    name_2 = data.iloc[1, 0]
    distance = varify(audio_url_1, audio_url_2)
    print("distance between {} and {} is {}".format(name_1, name_2, distance))


if __name__ == "__main__":
    main()
