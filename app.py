import streamlit as st

from ui.nexus import apply_theme, card, header

st.set_page_config(page_title="ネクサスラボ", page_icon="🧪", layout="wide")
apply_theme()
header("ホーム")

st.title("ネクサスラボ")
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
metric_cols[0].metric("ポイント", points)
metric_cols[1].metric("最長連続正解", best_streak)
metric_cols[2].metric("実績", f"{achievement_count} / 4")

st.subheader("研究室を選択")
left, right = st.columns(2)
with left:
    card("ハイ＆ロー", "トランプの確率と判断力を試すカードラボ。", "♠")
    st.page_link("pages/high_and_low_game.py", label="ハイ＆ローを開く", icon="🃏")
with right:
    card("生化学", "DNA、ATP、NADH、酵素をテーマにした研究ゲーム群。", "🧬")
    st.page_link("pages/biochemistry.py", label="生化学を開く", icon="🧬")

st.subheader("今日のミッション")
st.info("今日のミッション：ハイを3回選択して、判断データを記録する")