const form = document.querySelector("#analysis-form");
const submitButton = document.querySelector("#analyze-button");
const message = document.querySelector("#form-message");
const results = document.querySelector("#results");

function fillList(elementId, values, emptyText) {
  const list = document.getElementById(elementId);
  list.replaceChildren();
  const items = values.length ? values : [emptyText];
  for (const value of items) {
    const item = document.createElement("li");
    item.textContent = value;
    list.append(item);
  }
}

function renderResults(data) {
  const local = data.local_analysis;
  const ai = data.ai_analysis;
  document.querySelector("#match-percentage").textContent = local.match_percentage;
  document.querySelector("#match-bar").style.width = `${local.match_percentage}%`;
  document.querySelector("#matching-count").textContent = `(${local.matching_skills.length})`;
  document.querySelector("#missing-count").textContent = `(${local.missing_skills.length})`;
  fillList("matching-skills", local.matching_skills, "No recognized overlap yet");
  fillList("missing-skills", local.missing_skills, "No recognized JD skills are missing");
  fillList("strengths", ai.relevant_strengths, "No specific strengths were identified.");
  fillList("projects", ai.project_relevance, "No directly relevant project was mentioned.");
  fillList("suggestions", ai.resume_suggestions, "No suggestions returned.");
  fillList("questions", ai.interview_questions, "No questions returned.");
  document.querySelector("#overall-analysis").textContent = ai.overall_analysis;
  results.hidden = false;
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const resume = document.querySelector("#resume").value.trim();
  const jobDescription = document.querySelector("#job-description").value.trim();
  message.classList.remove("error");

  if (!resume || !jobDescription) {
    message.textContent = !resume ? "Please add your resume text." : "Please add the job description.";
    message.classList.add("error");
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Analyzing...";
  message.textContent = "Analyzing your profile...";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume, job_description: jobDescription }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to analyze this profile.");
    renderResults(data);
    message.textContent = "Analysis complete.";
  } catch (error) {
    message.textContent = error instanceof TypeError
      ? "Could not reach the server. Check your connection and try again."
      : error.message;
    message.classList.add("error");
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = 'Analyze My Profile <span aria-hidden="true">→</span>';
  }
});

document.querySelector("#new-analysis").addEventListener("click", () => {
  results.hidden = true;
  document.querySelector("#resume").focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
});