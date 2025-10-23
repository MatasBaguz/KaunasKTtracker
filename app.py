import streamlit as st
from streamlit.components.v1 import html

# --- Puslapio konfigūracija ---
st.set_page_config(page_title="Kill Team Tracker", layout="wide")
st.title("⚔️ Kill Team Tracker")

# --- CSS stilius ---
style = """
<style>
.round-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 10px;
  margin-bottom: 20px;
}
.round {
  width: 40px;
  height: 40px;
  border: 2px solid black;
  border-radius: 50%;
  text-align: center;
  line-height: 38px;
  font-weight: bold;
  font-size: 18px;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.round.active {
  background-color: #e74c3c;
  color: white;
}
.container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
  margin-left: 25px;
  margin-top: 10px;
}
.row {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-direction: row;
}
.label {
  width: 120px;
  text-align: left;
  font-weight: bold;
  font-size: 16px;
}
.dots {
  display: flex;
  flex-direction: row;
  gap: 6px;
}
.dot {
  width: 32px;
  height: 32px;
  border: 2px solid black;
  border-radius: 50%;
  background-color: white;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.dot.active-red { background-color: #e74c3c; }
.dot.active-blue { background-color: #3498db; }
.separator {
  width: 100%;
  height: 2px;
  background-color: black;
  margin: 16px 0;
}
.scoreboard {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  margin-top: 10px;
  margin-bottom: 10px;
}
.reset-btn {
  background-color: #555;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  display: block;
  margin: 10px auto;
}
.hidden {
  color: gray;
  font-style: italic;
}
</style>
"""

# --- Inicijuojam sesijos kintamuosius ---
if "mission1" not in st.session_state:
    st.session_state.mission1 = None
if "mission2" not in st.session_state:
    st.session_state.mission2 = None

# --- Slaptos misijos pasirinkimai ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Žaidėjas 1")
    if st.session_state.mission1 is None:
        mission1 = st.selectbox(
            "Pasirink slaptą misiją:",
            ["Crit op", "Tac op", "Kill op"],
            index=None,
            placeholder="Pasirink misiją...",
            key="m1"
        )
        if mission1:
            st.session_state.mission1 = mission1
    else:
        st.markdown("<p class='hidden'>🔒 Slapta misija nustatyta</p>", unsafe_allow_html=True)

with col2:
    st.subheader("🔵 Žaidėjas 2")
    if st.session_state.mission2 is None:
        mission2 = st.selectbox(
            "Pasirink slaptą misiją:",
            ["Crit op", "Tac op", "Kill op"],
            index=None,
            placeholder="Pasirink misiją...",
            key="m2"
        )
        if mission2:
            st.session_state.mission2 = mission2
    else:
        st.markdown("<p class='hidden'>🔒 Slapta misija nustatyta</p>", unsafe_allow_html=True)

mission1 = st.session_state.mission1 or ""
mission2 = st.session_state.mission2 or ""

# --- JS logika ---
script = f"""
<script>
let redScore = 0;
let blueScore = 0;
let redLines = [0, 0, 0];
let blueLines = [0, 0, 0];
let redMission = '{mission1}';
let blueMission = '{mission2}';

function toggleDot(dot, team, line) {{
  let isActive = dot.classList.contains('active-' + team);
  if (isActive) {{
    dot.classList.remove('active-' + team);
    if (team === 'red') {{ redScore--; redLines[line]--; }}
    else {{ blueScore--; blueLines[line]--; }}
  }} else {{
    dot.classList.add('active-' + team);
    if (team === 'red') {{ redScore++; redLines[line]++; }}
    else {{ blueScore++; blueLines[line]++; }}
  }}
  updateScore();
}}

function updateScore() {{
  document.getElementById('score').innerText = redScore + " : " + blueScore;
}}

function resetAll() {{
  document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active-red', 'active-blue'));
  redScore = 0; blueScore = 0;
  redLines = [0,0,0];
  blueLines = [0,0,0];
  document.getElementById('score').innerText = "0 : 0";
}}

function setRound(n) {{
  const rounds = document.querySelectorAll('.round');
  if (n === 5) {{
    const confirmEnd = confirm("Ar tikrai nori pabaigti žaidimą?");
    if (!confirmEnd) return;

    let bonusRed = 0;
    let bonusBlue = 0;

    if (redMission === "Crit op") bonusRed += Math.ceil(redLines[0] / 2);
    else if (redMission === "Tac op") bonusRed += Math.ceil(redLines[1] / 2);
    else if (redMission === "Kill op") bonusRed += Math.ceil(redLines[2] / 2);

    if (blueMission === "Crit op") bonusBlue += Math.ceil(blueLines[0] / 2);
    else if (blueMission === "Tac op") bonusBlue += Math.ceil(blueLines[1] / 2);
    else if (blueMission === "Kill op") bonusBlue += Math.ceil(blueLines[2] / 2);

    redScore += bonusRed;
    blueScore += bonusBlue;

    updateScore();

    alert(
      "Žaidimas baigtas!\\n" +
      "🔴 Misija: " + (redMission || "??") + " +" + bonusRed +
      "\\n🔵 Misija: " + (blueMission || "??") + " +" + bonusBlue +
      "\\n\\nGalutinis rezultatas: " + redScore + " : " + blueScore
    );
  }}

  rounds.forEach(el => el.classList.remove('active'));
  if (n > 0 && n <= rounds.length) rounds[n - 1].classList.add('active');
}}
</script>
"""

# --- HTML struktūra ---
html_code = """
<div class="round-container">
  <div class="round" onclick="setRound(1)">1</div>
  <div class="round" onclick="setRound(2)">2</div>
  <div class="round" onclick="setRound(3)">3</div>
  <div class="round" onclick="setRound(4)">4</div>
  <div class="round" onclick="setRound(5)">END</div>
</div>

<button class="reset-btn" onclick="resetAll()">Reset All</button>
<div class="scoreboard" id="score">0 : 0</div>

<div class="container">
<h4 style="color:#e74c3c;">🔴 Žaidėjas 1</h4>
"""

labels1 = ["Crit op", "Tac op", "Kill op"]
for i, label in enumerate(labels1):
    dots_html = "".join(
        [f"<div class='dot' onclick=\"toggleDot(this, 'red', {i})\"></div>" for _ in range(6)]
    )
    html_code += f"<div class='row'><div class='label'>{label}</div><div class='dots'>{dots_html}</div></div>"

html_code += "<div class='separator'></div><h4 style='color:#3498db;'>🔵 Žaidėjas 2</h4>"

labels2 = ["Crit op", "Tac op", "Kill op"]
for i, label in enumerate(labels2):
    dots_html = "".join(
        [f"<div class='dot' onclick=\"toggleDot(this, 'blue', {i})\"></div>" for _ in range(6)]
    )
    html_code += f"<div class='row'><div class='label'>{label}</div><div class='dots'>{dots_html}</div></div>"

html_code += "</div>"

# --- Atvaizduojam viską ---
html(style + script + html_code, height=950)
