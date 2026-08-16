const form = document.getElementById("analysisForm");
const level = document.getElementById("technicalLevel");
const levelValue = document.getElementById("levelValue");
const button = document.getElementById("submitButton");
const statusBox = document.getElementById("status");
const emptyState = document.getElementById("emptyState");
const resultBox = document.getElementById("result");

level.addEventListener("input", () => {
  levelValue.textContent = `${level.value} / 5`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    profession: document.getElementById("profession").value.trim(),
    ai_usage: document.getElementById("aiUsage").value,
    technical_level: Number(level.value),
    expectation: document.getElementById("expectation").value.trim()
  };

  button.disabled = true;
  statusBox.className = "status";
  statusBox.textContent = "Yerel yapay zekâ analiz ediyor...";

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Analiz sırasında bir hata oluştu.");
    }

    document.getElementById("profile").textContent = data.profile;
    document.getElementById("aiLevel").textContent = data.ai_level;
    document.getElementById("priorityNeed").textContent = data.priority_need;
    document.getElementById("recommendation").textContent = data.recommendation;

    const useCases = document.getElementById("useCases");
    useCases.innerHTML = "";
    (data.use_cases || []).forEach(item => {
      const chip = document.createElement("span");
      chip.className = "chip";
      chip.textContent = item;
      useCases.appendChild(chip);
    });

    emptyState.classList.add("hidden");
    resultBox.classList.remove("hidden");
    statusBox.textContent = "Analiz tamamlandı.";
  } catch (error) {
    statusBox.className = "status error";
    statusBox.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});
