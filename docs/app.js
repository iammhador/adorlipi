let pyodide = null;

const statusEl = document.getElementById("status");
const inputEl = document.getElementById("inputText");
const outputEl = document.getElementById("outputText");
const metaEl = document.getElementById("metaText");
const suggestionsEl = document.getElementById("suggestionsText");
const transliterateBtn = document.getElementById("transliterateBtn");
const clearBtn = document.getElementById("clearBtn");
const mappingSearchEl = document.getElementById("mappingSearch");
const mappingSearchResultsEl = document.getElementById("mappingSearchResults");
const conjunctStatsEl = document.getElementById("conjunctStats");

let fullMappingEntries = [];

const KEYBOARD_LAYOUT = [
  ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
  ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
  ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
  ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
];

function setStatus(message) {
  statusEl.textContent = message;
}

async function fetchJson(path) {
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`Failed to load ${path}: ${res.status}`);
  }
  return res.json();
}

function esc(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function sortedEntries(obj) {
  return Object.entries(obj).sort((a, b) => {
    if (a[0].length !== b[0].length) {
      return a[0].length - b[0].length;
    }
    return a[0].localeCompare(b[0]);
  });
}

function renderMapTable(containerId, entries, columns = { key: "Key", output: "Output" }) {
  const container = document.getElementById(containerId);
  const rows = entries
    .map(([key, value]) => `<tr><td><code>${esc(key)}</code></td><td>${esc(value)}</td></tr>`)
    .join("");

  container.innerHTML = `
    <div class="map-table-wrap">
      <table class="map-table">
        <thead>
          <tr><th>${columns.key}</th><th>${columns.output}</th></tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function buildKeyboard(mapping) {
  const grid = document.getElementById("keyboardGrid");
  const rowsHtml = KEYBOARD_LAYOUT.map((row, idx) => {
    const keycaps = row.map((key) => {
      const outputs = [];
      if (mapping.vowels[key]) outputs.push(`<span class="pill">স্বর: ${esc(mapping.vowels[key])}</span>`);
      if (mapping.consonants[key]) outputs.push(`<span class="pill alt">ব্যঞ্জন: ${esc(mapping.consonants[key])}</span>`);
      if (mapping.kars[key]) outputs.push(`<span class="pill warn">কার: ${esc(mapping.kars[key])}</span>`);
      if (mapping.folas[key]) outputs.push(`<span class="pill">ফলা: ${esc(mapping.folas[key])}</span>`);
      if (outputs.length === 0) outputs.push(`<span class="pill">-</span>`);
      return `
        <div class="keycap">
          <span class="k">${esc(key)}</span>
          <div class="out">${outputs.join("")}</div>
        </div>
      `;
    }).join("");

    const rowClass = idx === 2 ? "row-3" : idx === 3 ? "row-4" : "";
    return `<div class="keyboard-row ${rowClass}">${keycaps}</div>`;
  }).join("");
  grid.innerHTML = rowsHtml;
}

function collectFullEntries(mapping, conjunctPairs) {
  const entries = [];
  for (const [key, value] of Object.entries(mapping.vowels || {})) {
    entries.push({ category: "vowel", key, value });
  }
  for (const [key, value] of Object.entries(mapping.consonants || {})) {
    entries.push({ category: "consonant", key, value });
  }
  for (const [key, value] of Object.entries(mapping.kars || {})) {
    entries.push({ category: "kar", key, value });
  }
  for (const [key, value] of Object.entries(mapping.folas || {})) {
    entries.push({ category: "fola", key, value });
  }
  for (const [key, value] of Object.entries(conjunctPairs || {})) {
    entries.push({ category: "conjunct", key, value });
  }
  return entries;
}

function renderSearchResults(rows) {
  const limited = rows.slice(0, 160);
  const body = limited.map((entry) => `
    <tr>
      <td>${esc(entry.category)}</td>
      <td><code>${esc(entry.key)}</code></td>
      <td>${esc(entry.value)}</td>
    </tr>
  `).join("");
  mappingSearchResultsEl.innerHTML = `
    <div class="map-table-wrap">
      <table class="map-table">
        <thead>
          <tr><th>Category</th><th>Key</th><th>Output</th></tr>
        </thead>
        <tbody>${body}</tbody>
      </table>
    </div>
    <p class="muted">Showing ${limited.length} of ${rows.length} matched entries.</p>
  `;
}

function bindSearch() {
  mappingSearchEl.addEventListener("input", () => {
    const q = mappingSearchEl.value.trim().toLowerCase();
    if (!q) {
      renderSearchResults(fullMappingEntries);
      return;
    }
    const filtered = fullMappingEntries.filter((entry) =>
      entry.key.toLowerCase().includes(q) || entry.value.includes(mappingSearchEl.value.trim())
    );
    renderSearchResults(filtered);
  });
}

async function initMappingDocumentation() {
  const mapping = await fetchJson("./runtime/data/mapping.json");
  const inspired = await fetchJson("./runtime/data/inspired_conjuncts.json");
  const conjunctPairs = inspired.pairs || {};

  const vowelEntries = sortedEntries(mapping.vowels).filter(([key]) => !/^\d$/.test(key));
  const consonantEntries = sortedEntries(mapping.consonants);
  const karEntries = sortedEntries(mapping.kars);
  const folaEntries = sortedEntries(mapping.folas);
  const conjunctEntries = sortedEntries(conjunctPairs);

  renderMapTable("vowelTable", vowelEntries);
  renderMapTable("consonantTable", consonantEntries);
  renderMapTable("karTable", karEntries);
  renderMapTable("folaTable", folaEntries);
  renderMapTable("conjunctTable", conjunctEntries, { key: "Key Pair", output: "Conjunct" });
  conjunctStatsEl.textContent = `Total inspired conjunct pairs: ${conjunctEntries.length}`;

  buildKeyboard(mapping);
  fullMappingEntries = collectFullEntries(mapping, conjunctPairs);
  renderSearchResults(fullMappingEntries);
  bindSearch();
}

async function loadRuntimeFiles(manifest) {
  for (const relativePath of manifest.files) {
    const res = await fetch(`./runtime/${relativePath}`);
    if (!res.ok) {
      throw new Error(`Missing runtime file: ${relativePath}`);
    }
    const text = await res.text();
    const target = `/workspace/${relativePath}`;
    const lastSlash = target.lastIndexOf("/");
    const dir = target.slice(0, lastSlash);
    pyodide.FS.mkdirTree(dir);
    pyodide.FS.writeFile(target, text, { encoding: "utf8" });
  }
}

async function boot() {
  try {
    await initMappingDocumentation();
  } catch (err) {
    console.error(err);
    if (conjunctStatsEl) {
      conjunctStatsEl.textContent = "Mapping docs failed to load.";
    }
  }

  setStatus("Loading Python runtime...");
  pyodide = await loadPyodide();

  const manifest = await fetchJson("./runtime/manifest.json");
  setStatus("Loading AdorLipi engine files...");
  await loadRuntimeFiles(manifest);

  setStatus("Initializing transliterator...");
  pyodide.runPython(`
import json
import sys
sys.path.insert(0, "/workspace")
from core.engine.transliterator import Transliterator

_web_engine = Transliterator(data_dir="/workspace/data")

def _web_transliterate(text):
    cleaned = text.strip()
    info = _web_engine.explain_word(cleaned) if cleaned and " " not in cleaned else None
    suggestions = _web_engine.get_suggestions(cleaned) if cleaned and " " not in cleaned else []
    payload = {
        "output": _web_engine.transliterate(text),
        "info": info,
        "suggestions": suggestions,
    }
    return json.dumps(payload, ensure_ascii=False)
`);

  setStatus("Ready.");
  transliterateBtn.disabled = false;
}

async function runTransliteration() {
  if (!pyodide) {
    return;
  }

  const text = inputEl.value || "";
  pyodide.globals.set("INPUT_TEXT", text);
  const raw = pyodide.runPython("_web_transliterate(INPUT_TEXT)");
  pyodide.globals.delete("INPUT_TEXT");

  const payload = JSON.parse(raw);
  outputEl.textContent = payload.output || "-";

  if (payload.info) {
    metaEl.textContent = [
      `source: ${payload.info.source_layer}`,
      `confidence: ${Number(payload.info.confidence || 0).toFixed(2)}`,
      `matched_key: ${payload.info.matched_key || "-"}`,
    ].join("\n");
  } else {
    metaEl.textContent = "-";
  }

  if (payload.suggestions && payload.suggestions.length > 0) {
    suggestionsEl.textContent = payload.suggestions.join("\n");
  } else {
    suggestionsEl.textContent = "-";
  }
}

transliterateBtn.addEventListener("click", runTransliteration);
inputEl.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    runTransliteration();
  }
});
clearBtn.addEventListener("click", () => {
  inputEl.value = "";
  outputEl.textContent = "-";
  metaEl.textContent = "-";
  suggestionsEl.textContent = "-";
});

boot().catch((err) => {
  console.error(err);
  setStatus(`Failed to load demo: ${err.message}`);
  if (conjunctStatsEl && conjunctStatsEl.textContent.includes("Loading")) {
    conjunctStatsEl.textContent = "Failed to load mapping data.";
  }
});
