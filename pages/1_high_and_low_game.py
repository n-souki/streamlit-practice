import streamlit as st
import json
from pathlib import Path

# タイトル
st.title("_High & Low_ Game")
st.write("**High & Low** ゲームへようこそ！")

# JSONファイルを読み込む
json_path = Path(__file__).parent.parent / "sample_data" / "highlow.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# カードの情報
base_card = data["base_card"] 
result_card = data["result_card"]

st.write("次のカードは大きい？ 小さい？")
st.write("**High** か **Low** を選んでください。")

# 最初のカードを表示
st.write("最初のカード")
st.header(
    f"{base_card['suit']} {base_card['rank']}"
)

# 次のカードを表示
st.write("次のカード")
st.header(
    f"{result_card['suit']} {result_card['rank']}"
)



st.button("High") 
st.button("Low")

# ===== デザインの追加 =====
st.markdown("""
<style>
/* 背景：かなり濃い緑 */
.stApp {
    background: linear-gradient(135deg, #03140f, #062b1d);
}

/* メイン部分 */
.block-container {
    max-width: 850px;
    padding-top: 2.5rem;
}

/* タイトル：明るい金色 */
h1 {
    color: #ffdf70 !important;
    text-align: center;
    font-weight: 900;
}

/* 見出し：白 */
h2, h3 {
    color: #ffffff !important;
}

/* 本文：白 */
.stApp p,
.stApp label {
    color: #ffffff !important;
}

/* ボタン：濃い赤系ではなく、濃い金色系 */
.stButton > button {
    width: 100%;
    min-height: 54px;
    border-radius: 12px;
    border: 2px solid #ffdf70;
    background-color: #b8860b;
    color: #ffffff !important;
    font-size: 18px;
    font-weight: 800;
}

/* マウスを乗せたとき */
.stButton > button:hover {
    background-color: #e0a800;
    color: #000000 !important;
    border-color: #fff0a0;
}

/* カードの数字などの文字 */
.stMarkdown {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)
