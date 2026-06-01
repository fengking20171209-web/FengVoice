const assert = require("node:assert/strict");
const { spawnSync } = require("node:child_process");
const { existsSync, readFileSync } = require("node:fs");
const { resolve } = require("node:path");

const root = resolve(__dirname, "..");

// 1. Check asset_index.py exists
const assetIndexPath = resolve(root, "services/api/asset_index.py");
assert.ok(existsSync(assetIndexPath), "asset_index.py must exist");
const source = readFileSync(assetIndexPath, "utf8");
assert.match(source, /create_note_image_record/, "asset_index.py must export create_note_image_record");
assert.match(source, /sha256/, "asset_index.py must compute sha256");
assert.match(source, /image_id/, "asset_index.py must generate image_id");
assert.match(source, /jsonl/, "asset_index.py must write JSONL");

// 2. Check main.py returns image_id
const mainSource = readFileSync(resolve(root, "services/api/main.py"), "utf8");
assert.match(mainSource, /image_id/, "main.py must return image_id in upload response");

// 3. Check UploadedImage type
const apiSource = readFileSync(resolve(root, "apps/web/src/api.ts"), "utf8");
assert.match(apiSource, /image_id:\s*string/, "UploadedImage type must include image_id");

// 4. Check .gitignore
const gitignore = readFileSync(resolve(root, ".gitignore"), "utf8");
assert.match(gitignore, /runtime\//, ".gitignore must ignore runtime/");

// 5. Run Python backend test
const pyResult = spawnSync("python", [resolve(root, "scripts/verify-image-asset-index.py")], {
  cwd: root,
  encoding: "utf8",
  timeout: 30000,
});
if (pyResult.status !== 0) {
  process.stdout.write(pyResult.stdout);
  process.stderr.write(pyResult.stderr);
  process.exit(pyResult.status ?? 1);
}

console.log("image asset index verification passed");
