"""CELL SURVIVAL: cell metabolism simulation."""

import streamlit as st

from games.survival_engine import (
    PATHWAYS,
    CellResources,
    finish_turn,
    health,
    run_pathway,
)

MAX_TURNS = 10
INITIAL_RESOURCES = CellResources(
    atp=5,
    adp=12,
    nad=8,
    glucose=3,
    acetyl_coa=2,
    fad=2,
    oxygen=2,
)
DISPLAY_NAMES = {
    "atp": "ATP",
    "adp": "ADP",
    "nadh": "NADH",
    "nad": "NAD+",
    "nadph": "NADPH",
    "nadp": "NADP+",
    "fadh2": "FADH₂",
    "fad": "FAD",
    "glucose": "グルコース",
    "glucose6p": "グルコース6-リン酸",
    "pyruvate": "ピルビン酸",
    "acetyl_coa": "アセチルCoA",
    "citrate": "クエン酸",
    "fatty_acid": "脂肪酸",
    "oxygen": "酸素",
    "amino_acid": "アミノ酸",
    "ribose5p": "リボース5-リン酸",
    "reduced_glutathione": "還元型グルタチオン",
    "oxidized_glutathione": "酸化型グルタチオン",
    "lactate": "乳酸",
}


def _start() -> None:
    st.session_state.survival_resources = INITIAL_RESOURCES
    st.session_state.survival_turn = 0
    st.session_state.survival_history = []
    st.session_state.survival_snapshots = [vars(INITIAL_RESOURCES)]
    st.session_state.survival_message = ""


def _resource_rows(resources: CellResources) -> list[dict[str, int | str]]:
    return [
        {"物質": DISPLAY_NAMES[name], "量": getattr(resources, name)}
        for name in vars(resources)
    ]


def render() -> None:
    """Render the phase-one cell survival simulation."""
    if "survival_resources" not in st.session_state:
        _start()

    resources = st.session_state.survival_resources
    turn = st.session_state.survival_turn
    status, pressures = health(resources)

    st.header("CELL SURVIVAL：細胞代謝シミュレーション")
    st.caption("教育用の抽象モデルです。細胞質とミトコンドリアの区画を簡略化して表現します。")
    st.write(f"ターン: **{turn} / {MAX_TURNS}**　細胞状態: **{status}**")
    if pressures:
        st.warning("、".join(pressures))
    if st.session_state.survival_message:
        st.info(st.session_state.survival_message)

    metric_cols = st.columns(6)
    for column, name in zip(
        metric_cols, ("atp", "nadh", "nad", "glucose", "pyruvate", "oxygen")
    ):
        column.metric(DISPLAY_NAMES[name], getattr(resources, name))
    st.dataframe(_resource_rows(resources), hide_index=True, use_container_width=True)

    if turn >= MAX_TURNS:
        if status == "安定":
            st.success("細胞を維持しました！")
        else:
            st.error("細胞の状態が悪化しました。")
        if st.button("細胞サバイバルをもう一度遊ぶ", key="survival_restart"):
            _start()
            st.rerun()
        return

    st.subheader("代謝経路を1つ選択")
    selected = st.selectbox(
        "実行する経路",
        list(PATHWAYS),
        format_func=lambda key: (
            f"{PATHWAYS[key].name}（{PATHWAYS[key].compartment}）"
        ),
        key=f"survival_pathway_{turn}",
    )
    pathway = PATHWAYS[selected]
    st.write(pathway.description)
    st.caption(
        "必要: "
        + "、".join(
            f"{DISPLAY_NAMES[name]} {amount}"
            for name, amount in pathway.requirements.items()
        )
    )
    if st.button("経路を実行してターン終了", type="primary", key="survival_execute"):
        try:
            updated = finish_turn(run_pathway(resources, selected))
        except ValueError as error:
            st.error(str(error))
        else:
            st.session_state.survival_resources = updated
            st.session_state.survival_turn += 1
            st.session_state.survival_history.append(pathway.name)
            st.session_state.survival_snapshots.append(vars(updated))
            st.session_state.survival_message = (
                f"{pathway.name}を実行しました。ターン終了時にATPを1消費し、"
                "グルコースと酸素が供給されます。"
            )
            st.rerun()

    st.subheader("代謝履歴")
    for number, name in enumerate(st.session_state.survival_history, 1):
        st.write(f"{number}. {name}")
    if st.session_state.survival_snapshots:
        st.line_chart(
            st.session_state.survival_snapshots,
            y=("atp", "nadh", "nad", "oxygen"),
        )
