"""Material-balance engine for CELL SURVIVAL.

The model is intentionally abstract for learning. It separates cytosolic
glycolysis/fermentation from mitochondrial TCA and oxidative phosphorylation.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace


@dataclass(frozen=True)
class CellResources:
    atp: int = 0
    adp: int = 0
    nadh: int = 0
    nad: int = 0
    nadph: int = 0
    nadp: int = 0
    fadh2: int = 0
    fad: int = 0
    glucose: int = 0
    glucose6p: int = 0
    pyruvate: int = 0
    acetyl_coa: int = 0
    citrate: int = 0
    fatty_acid: int = 0
    oxygen: int = 0
    amino_acid: int = 0
    ribose5p: int = 0
    reduced_glutathione: int = 0
    oxidized_glutathione: int = 0
    lactate: int = 0


@dataclass(frozen=True)
class CellPathway:
    name: str
    compartment: str
    description: str
    requirements: dict[str, int]
    changes: dict[str, int]


PATHWAYS = {
    "glycolysis": CellPathway(
        "解糖系",
        "細胞質",
        "グルコースをピルビン酸へ分解し、基質レベルのATPとNADHを得ます。",
        {"glucose": 1, "nad": 2, "adp": 2},
        {"glucose": -1, "pyruvate": 2, "nad": -2, "nadh": 2, "adp": -2, "atp": 2},
    ),
    "fermentation": CellPathway(
        "乳酸発酵",
        "細胞質",
        "ピルビン酸を乳酸へ還元し、NAD+を再生します。ATPは産生しません。",
        {"pyruvate": 1, "nadh": 1},
        {"pyruvate": -1, "nadh": -1, "nad": 1, "lactate": 1},
    ),
    "tca": CellPathway(
        "TCA回路",
        "ミトコンドリア",
        "アセチルCoAを酸化し、NADH・FADH2・GTPを得ます。",
        {"acetyl_coa": 1, "nad": 3, "fad": 1, "adp": 1},
        {"acetyl_coa": -1, "nad": -3, "nadh": 3, "fad": -1, "fadh2": 1, "citrate": 1, "atp": 1, "adp": -1},
    ),
    "etc": CellPathway(
        "電子伝達系・酸化的リン酸化",
        "ミトコンドリア",
        "NADHとFADH2を酸化し、酸素を使ってATPを合成します。",
        {"nadh": 2, "oxygen": 1, "adp": 3},
        {"nadh": -2, "nad": 2, "oxygen": -1, "adp": -3, "atp": 3},
    ),
}


def can_run(resources: CellResources, pathway: CellPathway) -> bool:
    return all(
        getattr(resources, name) >= amount
        for name, amount in pathway.requirements.items()
    )


def run_pathway(resources: CellResources, pathway_key: str) -> CellResources:
    """Apply one pathway without allowing an invalid or negative balance."""
    if pathway_key not in PATHWAYS:
        raise ValueError(f"未知の代謝経路です: {pathway_key}")
    pathway = PATHWAYS[pathway_key]
    if not can_run(resources, pathway):
        raise ValueError(f"必要な資源が不足しています: {pathway.name}")

    updated = resources
    for name, change in pathway.changes.items():
        updated = replace(updated, **{name: getattr(updated, name) + change})
    if any(getattr(updated, field.name) < 0 for field in fields(updated)):
        raise ValueError("物質量が負になる反応は実行できません")
    return updated


def finish_turn(resources: CellResources) -> CellResources:
    """Apply abstract basal ATP demand and nutrient/oxygen supply."""
    return replace(
        resources,
        atp=max(0, resources.atp - 1),
        glucose=resources.glucose + 1,
        oxygen=resources.oxygen + 1,
    )


def health(resources: CellResources) -> tuple[str, list[str]]:
    """Return a coarse health label and the active failure pressures."""
    pressures = []
    if resources.atp == 0:
        pressures.append("ATP不足")
    if resources.nad == 0:
        pressures.append("NAD+不足")
    if resources.oxygen == 0:
        pressures.append("酸素不足")
    if resources.lactate >= 3:
        pressures.append("乳酸蓄積")
    if pressures:
        return "要注意", pressures
    return "安定", pressures
