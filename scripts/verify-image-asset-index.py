import io, os, sys, tempfile, json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
os.environ["FENGVOICE_DB_PATH"] = str(Path(tempfile.gettempdir()) / "fengvoice-phase2b-test.db")
sys.path.insert(0, str(root / "services" / "api"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

resp = client.post("/api/uploads/images", files={"file": ("paste.png", io.BytesIO(b"\x89PNG\r\n\x1a\n"), "image/png")})
assert resp.status_code == 200, resp.text
payload = resp.json()
assert "image_id" in payload, f"Response must include image_id: {payload}"
assert payload["image_id"].startswith("img_"), f"image_id prefix wrong: {payload}"
assert payload["url"].startswith("http://testserver/uploads/notes/"), payload

idx = root / "runtime" / "asset-index" / "note-images.jsonl"
assert idx.exists(), f"Index file missing: {idx}"
lines = idx.read_text(encoding="utf-8").strip().split("\n")
assert len(lines) > 0, "Index file empty"
last = json.loads(lines[-1])
assert last["image_id"] == payload["image_id"], f"image_id mismatch: {last['image_id']} != {payload['image_id']}"
assert last["source"] == "note_paste", f"source mismatch: {last['source']}"
assert len(last["sha256"]) == 64, f"sha256 length wrong: {len(last['sha256'])}"
assert last["mime_type"] == "image/png", f"mime_type mismatch: {last['mime_type']}"
assert last["size_bytes"] > 0, f"size_bytes not positive: {last['size_bytes']}"
assert last["image_id"].startswith("img_"), f"stored image_id prefix wrong: {last['image_id']}"

print("image asset index verification passed")
