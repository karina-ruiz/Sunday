let questions = [];
let currentQuestion = 0;
let currentTest = "";
const answers = {};

const startBtn = document.getElementById("start-btn");
const testMenu = document.getElementById("test-menu");
const quizContainer = document.getElementById("quiz-container");
const nextBtn = document.getElementById("next-btn");
const resultDiv = document.getElementById("result");

// Mostrar menú de tests
startBtn.addEventListener("click", () => {
  document.getElementById("intro").classList.add("hidden");
  testMenu.classList.remove("hidden");
});

// Elegir test y cargar preguntas
document.querySelectorAll(".test-btn").forEach((btn) => {
  btn.addEventListener("click", async () => {
    currentTest = btn.dataset.test;
    await loadQuestions(currentTest);
    resetTest();
    showQuestion();
  });
});

// Cargar preguntas desde JSON
async function loadQuestions(testName) {
    try {
      const res = await fetch(`tests/${testName}.json`);
      questions = await res.json();
      console.log("Preguntas cargadas:", questions); 
    } catch (error) {
      console.error("Error al cargar preguntas:", error);
    }
  }
  
// Reiniciar estado antes del test
function resetTest() {
  currentQuestion = 0;
  answers[currentTest] = 0;
  testMenu.classList.add("hidden");
  quizContainer.classList.remove("hidden");
  nextBtn.classList.remove("hidden");
  resultDiv.classList.add("hidden");
}

// Mostrar la pregunta actual
function showQuestion() {
  const q = questions[currentQuestion];

  const optionsHTML = q.options
    .map(opt => `
      <label>
        <input type="radio" name="answer" value="${opt.value}">
        ${opt.value}. ${opt.text}
      </label>
    `)
    .join("");

  quizContainer.innerHTML = `
    <h3>${q.question}</h3>
    ${optionsHTML}
  `;
}

// Obtener opción seleccionada
function getSelectedValue() {
  const options = document.getElementsByName("answer");
  for (let opt of options) {
    if (opt.checked) return parseInt(opt.value);
  }
  return null;
}

// Botón siguiente
nextBtn.addEventListener("click", () => {
  const val = getSelectedValue();
  if (val === null) {
    alert("Por favor selecciona una opción.");
    return;
  }

  const category = questions[currentQuestion].category;
  answers[category] += val;

  currentQuestion++;
  if (currentQuestion < questions.length) {
    showQuestion();
  } else {
    showResult();
  }
});

// Mostrar resultado final
function showResult() {
  quizContainer.classList.add("hidden");
  nextBtn.classList.add("hidden");
  resultDiv.classList.remove("hidden");

  const score = answers[currentTest];
  let mensaje = `<h2>Resultado del test: ${capitalize(currentTest)}</h2>`;

  if (score >= 10) {
    mensaje += "🔴 Alta probabilidad de síntomas graves.";
  } else if (score >= 6) {
    mensaje += "🟠 Posibles síntomas moderados.";
  } else {
    mensaje += "🟢 No se detectan síntomas preocupantes.";
  }

  mensaje += "<p><strong>Este test no reemplaza una evaluación profesional.</strong></p>";
  resultDiv.innerHTML = mensaje;
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
