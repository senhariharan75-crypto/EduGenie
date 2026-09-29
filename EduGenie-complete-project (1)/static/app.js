const task = document.getElementById('task');
const inputText = document.getElementById('inputText');
const submitBtn = document.getElementById('submitBtn');
const clearBtn = document.getElementById('clearBtn');
const result = document.getElementById('result');
const resultBody = document.getElementById('resultBody');
const errorBox = document.getElementById('error');
const copyBtn = document.getElementById('copyBtn');
const levelWrap = document.getElementById('levelWrap');
const weeksWrap = document.getElementById('weeksWrap');

function updateForm() {
  const learning = task.value === 'learn';
  levelWrap.classList.toggle('hidden', !learning);
  weeksWrap.classList.toggle('hidden', !learning);
  inputText.placeholder = {
    qa: 'Example: Which is the largest ocean?',
    explain: 'Example: Pythagoras theorem',
    quiz: 'Paste a lesson or passage here…',
    summarize: 'Paste a long educational passage here…',
    learn: 'Example: SQL database development'
  }[task.value];
}
task.addEventListener('change', updateForm);

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}
function showError(message) { errorBox.textContent = message; errorBox.classList.remove('hidden'); }
function clearError() { errorBox.textContent = ''; errorBox.classList.add('hidden'); }

async function run() {
  clearError();
  const text = inputText.value.trim();
  if (!text) return showError('Please enter some text.');
  submitBtn.disabled = true; submitBtn.textContent = 'Thinking…';
  try {
    let endpoint, body;
    if (task.value === 'qa') { endpoint='/qa'; body={question:text}; }
    if (task.value === 'explain') { endpoint='/explain'; body={topic:text}; }
    if (task.value === 'quiz') { endpoint='/quiz'; body={passage:text,count:3}; }
    if (task.value === 'summarize') { endpoint='/summarize'; body={text}; }
    if (task.value === 'learn') { endpoint='/learn/recommendations'; body={topic:text,level:document.getElementById('level').value,weeks:Number(document.getElementById('weeks').value)}; }
    const response = await fetch(endpoint, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed');
    render(data);
  } catch (err) { showError(err.message); }
  finally { submitBtn.disabled=false; submitBtn.textContent='Run EduGenie'; }
}

function render(data) {
  result.classList.remove('hidden');
  if (data.questions) {
    resultBody.innerHTML = data.questions.map((q, i) => `
      <div class="quiz-question"><h3>${i+1}. ${escapeHtml(q.question)}</h3>
        ${q.options.map(o => `<label class="option"><input type="radio" name="q${i}" value="${escapeHtml(o)}"> ${escapeHtml(o)}</label>`).join('')}
        <button class="secondary reveal" data-index="${i}">Check answer</button>
        <div id="feedback${i}" class="answer"></div>
      </div>`).join('');
    data.questions.forEach((q,i) => document.querySelector(`[data-index="${i}"]`).addEventListener('click', () => {
      const selected = document.querySelector(`input[name="q${i}"]:checked`);
      const feedback = document.getElementById(`feedback${i}`);
      if (!selected) { feedback.textContent='Choose an option first.'; return; }
      feedback.textContent = selected.value === q.correct_answer ? `Correct! ${q.explanation}` : `Correct answer: ${q.correct_answer}. ${q.explanation}`;
    }));
  } else {
    const text = data.answer || data.explanation || data.summary || data.recommendations || '';
    resultBody.innerHTML = `<div class="answer">${escapeHtml(text)}</div>`;
  }
  result.scrollIntoView({behavior:'smooth', block:'start'});
}

clearBtn.addEventListener('click', () => { inputText.value=''; result.classList.add('hidden'); clearError(); });
submitBtn.addEventListener('click', run);
copyBtn.addEventListener('click', async () => {
  await navigator.clipboard.writeText(resultBody.innerText);
  copyBtn.textContent='Copied!'; setTimeout(()=>copyBtn.textContent='Copy',1200);
});

fetch('/health').then(r=>r.json()).then(d=>document.getElementById('health').textContent = d.gemini_configured ? 'API ready' : 'Add GEMINI_API_KEY').catch(()=>document.getElementById('health').textContent='API offline');
updateForm();
