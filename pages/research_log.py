import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui.nexus import apply_theme, header

st.set_page_config(page_title="研究記録 | ネクサスラボ", page_icon="🧪", layout="wide")
apply_theme()
header("研究記録")
st.title("研究記録")
st.write("プレイ状況と学習の進行を確認できます。")
rows = [
    {"指標": "ハイ＆ロー 最高連勝", "値": st.session_state.get("highlow_best_streak", 0)},
    {"指標": "ハイ＆ロー 現在ポイント", "値": st.session_state.get("highlow_points", 0)},
    {"指標": "細胞サバイバル ターン", "値": st.session_state.get("survival_turn", 0)},
    {"指標": "酸化還元マスター ターン", "値": st.session_state.get("redox_turn", 0)},
    {"指標": "酵素ラボ スコア", "値": st.session_state.get("mechanism_score", 0)},
    {"指標": "酵素ラボ 正答数", "値": st.session_state.get("mechanism_correct", 0)},
    {"指標": "酵素ラボ 回答数", "値": st.session_state.get("mechanism_attempts", 0)},
    {"指標": "酵素ラボ 最長連続正解", "値": st.session_state.get("mechanism_best_streak", 0)},
]
st.dataframe(rows, hide_index=True, use_container_width=True)
st.caption("ゲームをプレイすると、このセッション中の研究記録が更新されます。")
