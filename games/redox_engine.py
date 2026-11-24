"""Material-balance model for REDOX MASTER.

This is an educational, deliberately simplified model. It is not a
quantitative representation of a real cell.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from typing import Callable


@dataclass(frozen=True)
class Resources:
    nadh: int = 0
    nad: int = 0
    nadph: int = 0
    nadp: int = 0
    atp: int = 0
    adp: int = 0
    glucose: int = 0
    pyruvate: int = 0
    acetyl_coa: int = 0
    oxygen: int = 0
    fadh2: int = 0
    gtp: int = 0
    ribose5p: int = 0
    fatty_acid: int = 0
    ros: int = 0
    glutathione: int = 0


@dataclass(frozen=True)
class Pathway:
    name: str
    description: str
    requirements: dict[str, int]
    changes: dict[str, int]


PATHWAYS = {
    "glycolysis": Pathway(
        "解糖系",
        "グルコースを分解し、ATP・NADH・ピルビン酸を得る（細胞質）。",
        {"glucose": 1, "nad": 2, "adp": 2},
        {"glucose": -1, "nad": -2, "nadh": 2, "adp": -2, "atp": 2, "pyruvate": 2},
    ),
    "ppp": Pathway(
        "ペントースリン酸経路",
        "グルコースからNADPHとリボース5-リン酸を得る（細胞質）。",
        {"glucose": 1, "nadp": 2},
        {"glucose": -1, "nadp": -2, "nadph": 2, "ribose5p": 1},
    ),
    "tca": Pathway(
        "TCA回路",
        "アセチルCoAを酸化し、還元当量とGTPを得る（ミトコンドリア）。",
        {"acetyl_coa": 1, "nad": 3},
        {"acetyl_coa": -1, "nad": -3, "nadh": 3, "fadh2": 1, "gtp": 1},
    ),
    "etc": Pathway(
        "電子伝達系・酸化的リン酸化",
        "NADHを酸化し、酸素を最終電子受容体としてATPを得る。",
        {"nadh": 2, "oxygen": 1, "adp": 3},
        {"nadh": -2, "oxygen": -1, "nad": 2, "adp": -3, "atp": 3},
    ),
    "fatty_acid_synthesis": Pathway(
        "脂肪酸合成",
        "アセチルCoA、ATP、NADPHを使って脂肪酸を合成する。",
        {"acetyl_coa": 1, "atp": 2, "nadph": 2},
        {"acetyl_coa": -1, "atp": -2, "nadph": -2, "nadp": 2, "fatty_acid": 1},
    ),
    "antioxidant": Pathway(
        "抗酸化システム",
        "NADPHを使って還元型グルタチオンを再生し、ROSを除去する。",
        {"nadph": 1, "ros": 1},
        {"nadph": -1, "nadp": 1, "ros": -1, "glutathione": 1},
    ),
    "fermentation": Pathway(
        "乳酸発酵",
        "ピルビン酸を還元し、NAD+を再生する。酸素不足時の補助経路。",
        {"pyruvate": 1, "nadh": 1},
        {"pyruvate": -1, "nadh": -1, "nad": 1},
    ),
}


def available(resources: Resources, pathway: Pathway) -> bool:
    """Return whether every substrate and cofactor is available."""
    return all(getattr(resources, name) >= amount for name, amount in pathway.requirements.items())


def apply_pathway(resources: Resources, pathway_key: str) -> Resources:
    """Apply one pathway and reject insufficient resources or negative balances."""
    try:
        pathway = PATHWAYS[pathway_key]
    except KeyError as error:
        raise ValueError(f"未知の代謝経路です: {pathway_key}") from error
    if not available(resources, pathway):
        raise ValueError(f"必要な資源が不足しています: {pathway.name}")

    updated = resources
    for name, change in pathway.changes.items():
        updated = replace(updated, **{name: getattr(updated, name) + change})
    if any(getattr(updated, field.name) < 0 for field in fields(updated)):
        raise ValueError("物質量が負になる反応は実行できません")
    return updated


def ratio(reduced: int, oxidized: int) -> float:
    """Return a display-only reduced/oxidized ratio."""
    if oxidized == 0:
        return float("inf") if reduced else 0.0
    return reduced / oxidized


def resource_dict(resources: Resources) -> dict[str, int]:
    """Convert resources to a chart-friendly dictionary."""
    return {field.name: getattr(resources, field.name) for field in fields(resources)}
