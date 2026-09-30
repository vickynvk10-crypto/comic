from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/")
assert response.status_code == 200, response.text
print("ComicCraft smoke test passed.")
