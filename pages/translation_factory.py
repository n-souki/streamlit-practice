import sys
from pathlib import Path

import streamlit as st

# Allow both `streamlit run` and direct execution of this page file.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.translation import CODON_TABLE, anticodon_for, answer_choices, shuffled_codons
from ui.nexus import apply_theme, header

TITLE = "翻訳工場：タンパク質を完成させろ！"


def start_game() -> None:
    """Initialize a new shuffled game."""
    codons = shuffled_codons()
    st.session_state.codons = codons
    st.session_state.choices = {codon: answer_choices(codon) for codon in codons}
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.answer_submitted = False
    st.session_state.selected_answer = None


def show_result(codon: str, selected: str) -> None:
    """Display feedback for the submitted answer."""
    correct_anticodon = anticodon_for(codon)
    amino_acid = CODON_TABLE[codon]

    if selected == correct_anticodon:
        st.markdown(
            f"<div style='background:#edf8ef; border:1px solid #8fd19a; "
            f"border-radius:10px; padding:.75rem 1rem; color:#17212b;'>"
            f"<strong style='color:#17212b;'>正解！ {codon} は {amino_acid} を指定します。</strong>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.error("不正解です。")
        st.info(
            f"正しいアンチコドンは 3'-{correct_anticodon}-5'、"
            f"アミノ酸は {amino_acid} です。"
        )


def show_finished_game() -> None:
    """Display the final score and restart control."""
    total = len(st.session_state.codons)
    correct = st.session_state.correct_count
    rate = correct / total * 100

    st.balloons()
    st.header("翻訳完了！")
    st.metric("最終スコア", f"{st.session_state.score} 点")
    st.write(f"正解数: **{correct} / {total}**")
    st.write(f"正答率: **{rate:.1f}%**")

    if st.button("もう一度遊ぶ", type="primary", use_container_width=True):
        start_game()
        st.rerun()


st.set_page_config(page_title=TITLE, page_icon="🧬", layout="centered")
apply_theme()
header("BIOCHEMISTRY / TRANSLATION FACTORY")
st.title(TITLE)
st.caption("mRNAのコドンを読み取り、対応するtRNAのアンチコドンを選びましょう。")

if "codons" not in st.session_state:
    start_game()

total_questions = len(st.session_state.codons)
question_index = st.session_state.question_index

if question_index >= total_questions:
    show_finished_game()
    st.stop()

score_col, correct_col = st.columns(2)
score_col.metric("スコア", f"{st.session_state.score} 点")
correct_col.metric(
    "正解数",
    f"{st.session_state.correct_count} / {total_questions}",
)
st.progress(question_index / total_questions)
st.write(f"問題 {question_index + 1} / {total_questions}")

codon = st.session_state.codons[question_index]
st.subheader("このコドンに対応するアンチコドンは？")
st.markdown(
    f"<div style='text-align:center; font-size:2.8rem; font-weight:700; "
    f"letter-spacing:.18em; margin:1rem 0; color:#17212b; "
    f"background:#eef3f7; border-radius:10px; padding:.5rem'>"
    f"5'-{codon}-3'</div>",
    unsafe_allow_html=True,
)
st.caption("アンチコドンは 3' → 5' の向きで表示されます。")

if not st.session_state.answer_submitted:
    selected = st.radio(
        "tRNAを選択してください",
        st.session_state.choices[codon],
        format_func=lambda value: f"3'-{value}-5'",
        key=f"answer_{question_index}",
    )
    if st.button("回答する", type="primary", use_container_width=True):
        st.session_state.selected_answer = selected
        st.session_state.answer_submitted = True
        if selected == anticodon_for(codon):
            st.session_state.score += 10
            st.session_state.correct_count += 1
        st.rerun()
else:
    show_result(codon, st.session_state.selected_answer)
    if st.button(
        "次の問題へ" if question_index + 1 < total_questions else "結果を見る",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.question_index += 1
        st.session_state.answer_submitted = False
        st.session_state.selected_answer = None
        st.rerun()