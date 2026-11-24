"""Shared visual system for NEXUS LAB."""

import streamlit as st

CSS = """
<style>
:root {
  --nexus-bg: #101C2C;
  --nexus-panel: #1C3045;
  --nexus-mint: #66E3C4;
  --nexus-blue: #65BDE8;
  --nexus-gold: #F5BD69;
  --nexus-text: #F1F5F9;
  --nexus-muted: #D8E3EC;
  --nexus-border: #34475B;
}
.stApp { background: var(--nexus-bg); color: var(--nexus-text); }
.stApp p,
.stApp li,
.stApp label,
.stApp caption,
.stApp small,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stWidgetLabel"],
.stApp [data-testid="stAlertContent"] {
  color: var(--nexus-text) !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
  color: var(--nexus-text) !important;
}
div[data-baseweb="select"] *,
div[data-baseweb="input"] *,
[data-testid="stCheckbox"] *,
[data-testid="stMultiSelect"] * {
  color: var(--nexus-text) !important;
}
[data-testid="stRadio"] {
  background: #eef3f7;
  border: 1px solid #cbd6df;
  border-radius: 10px;
  padding: .55rem .75rem;
}
[data-testid="stRadio"] *,
[data-testid="stRadio"] label,
[data-testid="stRadio"] p,
[data-testid="stRadio"] span,
[data-testid="stRadio"] div {
  color: #17212b !important;
}
[data-testid="stDataFrame"] *,
[data-testid="stTable"] * {
  color: #17212b !important;
  border-color: var(--nexus-border) !important;
}
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[role="listbox"] *,
[role="option"] * {
  color: #17212b !important;
}
.stAlert,
.stAlert p,
.stAlert strong,
.stAlert span,
.stAlert div {
  color: #17212b !important;
}
h1, h2, h3, h4, h5, h6 {
  color: var(--nexus-text) !important;
  letter-spacing: .02em;
}
[data-testid="stSidebar"] { background: #0c1726; border-right: 1px solid var(--nexus-border); }
[data-testid="stSidebar"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] small {
  color: var(--nexus-gold) !important;
}
[data-testid="stSidebar"] a { color: var(--nexus-gold) !important; }
[data-testid="stSidebar"] a:hover { color: #ffd18a !important; }
.nexus-header {
  padding: 1.1rem 1.3rem; margin-bottom: 1.2rem;
  border: 1px solid var(--nexus-border); border-radius: 18px;
  background: linear-gradient(135deg, #1c3045, #142638);
  box-shadow: 0 10px 28px rgba(0,0,0,.18);
}
.nexus-brand { color: var(--nexus-mint); font-size: 1.8rem; font-weight: 800; }
.nexus-subtitle { color: var(--nexus-muted); letter-spacing: .22em; font-size: .72rem; }
.nexus-page { color: var(--nexus-blue); margin-top: .5rem; }
.nexus-card {
  padding: 1.2rem; min-height: 130px; border: 1px solid var(--nexus-border);
  border-radius: 16px; background: var(--nexus-panel); margin-bottom: 1rem;
}
.nexus-card h3 { color: var(--nexus-mint); margin-top: 0; }
.stButton > button {
  border: 1px solid var(--nexus-border); border-radius: 10px;
  background: var(--nexus-panel); color: var(--nexus-text);
  transition: background .18s ease, border-color .18s ease, transform .18s ease;
}
.stButton > button:hover { background: #294861; border-color: var(--nexus-mint); transform: translateY(-1px); }
[data-testid="stMetric"] {
  background: var(--nexus-panel); border: 1px solid var(--nexus-border);
  border-radius: 14px; padding: .8rem;
}
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
  background: var(--nexus-panel); border-color: var(--nexus-border);
}
.stAlert { border-radius: 12px; }
@media (max-width: 700px) {
  .nexus-header { padding: .9rem; }
  .nexus-brand { font-size: 1.45rem; }
}
</style>
"""


def apply_theme() -> None:
    """Apply the shared NEXUS LAB color palette and component styles."""
    st.markdown(CSS, unsafe_allow_html=True)
    st.sidebar.markdown("## NEXUS LAB")
    st.sidebar.caption("PLAY. THINK. DISCOVER.")
    st.sidebar.markdown("---")
    st.sidebar.page_link("app.py", label="HOME", icon="🏠")
    st.sidebar.page_link("pages/high_and_low_game.py", label="HIGH & LOW", icon="🃏")
    st.sidebar.page_link("pages/biochemistry.py", label="BIOCHEMISTRY", icon="🧬")
    st.sidebar.page_link("pages/achievements.py", label="ACHIEVEMENTS", icon="🏆")
    st.sidebar.page_link("pages/research_log.py", label="RESEARCH LOG", icon="🧪")


def header(page_name: str, points: int | None = None) -> None:
    """Render a consistent brand header."""
    points_text = f"<span>POINTS {points}</span>" if points is not None else ""
    st.markdown(
        f"""
        <div class="nexus-header">
          <div class="nexus-brand">NEXUS LAB</div>
          <div class="nexus-subtitle">PLAY. THINK. DISCOVER.</div>
          <div class="nexus-page">{page_name} {points_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str, icon: str = "") -> None:
    """Render a reusable informational card."""
    st.markdown(
        f'<div class="nexus-card"><h3>{icon} {title}</h3><div>{body}</div></div>',
        unsafe_allow_html=True,
    )
