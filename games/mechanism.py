"""ENZYME LAB: PDH reaction-mechanism learning game."""

import streamlit as st

from games.mechanism_data import (
    ELECTRON_CHALLENGES,
    INTERMEDIATES,
    PDH_STEPS,
    RESEARCH_CHALLENGES,
)

MODES = (
    "モード1：反応経路構築",
    "モード2：電子移動チャレンジ",
    "モード3：中間体鑑定",
    "モード4：研究者チャレンジ",
)


def _reset() -> None:
    st.session_state.mechanism_score = 0
    st.session_state.mechanism_mistakes = 0
    st.session_state.mechanism_hints = 0
    st.session_state.mechanism_review = []
    st.session_state.mechanism_review_counts = {}
    st.session_state.mechanism_history = []
    st.session_state.mechanism_correct = 0
    st.session_state.mechanism_attempts = 0
    st.session_state.mechanism_streak = 0
    st.session_state.mechanism_best_streak = 0
    st.session_state.mechanism_mode_index = 0
    st.session_state.mechanism_submitted = False
    st.session_state.mechanism_finished = False
    st.session_state.mechanism_answered = {}


def _add_review(topic: str) -> None:
    if topic not in st.session_state.mechanism_review:
        st.session_state.mechanism_review.append(topic)
    counts = st.session_state.mechanism_review_counts
    counts[topic] = counts.get(topic, 0) + 1


def _record_answer(
    *,
    correct: bool,
    topic: str,
    difficulty: str,
    prompt: str,
    answer: str,
) -> int:
    st.session_state.mechanism_attempts += 1
    if correct:
        st.session_state.mechanism_correct += 1
        st.session_state.mechanism_streak += 1
        st.session_state.mechanism_best_streak = max(
            st.session_state.mechanism_best_streak,
            st.session_state.mechanism_streak,
        )
        points = {"基礎": 10, "標準": 15, "応用": 20, "発展": 25}.get(difficulty, 15)
        points += min(st.session_state.mechanism_streak - 1, 5) * 2
        st.session_state.mechanism_score += points
    else:
        st.session_state.mechanism_mistakes += 1
        st.session_state.mechanism_streak = 0
        points = 0
        _add_review(topic)

    st.session_state.mechanism_history.append(
        {
            "問題": prompt,
            "分野": topic,
            "難易度": difficulty,
            "判定": "正解" if correct else "不正解",
            "獲得": points,
            "正解数": st.session_state.mechanism_correct,
            "連続正解": st.session_state.mechanism_streak,
        }
    )
    return points


def _accuracy() -> float:
    attempts = st.session_state.mechanism_attempts
    if attempts == 0:
        return 0.0
    return st.session_state.mechanism_correct / attempts * 100


def _title() -> str:
    streak = st.session_state.mechanism_best_streak
    accuracy = _accuracy()
    attempts = st.session_state.mechanism_attempts
    if attempts >= 10 and accuracy >= 80:
        return "反応機構解析官"
    if streak >= 5:
        return "酵素反応マイスター"
    if streak >= 3:
        return "継続観察員"
    if attempts >= 1:
        return "見習い研究員"
    return "見習い研究員"


def _next_button(state_key: str, index: int, label: str = "次の問題へ") -> None:
    if st.button(label, type="primary", key=f"{state_key}_next_{index}"):
        st.session_state[state_key] += 1
        st.session_state.mechanism_answered.pop(f"{state_key}:{index}", None)
        st.rerun()


def _mode1() -> None:
    st.subheader("反応経路構築")
    st.caption("難易度：応用　配点：最大25点＋連続正解ボーナス")
    st.info("PDH複合体の反応段階を、起こる順番に選択してください。")
    order = st.multiselect(
        "起こる順に選択",
        [step.key for step in PDH_STEPS],
        format_func=lambda key: next(step.title for step in PDH_STEPS if step.key == key),
        key="mechanism_order_selection",
    )
    answer_id = "mechanism_order"
    already_answered = answer_id in st.session_state.mechanism_answered
    if st.button(
        "経路を判定",
        type="primary",
        key="mechanism_order_submit",
        disabled=already_answered,
    ):
        expected = [step.key for step in PDH_STEPS]
        correct = order == expected
        points = _record_answer(
            correct=correct,
            topic="反応経路の順番",
            difficulty="応用",
            prompt="PDH複合体の反応経路を正しい順番に並べる",
            answer=" → ".join(step.title for step in PDH_STEPS),
        )
        st.session_state.mechanism_answered[answer_id] = {
            "correct": correct,
            "points": points,
        }
        st.session_state.mechanism_submitted = True
    result = st.session_state.mechanism_answered.get(answer_id)
    if result:
        if result["correct"]:
            st.success(f"正解！ +{result['points']}点")
        else:
            st.error("順番が違います。正しい経路は次のとおりです。")
    if st.session_state.mechanism_submitted:
        for number, step in enumerate(PDH_STEPS, 1):
            st.write(f"{number}. **{step.title}** — {step.description}（{step.event}）")
        st.info(
            "TPPはピルビン酸の脱炭酸を担い、リポアミドはアセチル基と還元当量を段階的に運びます。"
            " E1・E2・E3の協調により、中間生成物を酵素間で直接移すことで副反応を抑えています。"
        )
    if st.session_state.mechanism_submitted:
        if st.button("経路をもう一度練習", key="mechanism_order_reset"):
            st.session_state.mechanism_submitted = False
            st.session_state.mechanism_answered.pop(answer_id, None)
            st.session_state.mechanism_order_selection = []
            st.rerun()


def _choice_mode(
    title: str,
    questions: tuple[dict, ...],
    state_key: str,
    review_topic: str,
) -> None:
    index = st.session_state[state_key]
    if index >= len(questions):
        st.success(f"{title} 完了")
        return
    question = questions[index]
    st.subheader(title)
    difficulty = question.get("difficulty", "標準")
    st.caption(f"問題 {index + 1} / {len(questions)}　|　難易度：{difficulty}")
    st.progress((index + 1) / len(questions))
    st.markdown(f"### {question['prompt']}")
    choice = st.radio("選択肢", question["choices"], key=f"{state_key}_choice_{index}")
    answer_id = f"{state_key}:{index}"
    result = st.session_state.mechanism_answered.get(answer_id)
    if st.button(
        "回答する",
        type="primary",
        key=f"{state_key}_submit_{index}",
        disabled=result is not None,
    ):
        answer_index = question["answer"]
        correct = choice == question["choices"][answer_index]
        points = _record_answer(
            correct=correct,
            topic=review_topic,
            difficulty=difficulty,
            prompt=question["prompt"],
            answer=question["choices"][answer_index],
        )
        st.session_state.mechanism_answered[answer_id] = {
            "correct": correct,
            "points": points,
            "answer": question["choices"][answer_index],
        }
        st.rerun()

    if result:
        if result["correct"]:
            st.success(f"正解！　+{result['points']}点")
        else:
            st.error(f"不正解。正解は「{result['answer']}」です。")
        st.markdown("#### 解説")
        st.info(question["explanation"])
        _next_button(state_key, index)


def _mode3() -> None:
    index = st.session_state.mechanism_intermediate_index
    if index >= len(INTERMEDIATES):
        st.success("中間体鑑定 完了")
        return
    question = INTERMEDIATES[index]
    st.subheader("中間体鑑定")
    st.caption(f"問題 {index + 1} / {len(INTERMEDIATES)}　|　難易度：応用")
    st.progress((index + 1) / len(INTERMEDIATES))
    st.markdown("### 以下の性質を示す中間体はどれですか？")
    st.info(question["clue"])
    answer = st.radio("中間体を選択", question["choices"], key=f"intermediate_choice_{index}")
    answer_id = f"mechanism_intermediate:{index}"
    result = st.session_state.mechanism_answered.get(answer_id)
    if st.button(
        "鑑定する",
        type="primary",
        key=f"intermediate_submit_{index}",
        disabled=result is not None,
    ):
        correct = answer == question["answer"]
        points = _record_answer(
            correct=correct,
            topic="反応中間体",
            difficulty="応用",
            prompt=question["clue"],
            answer=question["answer"],
        )
        st.session_state.mechanism_answered[answer_id] = {
            "correct": correct,
            "points": points,
            "answer": question["answer"],
        }
        st.rerun()

    if result:
        if result["correct"]:
            st.success(f"正解！　+{result['points']}点")
        else:
            st.error(f"不正解。正解は「{result['answer']}」です。")
        st.markdown("#### 解説")
        st.info(
            f"{question['answer']}は、{question['clue']} "
            f"次の変化は「{question['next']}」です。"
        )
        if st.button("次の中間体へ", type="primary", key=f"intermediate_next_{index}"):
            st.session_state.mechanism_intermediate_index += 1
            st.session_state.mechanism_answered.pop(answer_id, None)
            st.rerun()


def render() -> None:
    """Render the ENZYME LAB game."""
    if "mechanism_score" not in st.session_state:
        _reset()
    st.session_state.setdefault("mechanism_electron_index", 0)
    st.session_state.setdefault("mechanism_intermediate_index", 0)
    st.session_state.setdefault("mechanism_research_index", 0)
    st.session_state.setdefault("mechanism_answered", {})
    st.session_state.setdefault("mechanism_history", [])
    st.session_state.setdefault("mechanism_review_counts", {})
    st.session_state.setdefault("mechanism_correct", 0)
    st.session_state.setdefault("mechanism_attempts", 0)
    st.session_state.setdefault("mechanism_streak", 0)
    st.session_state.setdefault("mechanism_best_streak", 0)

    st.header("酵素ラボ：反応機構研究所")
    st.caption("題材：ピルビン酸デヒドロゲナーゼ複合体（PDH）｜反応中心と電子移動を模式的に解析")

    accuracy = _accuracy()
    metric_columns = st.columns(4)
    metric_columns[0].metric("スコア", st.session_state.mechanism_score)
    metric_columns[1].metric("正答率", f"{accuracy:.1f}%")
    metric_columns[2].metric("連続正解", st.session_state.mechanism_streak)
    metric_columns[3].metric("称号", _title())

    mode = st.selectbox("モード", MODES, key="mechanism_mode")

    if mode == MODES[0]:
        _mode1()
    elif mode == MODES[1]:
        _choice_mode(
            "電子移動チャレンジ",
            ELECTRON_CHALLENGES,
            "mechanism_electron_index",
            "電子の移動",
        )
    elif mode == MODES[2]:
        _mode3()
    else:
        _choice_mode(
            "研究者チャレンジ",
            RESEARCH_CHALLENGES,
            "mechanism_research_index",
            "PDH複合体の総合機構",
        )

    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("復習リスト")
        if st.session_state.mechanism_review:
            for topic in st.session_state.mechanism_review:
                count = st.session_state.mechanism_review_counts.get(topic, 1)
                st.write(f"- **{topic}**（誤答 {count}回）")
        else:
            st.caption("まだありません。正解・不正解の記録が復習項目になります。")
    with right:
        st.subheader("実績")
        streak = st.session_state.mechanism_best_streak
        accuracy = _accuracy()
        achievements = (
            ("初回解析", "1問以上回答", st.session_state.mechanism_attempts >= 1),
            ("継続観察員", "3問連続正解", streak >= 3),
            ("反応機構マイスター", "5問連続正解", streak >= 5),
            ("高精度解析官", "10問以上かつ正答率80%以上", st.session_state.mechanism_attempts >= 10 and accuracy >= 80),
        )
        for name, condition, achieved in achievements:
            status = "解除済" if achieved else "未解除"
            st.markdown(f"{'◆' if achieved else '◇'} **{name}**　`{status}`")
            st.caption(condition)

    if st.session_state.mechanism_history:
        st.divider()
        st.subheader("回答履歴")
        st.dataframe(
            st.session_state.mechanism_history[::-1],
            hide_index=True,
            use_container_width=True,
        )

    if st.button("酵素ラボをリセット", key="mechanism_reset"):
        _reset()
        st.session_state.mechanism_electron_index = 0
        st.session_state.mechanism_intermediate_index = 0
        st.session_state.mechanism_research_index = 0
        st.rerun()
