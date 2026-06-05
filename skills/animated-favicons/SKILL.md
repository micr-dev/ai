---
name: animated-favicons
description: Build and review animated browser favicons using canvas, PNG data URLs, tab badges, progress indicators, and optional Web Worker rendering. Use when implementing animated favicons, notification dots, loading/progress favicons, tab attention indicators, or favicon updates from canvas.
---

# Animated Favicons

## Quick Start

Use animated favicons only for real state: uploads, exports, builds, unread notifications, live monitoring, or a short branded moment. Prefer a static favicon or static badge when the state does not need motion.

```js
let favicon = document.querySelector('link[rel~="icon"]');
if (!favicon) {
  favicon = document.createElement('link');
  favicon.rel = 'icon';
  document.head.appendChild(favicon);
}

const originalHref = favicon.href;
const canvas = document.createElement('canvas');
canvas.width = 32;
canvas.height = 32;
const ctx = canvas.getContext('2d');

let frameId;
function drawFrame(time) {
  const scale = 0.5 + 0.5 * Math.abs(Math.sin(time / 400));
  ctx.clearRect(0, 0, 32, 32);
  ctx.fillStyle = '#ef4444';
  ctx.beginPath();
  ctx.arc(16, 16, 14 * scale, 0, Math.PI * 2);
  ctx.fill();

  favicon.href = canvas.toDataURL('image/png');
  frameId = requestAnimationFrame(drawFrame);
}

frameId = requestAnimationFrame(drawFrame);

function stopAnimatedFavicon() {
  cancelAnimationFrame(frameId);
  favicon.href = originalHref;
}
```

## Workflow

1. Decide whether motion is justified.
   - Good uses: long-running work, unread attention, live status, secondary-tab tools.
   - Bad uses: decoration, constant branding loops, mobile-first experiences, Safari-critical UX.
2. Preserve the original favicon before changing it.
3. Draw at 16x16 or 32x32 on a canvas.
4. Export frames as `image/png` data URLs and assign them to `link[rel~="icon"]`.
5. Stop the animation as soon as the underlying state ends or the user has seen the notification.
6. Restore the original favicon on stop and during page teardown when appropriate.

## Worker Pattern

For apps that users leave in background tabs, consider a Web Worker with `OffscreenCanvas`. Main-thread `requestAnimationFrame` is throttled in background tabs, especially in Chrome and Edge. A worker can keep producing favicon frames while the main thread only updates the DOM link.

```js
const worker = new Worker('/favicon-worker.js');
worker.onmessage = (event) => {
  if (event.data.type === 'updateFavicon') {
    document.querySelector('link[rel~="icon"]').href = event.data.dataUrl;
  }
};
worker.postMessage({ type: 'start' });
```

Inside the worker, draw on an `OffscreenCanvas`, call `convertToBlob()`, convert the blob to a data URL with `FileReader`, then post `{ type: 'updateFavicon', dataUrl }` back to the page.

## Browser Reality

- Firefox generally animates favicons smoothly, including background tabs.
- Chrome and Edge animate active tabs, but background-tab `requestAnimationFrame` often drops to roughly 1fps.
- Safari may update slowly or inconsistently. Do not rely on smooth favicon animation there.

## Review Checklist

- The animation communicates real user-visible state.
- A static badge would not be enough.
- The favicon is 16x16 or 32x32.
- Frames are PNG data URLs, not hand-encoded ICO files.
- The original favicon is restored.
- The animation has a clear stop condition.
- Worker complexity is used only when background-tab updates matter.
- The implementation avoids permanent loops that waste CPU and battery.

## Reference

Source article: https://favicon.im/es/blog/animated-favicon-live-demo
