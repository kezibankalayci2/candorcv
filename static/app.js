"use strict";

const state = {
  csrf: null,
  cvId: null,
  jobId: null,
  analysisId: null,
  optimizationId: null,
  sessionToken: null,
  downloadUrl: null,
  busy: false,
};

const $ = (selector) => document.querySelector(selector);
const elements = {
  file: $("#cv-file"),
  cvState: $("#cv-state"),
  job: $("#job-text"),
  count: $("#job-count"),
  analyze: $("#analyze-button"),
  error: $("#error-box"),
  errorMessage: $("#error-message"),
  status: $("#status-box"),
  mode: $("#mode-badge"),
  analysisSection: $("#analysis-section"),
  decisionSection: $("#decision-section"),
  resultSection: $("#result-section"),
};

function node(tag, className, text) {
  const item = document.createElement(tag);
  if (className) item.className = className;
  if (text !== undefined) item.textContent = text;
  return item;
}

function announce(message) {
  elements.status.textContent = "";
  window.setTimeout(() => { elements.status.textContent = message; }, 20);
}

function showError(message) {
  elements.errorMessage.textContent = message;
  elements.error.hidden = false;
  elements.error.scrollIntoView({ behavior: "smooth", block: "center" });
  announce(message);
}

function clearError() {
  elements.error.hidden = true;
  elements.errorMessage.textContent = "";
}

function setBusy(button, busy, label) {
  state.busy = busy;
  button.disabled = busy;
  if (!button.dataset.label) button.dataset.label = button.textContent;
  button.textContent = busy ? label : button.dataset.label;
}

function updateAnalyzeState() {
  elements.analyze.disabled = state.busy || !state.cvId || elements.job.value.trim().length < 100;
}

function setProgress(step) {
  document.querySelectorAll(".progress-step").forEach((item) => {
    const value = Number(item.dataset.step);
    item.classList.toggle("is-active", value === step);
    item.classList.toggle("is-complete", value < step);
  });
}

async function api(path, options = {}) {
  clearError();
  const headers = { ...(options.headers || {}) };
  let body = options.body;
  if (body) {
    headers["Content-Type"] = "application/json";
    const parsed = JSON.parse(body);
    if (state.sessionToken) parsed._session_state = state.sessionToken;
    body = JSON.stringify(parsed);
  }
  if (options.method && options.method !== "GET") headers["X-CSRF-Token"] = state.csrf;
  const response = await fetch(path, { ...options, body, headers });
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json") ? await response.json() : null;
  if (!response.ok) {
    const message = payload?.error?.message || "The request could not be completed.";
    throw new Error(message);
  }
  if (payload?.state_token) {
    state.sessionToken = payload.state_token;
  }
  if (payload?.csrf_token) state.csrf = payload.csrf_token;
  return payload;
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const value = String(reader.result);
      resolve(value.includes(",") ? value.split(",", 2)[1] : value);
    };
    reader.onerror = () => reject(new Error("The selected CV could not be read."));
    reader.readAsDataURL(file);
  });
}

async function initialize() {
  try {
    const payload = await api("/api/session");
    state.csrf = payload.csrf_token;
    state.cvId = payload.state.cv?.id || null;
    elements.mode.textContent = payload.ai_mode === "openai"
      ? `AI mode · ${payload.model} · short-lived private session`
      : "Verified local mode · add an API key for AI rewriting · short-lived private session";
    if (payload.state.cv) {
      elements.cvState.textContent = `${payload.state.cv.filename} is available in this session.`;
      elements.cvState.classList.add("is-success");
    }
    updateAnalyzeState();
  } catch (error) {
    showError(error.message);
  }
}

elements.file.addEventListener("change", async () => {
  const file = elements.file.files?.[0];
  state.cvId = null;
  updateAnalyzeState();
  if (!file) {
    elements.cvState.textContent = "No CV selected.";
    return;
  }
  if (file.size > 3_000_000) {
    showError("The CV exceeds the 3 MB upload limit.");
    elements.file.value = "";
    return;
  }
  elements.cvState.classList.remove("is-success");
  elements.cvState.textContent = "Reading and validating the CV…";
  announce("Reading and validating the CV.");
  try {
    const dataBase64 = await fileToBase64(file);
    const payload = await api("/api/cv", {
      method: "POST",
      body: JSON.stringify({ filename: file.name, data_base64: dataBase64 }),
    });
    state.cvId = payload.cv.id;
    elements.cvState.textContent = `${payload.cv.filename} is ready · ${payload.summary.blocks} source blocks · ${payload.summary.characters} characters.`;
    elements.cvState.classList.add("is-success");
    announce("The CV is ready for analysis.");
  } catch (error) {
    elements.cvState.textContent = "The CV is not ready.";
    showError(error.message);
  } finally {
    updateAnalyzeState();
  }
});

elements.job.addEventListener("input", () => {
  elements.count.textContent = `${elements.job.value.length.toLocaleString()} / 30,000`;
  updateAnalyzeState();
});

elements.analyze.addEventListener("click", async () => {
  if (!state.cvId) return;
  setBusy(elements.analyze, true, "Analyzing CV…");
  announce("The CV and job description are being analyzed.");
  try {
    const jobPayload = await api("/api/job", {
      method: "POST",
      body: JSON.stringify({ text: elements.job.value }),
    });
    state.jobId = jobPayload.job.id;
    const analysisPayload = await api("/api/analyze", {
      method: "POST",
      body: JSON.stringify({ cv_id: state.cvId, job_id: state.jobId }),
    });
    state.analysisId = analysisPayload.analysis.id;
    renderAnalysis(analysisPayload.analysis);
    elements.analysisSection.hidden = false;
    elements.decisionSection.hidden = false;
    elements.resultSection.hidden = true;
    setProgress(2);
    elements.analysisSection.scrollIntoView({ behavior: "smooth", block: "start" });
    announce("Analysis complete. Review the estimated match and evidence.");
  } catch (error) {
    showError(error.message);
  } finally {
    setBusy(elements.analyze, false, "Analyzing CV…");
    updateAnalyzeState();
  }
});

function clearChildren(element) {
  while (element.firstChild) element.removeChild(element.firstChild);
}

function renderAnalysis(analysis) {
  $("#score-value").textContent = `${analysis.score}%`;
  $("#score-summary").textContent = analysis.summary || `${analysis.score_label}. Review the evidence and not-visible areas below.`;
  $("#score-disclaimer").textContent = analysis.disclaimer;
  $("#analysis-mode").textContent = analysis.mode === "ai"
    ? "AI wording enhancement with deterministic evidence checks."
    : "Deterministic evidence analysis; no external AI rewriting was used.";

  const dimensions = $("#dimensions-list");
  clearChildren(dimensions);
  const dimensionLabels = {
    required_requirements: "Required requirements",
    preferred_requirements: "Preferred requirements",
    keyword_coverage: "Keyword coverage",
    ats_structure: "ATS structure",
  };
  Object.entries(analysis.dimensions).forEach(([key, value]) => {
    const item = node("div", "dimension");
    const label = node("div", "dimension-label");
    label.append(node("span", "", dimensionLabels[key] || key), node("strong", "", `${value}%`));
    const track = node("div", "dimension-track");
    const fill = node("div", "dimension-fill");
    fill.style.width = `${Math.max(0, Math.min(100, value))}%`;
    track.append(fill);
    item.append(label, track);
    dimensions.append(item);
  });

  renderResultItems($("#strengths-list"), analysis.strengths, true);
  renderResultItems($("#missing-list"), analysis.missing_areas, false);

  const keywords = $("#keywords-list");
  clearChildren(keywords);
  analysis.keywords.forEach((keyword) => {
    const supported = keyword.status === "supported";
    keywords.append(node("span", `chip ${supported ? "chip-supported" : "chip-missing"}`, `${supported ? "✓" : "○"} ${keyword.term} · ${supported ? "supported" : "not visible"}`));
  });

  const improvements = $("#improvements-list");
  clearChildren(improvements);
  analysis.improvements.forEach((text) => improvements.append(node("li", "", text)));
}

function renderResultItems(container, items, includeSource) {
  clearChildren(container);
  if (!items.length) {
    container.append(node("p", "", "No evidence was identified for this section."));
    return;
  }
  items.forEach((result) => {
    const item = node("div", "result-item");
    item.append(node("strong", "", result.title), node("p", "", result.detail));
    if (includeSource && result.source) {
      const location = result.source.page ? `page ${result.source.page}` : result.source.section;
      item.append(node("span", "source-note", `Source: ${result.source.source_id} · ${location}`));
    }
    container.append(item);
  });
}

async function saveDecision(choice) {
  if (!state.analysisId) return;
  const yes = $("#decision-yes");
  const no = $("#decision-no");
  yes.disabled = true;
  no.disabled = true;
  try {
    await api("/api/decision", {
      method: "POST",
      body: JSON.stringify({ analysis_id: state.analysisId, choice }),
    });
    setProgress(3);
    if (choice === "no") {
      $("#decision-result").textContent = "Analysis complete. No CV was generated.";
      elements.resultSection.hidden = true;
      announce("The process ended after analysis. No CV was generated.");
      return;
    }
    $("#decision-result").textContent = "Your Yes decision was recorded for this CV and job description only.";
    await createOptimization();
  } catch (error) {
    showError(error.message);
    yes.disabled = false;
    no.disabled = false;
  }
}

$("#decision-yes").addEventListener("click", () => saveDecision("yes"));
$("#decision-no").addEventListener("click", () => saveDecision("no"));

async function createOptimization() {
  announce("Creating and verifying the source-grounded ATS CV.");
  try {
    const payload = await api("/api/optimize", {
      method: "POST",
      body: JSON.stringify({ analysis_id: state.analysisId }),
    });
    const result = payload.optimization;
    state.optimizationId = result.id;
    $("#cv-preview").textContent = result.content;
    if (state.downloadUrl) URL.revokeObjectURL(state.downloadUrl);
    state.downloadUrl = URL.createObjectURL(new Blob([result.content], { type: "text/plain;charset=utf-8" }));
    $("#download-link").href = state.downloadUrl;
    $("#download-link").download = "candorcv-optimized.txt";
    renderChanges(result.references);
    elements.resultSection.hidden = false;
    setProgress(4);
    elements.resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
    announce("The ATS CV is ready. Review every change before downloading.");
  } catch (error) {
    showError(error.message);
    $("#decision-yes").disabled = false;
    $("#decision-no").disabled = false;
  }
}

function renderChanges(references) {
  const changed = references.filter((item) => item.changed);
  $("#change-summary").textContent = `${references.length} source blocks preserved · ${changed.length} wording changes.`;
  const list = $("#changes-list");
  clearChildren(list);
  references.forEach((reference) => {
    const item = node("div", "change-item");
    item.append(node("strong", "", `${reference.source_id} · ${reference.section}`));
    item.append(node("span", "", reference.changed ? "Wording refined; source facts preserved." : "Original wording preserved."));
    list.append(item);
  });
}

$("#delete-session").addEventListener("click", async () => {
  try {
    await api("/api/session", { method: "DELETE", body: "{}" });
    state.csrf = null;
    state.cvId = null;
    state.jobId = null;
    state.analysisId = null;
    state.optimizationId = null;
    if (state.downloadUrl) URL.revokeObjectURL(state.downloadUrl);
    state.downloadUrl = null;
    elements.file.value = "";
    elements.job.value = "";
    elements.cvState.textContent = "No CV selected.";
    elements.cvState.classList.remove("is-success");
    elements.analysisSection.hidden = true;
    elements.decisionSection.hidden = true;
    elements.resultSection.hidden = true;
    setProgress(1);
    announce("Session data deleted. Creating a new private session.");
    await initialize();
  } catch (error) {
    showError(error.message);
  }
});

initialize();
