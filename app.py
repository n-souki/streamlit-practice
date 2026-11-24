import streamlit as st

from ui.nexus import apply_theme, card, header

st.set_page_config(page_title="NEXUS LAB", page_icon="🧪", layout="wide")
apply_theme()
header("HOME")

st.title("NEXUS LAB")
st.write("科学研究施設とゲームセンターが交差する、学習ゲームの実験場です。")

points = st.session_state.get("highlow_points", 0)
best_streak = st.session_state.get("highlow_best_streak", 0)
achievement_count = sum(
    (
        best_streak >= 1,
        best_streak >= 3,
        best_streak >= 5,
        points >= 1000,
    )
)
metric_cols = st.columns(3)
metric_cols[0].metric("POINTS", points)
metric_cols[1].metric("BEST STREAK", best_streak)
metric_cols[2].metric("ACHIEVEMENTS", f"{achievement_count} / 4")

st.subheader("SELECT YOUR LAB")
left, right = st.columns(2)
with left:
    card("HIGH & LOW", "トランプの確率と判断力を試すカードラボ。", "♠")
    st.page_link("pages/high_and_low_game.py", label="HIGH & LOWを開く", icon="🃏")
with right:
    card("BIOCHEMISTRY", "DNA、ATP、NADH、酵素をテーマにした研究ゲーム群。", "🧬")
    st.page_link("pages/biochemistry.py", label="BIOCHEMISTRYを開く", icon="🧬")

st.subheader("DAILY MISSION")
st.info("今日のミッション：Highを3回選択して、判断データを記録する")