import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.highlow import calculate_payout, draw_cards, judge, win_probability
from ui.nexus import apply_theme, header

MODES = ("CLASSIC", "SURVIVAL", "CHALLENGE")
MODE_LABELS = {
    "CLASSIC": "クラシック",
    "SURVIVAL": "サバイバル",
    "CHALLENGE": "チャレンジ",
}
MISSIONS = (
    "10ターン以内に5連勝する",
    "1000ポイントを獲得する",
    "Highを3回選ぶ",
)


def _new_round() -> None:
    st.session_state.base_card, st.session_state.result_card = draw_cards()
    st.session_state.choice = None
    st.session_state.highlow_round_resolved = False


def _start(mode: str = "CLASSIC") -> None:
    st.session_state.highlow_mode = mode
    st.session_state.highlow_points = (
        st.session_state.get("highlow_initial_points", 1000)
    )
    st.session_state.highlow_streak = 0
    st.session_state.highlow_best_streak = st.session_state.get(
        "highlow_best_streak", 0
    )
    st.session_state.highlow_turns = 0
    st.session_state.highlow_high_choices = 0
    st.session_state.highlow_mission = st.session_state.get(
        "highlow_mission_selector", MISSIONS[0]
    )
    st.session_state.highlow_ability_used = False
    st.session_state.highlow_insurance = False
    st.session_state.highlow_message = ""
    _new_round()


def _ensure_state() -> None:
    if "highlow_mode" not in st.session_state:
        _start()


def _achievement_rows() -> list[tuple[str, bool]]:
    return [
        ("初勝利", st.session_state.highlow_best_streak >= 1),
        ("3連勝", st.session_state.highlow_best_streak >= 3),
        ("5連勝", st.session_state.highlow_best_streak >= 5),
        ("1000ポイント達成", st.session_state.highlow_points >= 1000),
    ]


def _mission_complete() -> bool:
    mission = st.session_state.highlow_mission
    if mission.startswith("10ターン"):
        return (
            st.session_state.highlow_turns <= 10
            and st.session_state.highlow_best_streak >= 5
        )
    if mission.startswith("1000"):
        return st.session_state.highlow_points >= 1000
    return st.session_state.highlow_high_choices >= 3


def _show_settings() -> None:
    mode = st.selectbox(
        "ゲームモード",
        MODES,
        format_func=lambda value: MODE_LABELS[value],
        key="highlow_mode_selector",
    )
    if mode == "SURVIVAL":
        st.number_input(
            "サバイバル初期ポイント",
            min_value=100,
            max_value=10000,
            value=1000,
            step=100,
            key="highlow_initial_points",
        )
    elif mode == "CHALLENGE":
        st.selectbox("ミッション", MISSIONS, key="highlow_mission_selector")
    if st.button("このモードで開始", type="primary", key="highlow_start"):
        _start(mode)
        st.rerun()


def _resolve_round(bet: int) -> None:
    base_card = st.session_state.base_card
    result_card = st.session_state.result_card
    choice = st.session_state.choice
    result = judge(base_card["rank"], result_card["rank"], choice)

    if result == "win":
        st.session_state.highlow_streak += 1
        st.session_state.highlow_message = f"正解！ +{bet}ポイント"
    elif result == "lose":
        if st.session_state.highlow_insurance:
            st.session_state.highlow_insurance = False
            st.session_state.highlow_message = "不正解ですが、保険能力でポイント減少を防ぎました。"
        else:
            st.session_state.highlow_points = max(
                0,
                st.session_state.highlow_points - bet,
            )
            st.session_state.highlow_message = f"残念！ -{bet}ポイント"
        st.session_state.highlow_streak = 0
    else:
        st.session_state.highlow_message = "引き分け！ポイント変動なし。"

    if result == "win":
        st.session_state.highlow_points += calculate_payout(
            st.session_state.highlow_points,
            bet,
            result,
        )
    st.session_state.highlow_turns += 1
    st.session_state.highlow_best_streak = max(
        st.session_state.highlow_best_streak,
        st.session_state.highlow_streak,
    )
    st.session_state.highlow_round_resolved = True


def render() -> None:
    """Render the High & Low game with modes, abilities, and achievements."""
    apply_theme()
    _ensure_state()
    header("ハイ＆ロー", st.session_state.highlow_points)
    st.title("ハイ＆ローゲーム")
    st.write("**ハイ＆ロー**ゲームへようこそ！")
    st.caption(f"モード: **{MODE_LABELS[st.session_state.highlow_mode]}**")

    with st.expander("ゲームモードを変更する"):
        _show_settings()

    if st.session_state.highlow_mode == "SURVIVAL":
        st.metric("現在の連勝", st.session_state.highlow_streak)
        st.metric("最高連勝", st.session_state.highlow_best_streak)
    elif st.session_state.highlow_mode == "CHALLENGE":
        st.info(f"ミッション: {st.session_state.highlow_mission}")
        st.write(
            f"ターン: {st.session_state.highlow_turns} / 10、"
            f"High選択: {st.session_state.highlow_high_choices} / 3"
        )

    points_col, bet_col, probability_col = st.columns(3)
    points_col.metric("ポイント", st.session_state.highlow_points)
    bet = bet_col.number_input(
        "賭けポイント",
        min_value=1,
        max_value=max(1, st.session_state.highlow_points),
        value=min(100, max(1, st.session_state.highlow_points)),
        step=10,
        disabled=st.session_state.highlow_points <= 0,
        key=f"highlow_bet_{st.session_state.highlow_turns}",
    )
    base_card = st.session_state.base_card
    choice_for_probability = "High" if base_card["rank"] < 7 else "Low"
    probability_col.metric(
        f"{'ハイ' if choice_for_probability == 'High' else 'ロー'}勝率",
        f"{win_probability(base_card['rank'], choice_for_probability):.0%}",
    )

    if st.session_state.highlow_points <= 0:
        st.error("ポイントが0になったためゲーム終了です。")
        if st.button("もう一度遊ぶ", key="highlow_game_over_restart"):
            _start(st.session_state.highlow_mode)
            st.rerun()
        return

    st.write("**最初のカード**")
    st.header(f"{base_card['suit']} {base_card['rank']}")

    if not st.session_state.highlow_round_resolved:
        st.subheader("特殊能力")
        ability_col, insurance_col = st.columns(2)
        if ability_col.button(
            "カード交換（1回）",
            disabled=st.session_state.highlow_ability_used,
            key="highlow_swap",
        ):
            st.session_state.result_card = draw_cards()[1]
            st.session_state.highlow_ability_used = True
            st.rerun()
        if insurance_col.button(
            "保険（次の敗北を無効化）",
            disabled=st.session_state.highlow_insurance,
            key="highlow_insurance",
        ):
            st.session_state.highlow_insurance = True
            st.rerun()
        if st.session_state.highlow_insurance:
            st.caption("保険が有効です。次に負けても賭けポイントは減りません。")

        high_col, low_col = st.columns(2)
        if high_col.button("ハイ", use_container_width=True, key="highlow_high"):
            st.session_state.choice = "High"
            st.session_state.highlow_high_choices += 1
            _resolve_round(int(bet))
            st.rerun()
        if low_col.button("ロー", use_container_width=True, key="highlow_low"):
            st.session_state.choice = "Low"
            _resolve_round(int(bet))
            st.rerun()
        return

    result_card = st.session_state.result_card
    st.write("**次のカード**")
    st.header(f"{result_card['suit']} {result_card['rank']}")
    result = judge(
        base_card["rank"],
        result_card["rank"],
        st.session_state.choice,
    )
    if result == "win":
        st.success(st.session_state.highlow_message)
    elif result == "lose":
        st.error(st.session_state.highlow_message)
    else:
        st.info(st.session_state.highlow_message)

    if st.session_state.highlow_mode == "CHALLENGE" and _mission_complete():
        st.success("ミッション達成！")

    if st.button("次のカード", type="primary", key="highlow_next"):
        if (
            st.session_state.highlow_mode == "SURVIVAL"
            and result == "lose"
        ):
            st.warning("不正解のためサバイバル挑戦終了です。")
        _new_round()
        st.rerun()

    st.subheader("実績")
    for name, achieved in _achievement_rows():
        st.write(f"{'✅' if achieved else '⬜'} {name}")
