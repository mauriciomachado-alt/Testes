#!/usr/bin/env python3
"""Diário interativo com análise simples de personalidade.

Digite seus pensamentos. Use "analisar" para ver o perfil ou "sair" para encerrar.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TraitProfile:
    openness: int
    conscientiousness: int
    extraversion: int
    agreeableness: int
    neuroticism: int

    def as_dict(self) -> Dict[str, int]:
        return {
            "Abertura (Openness)": self.openness,
            "Conscienciosidade": self.conscientiousness,
            "Extroversão": self.extraversion,
            "Amabilidade": self.agreeableness,
            "Neuroticismo": self.neuroticism,
        }


KEYWORDS = {
    "openness": [
        "curioso",
        "imaginar",
        "criativo",
        "novo",
        "novidade",
        "arte",
        "livro",
        "aprender",
        "explorar",
        "ideia",
    ],
    "conscientiousness": [
        "planejar",
        "organizar",
        "meta",
        "responsável",
        "disciplina",
        "rotina",
        "pontual",
        "foco",
        "cumprir",
    ],
    "extraversion": [
        "amigos",
        "festa",
        "social",
        "conversar",
        "energia",
        "grupo",
        "divertido",
        "sair",
        "encontro",
    ],
    "agreeableness": [
        "ajudar",
        "gentil",
        "empatia",
        "compreender",
        "cooperar",
        "carinho",
        "ouvir",
        "solidário",
    ],
    "neuroticism": [
        "ansioso",
        "medo",
        "preocupado",
        "tenso",
        "inseguro",
        "estresse",
        "culpa",
        "triste",
        "irritado",
    ],
}

FOLLOW_UPS = [
    "Quer me contar um pouco mais sobre isso?",
    "Como você se sentiu durante essa situação?",
    "O que foi mais importante para você nesse momento?",
    "Há algo que gostaria de fazer diferente da próxima vez?",
]


def score_entries(entries: List[str]) -> TraitProfile:
    scores = {trait: 50 for trait in KEYWORDS}
    text = " ".join(entries).lower()
    for trait, words in KEYWORDS.items():
        hits = 0
        for word in words:
            hits += len(re.findall(rf"\b{re.escape(word)}\b", text))
        scores[trait] = min(100, 50 + hits * 5)
    return TraitProfile(
        openness=scores["openness"],
        conscientiousness=scores["conscientiousness"],
        extraversion=scores["extraversion"],
        agreeableness=scores["agreeableness"],
        neuroticism=scores["neuroticism"],
    )


def summarize_profile(profile: TraitProfile) -> str:
    lines = ["Resumo da personalidade (estimativa baseada no diário):"]
    for trait, value in profile.as_dict().items():
        label = "baixo"
        if value >= 70:
            label = "alto"
        elif value >= 55:
            label = "moderado"
        lines.append(f"- {trait}: {value}/100 ({label})")
    lines.append(
        "\nLembrete: esta análise é apenas indicativa e não substitui avaliação profissional."
    )
    return "\n".join(lines)


def prompt_user() -> None:
    print("Bem-vindo ao Diário Interativo! Escreva seus pensamentos.")
    print("Comandos: 'analisar' para resumo, 'sair' para encerrar.\n")
    entries: List[str] = []
    follow_up_index = 0
    while True:
        entry = input("Você: ").strip()
        if not entry:
            print("Diário: Pode escrever quando estiver pronto.")
            continue
        lowered = entry.lower()
        if lowered in {"sair", "exit", "quit"}:
            print("Diário: Obrigado por compartilhar seu dia comigo!")
            break
        if lowered in {"analisar", "resumo", "perfil"}:
            if not entries:
                print("Diário: Ainda não tenho conteúdo suficiente para analisar.")
                continue
            profile = score_entries(entries)
            print(summarize_profile(profile))
            continue
        entries.append(entry)
        follow_up = FOLLOW_UPS[follow_up_index % len(FOLLOW_UPS)]
        follow_up_index += 1
        print(f"Diário: Obrigado por compartilhar. {follow_up}")


if __name__ == "__main__":
    prompt_user()
