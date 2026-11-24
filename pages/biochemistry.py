import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ui.nexus import apply_theme, card, header

st.set_page_config(page_title="BIOCHEMISTRY | NEXUS LAB", page_icon="🧬", layout="wide")
apply_theme()
header("BIOCHEMISTRY")
st.title("BIOCHEMISTRY GAMES")
st.write("分子・エネルギー・反応機構を、研究室の実験記録として学びます。")

games = (
    ("翻訳工場", "mRNAコドンとtRNAアンチコドン", "基礎", "pages/translation_factory.py", "🧬"),
    ("REDOX MASTER", "NADHとNADPHの代謝戦略", "中級", "pages/redox_master.py", "⚡"),
    ("ENZYME LAB", "PDH複合体の反応機構", "上級", "pages/enzyme_lab.py", "🧪"),
    ("CELL SURVIVAL", "細胞内資源と代謝経路の管理", "上級", "pages/cell_survival.py", "🔬"),
)
for title, description, difficulty, page, icon in games:
    card(title, f"{description}<br><small>DIFFICULTY: {difficulty}</small>", icon)
    st.page_link(page, label=f"{title}を開く", icon="🧪")
