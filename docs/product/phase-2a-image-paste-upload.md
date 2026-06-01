# Phase 2A Image Paste Upload

Phase 2A adds image paste upload support to the notes editor.

## Behavior

- Pasting normal text into the note textarea keeps the browser default behavior.
- Pasting an image uploads the first image file from the clipboard.
- Successful uploads insert Markdown at the current cursor position:

```markdown
![pasted image](http://localhost:8000/uploads/notes/example.png)
```

- Returned relative upload paths are converted to absolute URLs in the web app before insertion.
- Successful uploads show `图片上传成功`.
- Failed uploads show `图片上传失败，请重试` and keep the current note content unchanged.

## API

`POST /api/uploads/images`

- Form field: `file`
- Accepts only `image/*`
- Limit: 5 MB
- Stores files under `public/uploads/notes/`
- Returns:

```json
{
  "url": "http://localhost:8000/uploads/notes/example.png",
  "alt": "pasted image"
}
```

## Verification

```powershell
cd apps/web
npm run build
npm test
```

`npm test` runs `scripts/verify-image-paste-upload.js`, which checks the upload API and front-end Markdown URL/alt insertion helpers.
