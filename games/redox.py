"""REDOX MASTER: stage 1 strategy simulation."""

import streamlit as st

from games.redox_engine import (
    PATHWAYS,
    Resources,
    apply_pathway,
    ratio,
    resource_dict,
)

STAGE_TURNS = 6
STAGE_GOAL = 15
INITIAL_RESOURCES = Resources(nad=6, atp=5, adp=10, glucose=3, oxygen=2)
DISPLAY_NAMES = {
    "nadh": "NADH",
    "nad": "NAD+",
    "nadph": "NADPH",
    "nadp": "NADP+",
    "atp": "ATP",
    "adp": "ADP",
    "glucose": "グルコース",
    "pyruvate": "ピルビン酸",
    "acetyl_coa": "アセチルCoA",
    "oxygen": "O₂",
    "fadh2": "FADH₂",
    "gtp": "GTP",
    "ribose5p": "リボース5-リン酸",
    "fatty_acid": "脂肪酸",
    "ros": "ROS",
    "glutathione": "還元型グルタチオン",
}


def _start() -> None:
    st.session_state.redox_resources = INITIAL_RESOURCES
    st.session_state.redox_turn = 0
    st.session_state.redox_history = []
    st.session_state.redox_snapshots = [resource_dict(INITIAL_RESOURCES)]
    st.session_state.redox_finished = False


def _rank(resources: Resources, turns: int) -> str:
    if resources.atp < STAGE_GOAL:
        return "C"
    if turns <= 4 and resources.atp >= STAGE_GOAL:
        return "S"
    return "A"


def _show_resources(resources: Resources) -> None:
    cols = st.columns(6)
    for column, key in zip(
        cols,
        ("atp", "nadh", "nadph", "nad", "nadp", "glucose"),
    ):
        column.metric(DISPLAY_NAMES[key], getattr(resources, key))
    st.write(
        f"NADH/NAD+比: **{ratio(resources.nadh, resources.nad):.2f}**　"
        f"NADPH/NADP+比: **{ratio(resources.nadph, resources.nadp):.2f}**"
    )


def _finish(resources: Resources, turns: int) -> None:
    rank = _rank(resources, turns)
    if resources.atp >= STAGE_GOAL:
        st.success(f"STAGE 1クリア！ ランク: **{rank}**")
    else:
        st.error(f"STAGE 1失敗。ランク: **{rank}**")
    st.write(f"最終ATP: **{resources.atp}** / 目標 {STAGE_GOAL}")
    if st.button("STAGE 1をもう一度遊ぶ", key="redox_restart"):
        _start()
        st.rerun()


def render() -> None:
    """Render the REDOX MASTER stage 1."""
    if "redox_resources" not in st.session_state:
        _start()

    st.header("REDOX MASTER：細胞の酸化還元戦略")
    st.caption("教育用の簡略モデルです。実際の細胞内代謝を定量的に再現するものではありません。")
    resources = st.session_state.redox_resources
    turn = st.session_state.redox_turn
    _show_resources(resources)
    st.info("STAGE 1：エネルギー不足 — 解糖系と電子伝達系でATPを15以上にする")
    st.progress(min(turn / STAGE_TURNS, 1.0))
    st.write(f"ターン: **{turn} / {STAGE_TURNS}**　目標ATP: **{STAGE_GOAL}以上**")

    if turn >= STAGE_TURNS or st.session_state.redox_finished:
        _finish(resources, turn)
        return

    st.subheader("代謝経路を1つ選んで実行")
    choices = list(PATHWAYS)
    selected = st.selectbox(
        "経路",
        choices,
        format_func=lambda key: f"{PATHWAYS[key].name} — {PATHWAYS[key].description}",
        key=f"redox_pathway_{turn}",
    )
    pathway = PATHWAYS[selected]
    requirements = "、".join(
        f"{DISPLAY_NAMES[key]} {amount}" for key, amount in pathway.requirements.items()
    )
    st.caption(f"必要条件: {requirements}")
    if st.button("反応を実行", type="primary", key="redox_execute"):
        try:
            updated = apply_pathway(resources, selected)
        except ValueError as error:
            st.error(str(error))
        else:
            st.session_state.redox_resources = updated
            st.session_state.redox_turn += 1
            st.session_state.redox_history.append(PATHWAYS[selected].name)
            st.session_state.redox_snapshots.append(resource_dict(updated))
            if updated.atp >= STAGE_GOAL:
                st.session_state.redox_finished = True
            st.rerun()

    st.subheader("代謝履歴")
    if st.session_state.redox_history:
        for number, name in enumerate(st.session_state.redox_history, 1):
            st.write(f"{number}. {name}")
    else:
        st.caption("まだ反応を実行していません。")
    st.line_chart(st.session_state.redox_snapshots, y=("atp", "nadh", "nadph"))
