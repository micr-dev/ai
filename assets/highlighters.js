import { highlightSelection } from "https://cdn.jsdelivr.net/npm/@highlighters/core@1.1.1/dist/index.js";

const script = document.currentScript;
const blendMode = script?.dataset.highlightersBlend ?? "screen";
const color = script?.dataset.highlightersColor ?? "#9ca3af";

const options = {
  color,
  opacity: 0.42,
  blendMode,
  ink: {
    flow: 0.5,
    feathering: 0.28,
    streakiness: 0.22,
  },
  animation: {
    trigger: "in-view",
    duration: 460,
  },
};

const selectionHandle = highlightSelection({
  ...options,
  snap: "word",
});

window.addEventListener("pagehide", () => {
  selectionHandle.remove();
});
