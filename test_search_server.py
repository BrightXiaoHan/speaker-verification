import base64
import glob

from fastapi.testclient import TestClient

from search_server import app

client = TestClient(app)
assets_folder = "assets"


def test_search():
    for i, wav_file in enumerate(glob.glob(f"{assets_folder}/*.wav")):
        # base64 encode wav file
        with open(wav_file, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        # send request
        response = client.post(
            "/voiceprint/update", json={"id": f"test_id_{i}", "name": f"test_name_{i}", "data": data, "sampling_rate": 16000}
        )
        assert response.status_code == 200

    for i, wav_file in enumerate(glob.glob(f"{assets_folder}/*.wav")):
        with open(wav_file, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        response = client.post(
            "/voiceprint/reasoning",
            json={
                "data": data,
                "sampling_rate": 16000,
            },
        )
        assert response.status_code == 200
        result = response.json()
        assert result["data"][0]["id"] == f"test_id_{i}"

    for i, wav_file in enumerate(glob.glob(f"{assets_folder}/*.wav")):
        response = client.post(
            "/voiceprint/delete",
            json={
                "id": f"test_id_{i}",
            },
        )
        assert response.status_code == 200
        result = response.json()
        assert result["msg"] == "success"

        with open(wav_file, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        response = client.post(
            "/voiceprint/reasoning",
            json={
                "data": data,
                "sampling_rate": 16000,
            },
        )
        assert response.status_code == 200
        result = response.json()
        assert len(result["data"]) == 0 or result["data"][0]["id"] != f"test_id_{i}"


if __name__ == "__main__":
    test_search()
