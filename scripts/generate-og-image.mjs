import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { execFileSync } from "node:child_process";

const root = resolve(import.meta.dirname, "..");
const indexPath = resolve(root, "index.html");
const svgPath = resolve(root, "assets/og-image.svg");
const pngPath = resolve(root, "og-image.png");
const html = readFileSync(indexPath, "utf8");
const today = new Date().toISOString().slice(0, 10);
const version = today.replaceAll("-", "");

function escapeXml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function textFromHtml(value) {
  return value.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim()
    .replaceAll("&amp;", "&").replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">").replaceAll("&quot;", '"').replaceAll("&#39;", "'");
}

function section(title) {
  const match = html.match(new RegExp(`<section class="stack-section"[^>]*>[\\s\\S]*?<h2 class="section-heading">${title}</h2>([\\s\\S]*?)(?=<section class="stack-section"|</main>)`));
  if (!match) throw new Error(`Missing section: ${title}`);
  return [...match[1].matchAll(/<span class="(?:entry-name|skill-name[^\"]*)">([\s\S]*?)<\/span>/g)]
    .map((match) => textFromHtml(match[1]));
}

function fitNames(names, limit = 4) {
  const selected = names.slice(0, limit);
  if (names.length > limit) selected.push(`+ ${names.length - limit} more`);
  return selected.join(" · ");
}

const models = section("Models");
const harnesses = section("Harnesses");
const toolSections = ["Hooks", "MCPs", "CLI", "Code Review", "Skills", "Workspace"];
const toolNames = toolSections.flatMap((title) => section(title));
const toolCount = toolNames.length;
const lines = [
  ["Models", fitNames(models)],
  ["Harnesses", fitNames(harnesses)],
  ["Tools", `${toolCount} entries · ${toolSections.length} categories`],
];

const detailLines = lines.flatMap(([title, value], index) => {
  const y = 128 + index * 136;
  return [
    `    <text x="588" y="${y}" font-size="24" font-weight="500" fill="#fff">${escapeXml(title)}</text>`,
    `    <text x="588" y="${y + 30}" font-size="20" fill="#8b8b8b">${escapeXml(value)}</text>`,
    ...(index < lines.length - 1 ? [`    <line x1="588" y1="${y + 86}" x2="1126" y2="${y + 86}" stroke="#242424"/>`] : []),
  ];
}).join("\n");

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <style>
    .sans { font-family: 'Helvetica Neue', sans-serif; }
    .mono { font-family: 'Ioskeley Mono', monospace; }
  </style>
  <rect width="1200" height="630" fill="#121212"/>
  <g class="sans" fill="#fff">
    <text x="78" y="176" font-size="82" font-weight="700">AI Stack</text>
    <text x="82" y="218" font-size="24" fill="#8b8b8b">the tools behind the work</text>
    <line x1="82" y1="270" x2="404" y2="270" stroke="#fff" stroke-width="2"/>
    <text x="82" y="340" font-size="27" font-weight="500">models → harnesses → tools</text>
    <text x="82" y="380" font-size="23" fill="#8b8b8b">hooks, MCPs, CLI, skills, workspace</text>
  </g>
  <line x1="536" y1="78" x2="536" y2="552" stroke="#242424" stroke-width="1"/>
  <g class="sans">
${detailLines}
  </g>
  <text x="1126" y="572" text-anchor="end" class="mono" font-size="16" fill="#555">updated ${today} · ai.micr.dev</text>
</svg>
`;

writeFileSync(svgPath, svg);
execFileSync("convert", ["-background", "#121212", "-depth", "8", "-colorspace", "sRGB", "-type", "TrueColor", "-define", "png:color-type=2", "-define", "png:exclude-chunk=date,time", svgPath, pngPath], { stdio: "inherit" });
const updatedHtml = html.replace(/https:\/\/ai\.micr\.dev\/og-image\.png(?:\?v=\d+)?/g, `https://ai.micr.dev/og-image.png?v=${version}`);
writeFileSync(indexPath, updatedHtml);
console.log(`Generated og-image.png and cache-busted metadata for ${today}`);
