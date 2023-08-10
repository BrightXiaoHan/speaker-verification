import base64
import tempfile
from typing import List, Union

import fastapi
import torch
from deeplake.core.vectorstore.deeplake_vectorstore import VectorStore

from pyannote.audio import Audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding

model = PretrainedSpeakerEmbedding("speechbrain/spkrec-ecapa-voxceleb", device=torch.device("cpu"))

VECTOR_STORE_PATH = "vector_store"

app = fastapi.FastAPI()
vector_store = VectorStore(
    path=VECTOR_STORE_PATH,
)


def embedding_function(audio_file: str, sample_rate: int = 16000):
    audio = Audio(sample_rate=16000, mono=True)
    waveform, _ = audio({"audio": audio_file, "sample_rate": sample_rate})
    embedding = model(waveform[None])
    return embedding


@app.post("/voiceprint/reasoning")
def search(data: str = fastapi.Body(..., embed=True), sample_rate: int = fastapi.Body(..., embed=True)):
    # decode base64 from data
    data = base64.b64decode(data)
    # save data to temp wav file
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav_file:
        temp_wav_file.write(data)
        embedding = embedding_function(temp_wav_file.name, sample_rate)
        # search
        search_results = vector_store.search(embedding, k=5)
        # return results
        return {"code": 200, "msg": "", "data": [{"id": "1", "name": "张三", "score": "0.97"}]}


@app.post("/voiceprint/delete")
def delete(id: Union[str, List[str]] = fastapi.Body(..., embed=True)):
    if isinstance(id, str):
        id = [id]
    vector_store.delete(id)
    return {
        "code": 200,
        "msg": "success",
    }


@app.post("/voiceprint/update")
def update(
    id: str = fastapi.Body(..., embed=True),
    name: str = fastapi.Body(..., embed=True),
    sample_rate: int = fastapi.Body(..., embed=True),
    data: str = fastapi.Body(..., embed=True),
):
    # decode base64 from data
    data = base64.b64decode(data)
    # save data to temp wav file
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_wav_file:
        temp_wav_file.write(data)
        embedding = embedding_function(temp_wav_file.name, sample_rate)
        # update
        vector_store.add(
            [name],
            embedding=[embedding],
            metadata=[
                {
                    "id": id,
                    "name": name,
                    "sample_rate": sample_rate,
                }
            ],
        )

    return {
        "code": 200,
        "msg": "success",
    }
