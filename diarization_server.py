import shutil
import tempfile
from io import TextIOWrapper

import requests
import uvicorn
from fastapi import FastAPI

from diarization import varify

app = FastAPI()


def download_file(url, dest: TextIOWrapper):

    local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        shutil.copyfileobj(r.raw, dest)

    return local_filename


@app.post("/yuyispeech/vector/score")
def score(enroll_audio_url, test_audio_url, sample_rate: int = 16000):
    enroll_audio_file = tempfile.NamedTemporaryFile(suffix=".wav")
    download_file(enroll_audio_url, enroll_audio_file)
    test_audio_file = tempfile.NamedTemporaryFile(suffix=".wav")
    download_file(test_audio_url, test_audio_file)

    same = varify(test_audio_file.name, enroll_audio_file.name)

    enroll_audio_file.close()
    test_audio_file.close()
    return {
        "success": True,
        "code": 200,
        "message": {"description": "success"},
        "result": {"score": 1 if same else 0},
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
