import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from games.mechanism import render
from ui.nexus import apply_theme, header

st.set_page_config(page_title="生化学について", page_icon="🧪")
apply_theme()
header("生化学を学ぼう")
render()
