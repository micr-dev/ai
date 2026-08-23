---
name: file-upload
description: Upload a file and return a stable public URL. Use when the user asks to upload a file or when a file is needed for a PR description.
metadata:
  harness: [claude, codex]
  platform: [darwin, linux]
  scope: fleet
---

# File upload

Use a permanent or account-backed storage provider. Do not use temporary hosts such as `files.tslop.org`, Catbox, Litterbox, transfer.sh, 0x0.st, or file.io for files that must remain available.

## Preferred hosted backend: Uploadcare

Use Uploadcare when the user wants a private upload project with public URLs for images or videos. The project and upload credentials remain private, while each uploaded object is delivered through an unguessable Uploadcare CDN URL.

Uploadcare's current Free plan lists:

- 1 GB of storage
- 5 GB of CDN traffic per month
- 1,000 operations per month
- 500 MB maximum file size

The free plan is suitable for occasional PR screenshots and short videos. Storage is account-backed and has no per-file expiry, but it is not an absolute permanence guarantee: the account and project must remain active, and the quota must not be exceeded.

For files below Uploadcare's direct-upload limit, use the Upload API. The public key is sufficient for the upload; never put the secret key in the upload command:

```bash
response=$(curl --fail-with-body -sS \
  -F "UPLOADCARE_PUB_KEY=${UPLOADCARE_PUBLIC_KEY}" \
  -F "file=@${file_path}" \
  https://upload.uploadcare.com/base/)

file_uuid=$(printf '%s' "$response" | tr -d '[:space:]')
file_url="https://ucarecdn.com/${file_uuid}/$(basename "$file_path")"
```

Direct uploads support files smaller than 100 MB. Use Uploadcare's multipart upload flow or an official client for larger files. Keep the secret key out of repositories and chat. Use signed uploads when the upload endpoint must not accept arbitrary anonymous uploads.

The public delivery URL has the form:

```text
https://ucarecdn.com/<file-uuid>/<filename>
```

Use the URL returned by Uploadcare as the source of truth. Verify it with a bounded `HEAD` or `GET` request before reporting success. Do not upload secrets, private data, or files that should not become public.

If the user needs the media itself to remain private, use Uploadcare signed delivery URLs instead of public CDN URLs. A public URL is intentionally retrievable by anyone who has it.

## Other hosted alternatives

Cloudinary also supports private projects, image and video delivery, transformations, and public or signed URLs. Its free plan uses a combined credit allowance, so it is less predictable for video-heavy use than Uploadcare. Choose it when media transformations matter more than simple file hosting.

Do not recommend Pixeldrain as permanent storage. Its retention rules can delete inactive files, and those rules have changed over time.

## Cloudflare R2 backend

Use Cloudflare R2 when the user wants a simple, durable object store and is willing to manage a Cloudflare account. Keep the bucket private for uploads, then expose only the object URLs that should be public through a custom domain or a controlled public bucket. Use presigned URLs for temporary private access.

The current R2 free tier lists:

- 10 GB-month of Standard storage per month
- 1 million Class A operations per month
- 10 million Class B operations per month
- No egress charge

The free tier does not apply to Infrequent Access storage. Usage beyond the free tier is billed, so configure billing alerts and do not treat R2 as unconditionally free.

R2 is S3-compatible and works with `aws s3`, `rclone`, `mc`, or an application using the S3 API. It is managed storage, not self-hosted.

## Self-hosted backend: MinIO

Use MinIO on an Oracle Always Free VM or another machine the user controls when avoiding any hosted provider is more important than operational simplicity. Put it behind HTTPS using a reverse proxy or Cloudflare Tunnel, configure public read access only for intended objects, and back up the data before treating it as durable.

## Upload rules

- Confirm the target backend and credentials before uploading. Never guess credentials.
- Use only the file basename in the public object key unless the configured backend requires a prefix.
- Preserve the file extension.
- Treat the provider's response or verified release metadata as the source of truth for the URL.
- Verify the returned URL with a `HEAD` or bounded `GET` request before reporting success.
- On authentication failure, report that the credential is missing or invalid. Do not retry blindly.
- Do not claim a file is permanent in an absolute sense. Say that it has no configured expiry and is retained by the provider while the account, release, or self-hosted service remains available.

## Use the URL in GitHub

- Embed images (`png`, `jpg`, `gif`, `webp`) as `![description](URL)`.
- Link videos (`mp4`, `mov`, `webm`) as `[screen recording](URL)` because GitHub does not inline-play externally hosted video.
- When an inline preview genuinely helps and the clip is shorter than about 30 seconds, also upload a GIF preview:

```bash
ffmpeg -i recording.mp4 -vf "fps=10,scale=800:-1" -loop 0 preview.gif
```

Embed the GIF and link the full-quality video below it.
