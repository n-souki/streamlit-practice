import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui.nexus import apply_theme, header

st.set_page_config(page_title="RESEARCH LOG | NEXUS LAB", page_icon="🧪", layout="wide")
apply_theme()
header("RESEARCH LOG")

st.title("RESEARCH LOG")
st.write("プレイ状況と学習の進行を確認できます。")
rows = [
    {"指標": "High & Low 最高連勝", "値": st.session_state.get("highlow_best_streak", 0)},
    {"指標": "High & Low 現在ポイント", "値": st.session_state.get("highlow_points", 0)},
    {"指標": "CELL SURVIVAL ターン", "値": st.session_state.get("survival_turn", 0)},
    {"指標": "REDOX MASTER ターン", "値": st.session_state.get("redox_turn", 0)},
    {"指標": "ENZYME LAB スコア", "値": st.session_state.get("mechanism_score", 0)},
    {"指標": "ENZYME LAB 正答数", "値": st.session_state.get("mechanism_correct", 0)},
    {"指標": "ENZYME LAB 回答数", "値": st.session_state.get("mechanism_attempts", 0)},
    {"指標": "ENZYME LAB 最長連続正解", "値": st.session_state.get("mechanism_best_streak", 0)},
]
st.dataframe(rows, hide_index=True, use_container_width=True)
st.caption("ゲームをプレイすると、このセッション中の研究記録が更新されます。")
