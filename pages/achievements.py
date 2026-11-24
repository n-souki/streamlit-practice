import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui.nexus import apply_theme, header

st.set_page_config(page_title="実績 | ネクサスラボ", page_icon="🏆", layout="wide")
apply_theme()
header("実績", st.session_state.get("highlow_points", 0))
st.title("実績")
best = st.session_state.get("highlow_best_streak", 0)
points = st.session_state.get("highlow_points", 0)
achievements = (
    ("初勝利", "最初の勝利を記録", best >= 1),
    ("3連勝", "3回連続で勝利", best >= 3),
    ("5連勝", "5回連続で勝利", best >= 5),
    ("ポイント研究員", "1000ポイント以上を保持", points >= 1000),
)
for name, description, achieved in achievements:
    status = "達成" if achieved else "未達成"
    color = "🟡" if achieved else "⚪"
    st.markdown(f"### {color} {name}　`{status}`")
    st.caption(description)
st.divider()
st.metric("最高連勝", best)
st.metric("現在のポイント", points)
