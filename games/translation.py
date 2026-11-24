"""Translation factory game."""

import streamlit as st

from models.translation import CODON_TABLE, anticodon_for, answer_choices, shuffled_codons


def _start() -> None:
    codons = shuffled_codons()
    st.session_state.translation_codons = codons
    st.session_state.translation_choices = {
        codon: answer_choices(codon) for codon in codons
    }
    st.session_state.translation_index = 0
    st.session_state.translation_score = 0
    st.session_state.translation_correct = 0
    st.session_state.translation_answered = False
    st.session_state.translation_selected = None


def _result(codon: str, selected: str) -> None:
    correct = anticodon_for(codon)
    amino_acid = CODON_TABLE[codon]
    if selected == correct:
        st.success(f"正解！ {codon} は {amino_acid} を指定します。")
    else:
        st.error("不正解です。")
        st.info(f"正しいアンチコドンは 3'-{correct}-5'、アミノ酸は {amino_acid} です。")


def render() -> None:
    """Render the translation factory game."""
    if "translation_codons" not in st.session_state:
        _start()

    codons = st.session_state.translation_codons
    index = st.session_state.translation_index
    st.header("翻訳工場：タンパク質を完成させろ！")

    if index >= len(codons):
        correct = st.session_state.translation_correct
        st.success("翻訳完了！")
        st.metric("最終スコア", f"{st.session_state.translation_score} 点")
        st.write(f"正解数: **{correct} / {len(codons)}**")
        st.write(f"正答率: **{correct / len(codons) * 100:.1f}%**")
        if st.button("翻訳工場をもう一度遊ぶ", key="translation_restart"):
            _start()
            st.rerun()
        return

    score_col, correct_col = st.columns(2)
    score_col.metric("スコア", f"{st.session_state.translation_score} 点")
    correct_col.metric("正解数", f"{st.session_state.translation_correct} / {len(codons)}")
    st.progress(index / len(codons))
    st.write(f"問題 {index + 1} / {len(codons)}")

    codon = codons[index]
    st.subheader("このコドンに対応するアンチコドンは？")
    st.markdown(
        f"<div style='text-align:center; font-size:2.8rem; font-weight:700'>"
        f"5'-{codon}-3'</div>",
        unsafe_allow_html=True,
    )
    st.caption("アンチコドンは3'→5'の向きです。")

    if not st.session_state.translation_answered:
        selected = st.radio(
            "tRNAを選択してください",
            st.session_state.translation_choices[codon],
            format_func=lambda value: f"3'-{value}-5'",
            key=f"translation_answer_{index}",
        )
        if st.button("回答する", type="primary", key="translation_submit"):
            st.session_state.translation_selected = selected
            st.session_state.translation_answered = True
            if selected == anticodon_for(codon):
                st.session_state.translation_score += 10
                st.session_state.translation_correct += 1
            st.rerun()
    else:
        _result(codon, st.session_state.translation_selected)
        label = "次の問題へ" if index + 1 < len(codons) else "結果を見る"
        if st.button(label, type="primary", key="translation_next"):
            st.session_state.translation_index += 1
            st.session_state.translation_answered = False
            st.session_state.translation_selected = None
            st.rerun()
