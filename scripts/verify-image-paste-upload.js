const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const { readFileSync } = require("node:fs");
const { resolve } = require("node:path");

const root = resolve(__dirname, "..");
const helperSource = readFileSync(resolve(root, "apps/web/src/imagePaste.ts"), "utf8");

assert.match(helperSource, /new URL\(path, origin\)\.toString\(\)/, "relative upload paths must become absolute URLs");
assert.match(helperSource, /pasted image/, "image markdown must have fallback alt text");
assert.match(helperSource, /!\[\$\{.*alt/, "markdown helper must include alt text");
assert.match(helperSource, /selectionStart|slice\(0, start\)/, "markdown insertion must use the textarea selection");

const python = String.raw`
import io
import os
import sys
import tempfile
from pathlib import Path

root = Path(r"${root}")
os.environ["FENGVOICE_DB_PATH"] = str(Path(tempfile.gettempdir()) / "fengvoice-image-paste-test.db")
sys.path.insert(0, str(root / "services" / "api"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

text_response = client.post(
    "/api/uploads/images",
    files={"file": ("note.txt", io.BytesIO(b"not an image"), "text/plain")},
)
assert text_response.status_code == 400, text_response.text

png_response = client.post(
    "/api/uploads/images",
    files={"file": ("paste.png", io.BytesIO(b"\x89PNG\r\n\x1a\n"), "image/png")},
)
assert png_response.status_code == 200, png_response.text
payload = png_response.json()
assert payload["url"].startswith("http://testserver/uploads/notes/"), payload
assert payload["alt"] == "pasted image", payload
`;

const result = spawnSync("python", ["-c", python], {
  cwd: root,
  encoding: "utf8",
});

if (result.status !== 0) {
  process.stdout.write(result.stdout);
  process.stderr.write(result.stderr);
  process.exit(result.status ?? 1);
}

console.log("image paste upload verification passed");
