"""Data and pure functions for the translation game."""

from __future__ import annotations

import random

BASE_COMPLEMENTS = str.maketrans({"A": "U", "U": "A", "G": "C", "C": "G"})

CODON_TABLE: dict[str, str] = {
    "UUU": "フェニルアラニン", "UUC": "フェニルアラニン",
    "UUA": "ロイシン", "UUG": "ロイシン",
    "UCU": "セリン", "UCC": "セリン", "UCA": "セリン", "UCG": "セリン",
    "UAU": "チロシン", "UAC": "チロシン",
    "UGU": "システイン", "UGC": "システイン",
    "UGG": "トリプトファン",
    "CUU": "ロイシン", "CUC": "ロイシン", "CUA": "ロイシン", "CUG": "ロイシン",
    "CCU": "プロリン", "CCC": "プロリン", "CCA": "プロリン", "CCG": "プロリン",
    "CAU": "ヒスチジン", "CAC": "ヒスチジン",
    "CAA": "グルタミン", "CAG": "グルタミン",
    "CGU": "アルギニン", "CGC": "アルギニン", "CGA": "アルギニン", "CGG": "アルギニン",
    "AUU": "イソロイシン", "AUC": "イソロイシン", "AUA": "イソロイシン",
    "AUG": "メチオニン",
    "ACU": "スレオニン", "ACC": "スレオニン", "ACA": "スレオニン", "ACG": "スレオニン",
    "AAU": "アスパラギン", "AAC": "アスパラギン",
    "AAA": "リシン", "AAG": "リシン",
    "AGU": "セリン", "AGC": "セリン",
    "AGA": "アルギニン", "AGG": "アルギニン",
    "GUU": "バリン", "GUC": "バリン", "GUA": "バリン", "GUG": "バリン",
    "GCU": "アラニン", "GCC": "アラニン", "GCA": "アラニン", "GCG": "アラニン",
    "GAU": "アスパラギン酸", "GAC": "アスパラギン酸",
    "GAA": "グルタミン酸", "GAG": "グルタミン酸",
    "GGU": "グリシン", "GGC": "グリシン", "GGA": "グリシン", "GGG": "グリシン",
}


def anticodon_for(codon: str) -> str:
    """Return the complementary anticodon written 3' to 5'."""
    normalized = codon.upper()
    if normalized not in CODON_TABLE:
        raise ValueError(f"アミノ酸を指定できないコドンです: {codon}")
    return normalized.translate(BASE_COMPLEMENTS)


def shuffled_codons(rng: random.Random | None = None) -> list[str]:
    """Return every amino-acid codon once, with AUG as the first question."""
    generator = rng or random
    remaining = [codon for codon in CODON_TABLE if codon != "AUG"]
    generator.shuffle(remaining)
    return ["AUG", *remaining]


def answer_choices(codon: str, rng: random.Random | None = None) -> list[str]:
    """Return four distinct anticodon choices, including the correct one."""
    correct = anticodon_for(codon)
    generator = rng or random
    distractors = {
        anticodon_for(candidate)
        for candidate in CODON_TABLE
        if candidate != codon
    }
    choices = generator.sample(list(distractors), 3)
    choices.append(correct)
    generator.shuffle(choices)
    return choices
