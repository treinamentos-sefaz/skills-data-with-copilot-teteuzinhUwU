"""Módulo 2 — Manipulação de DataFrames com pandas.

Complete cada função com o apoio do GitHub Copilot. Prefira operações
vetorizadas e evite alterar o DataFrame original (use ``.copy()``).

Valide com:  ``python lab/check.py --module pandas``
"""
from __future__ import annotations

import pandas as pd


def load_wines(path: str) -> pd.DataFrame:
    """Leia o CSV em ``path`` e retorne um DataFrame do pandas."""
    return pd.read_csv(path)


def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Converta a coluna ``rating`` para numérico e remova as linhas cujo
    ``rating`` seja nulo. Retorne o DataFrame limpo."""
    result = df.copy()
    result["rating"] = pd.to_numeric(result["rating"], errors="coerce")
    return result.dropna(subset=["rating"]).reset_index(drop=True)


def top_varieties_by_avg_rating(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Retorne as ``n`` variedades com maior média de ``rating`` (colunas:
    variety, avg_rating), ordenadas da maior para a menor."""
    return (
        df.groupby("variety")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .reset_index(name="avg_rating")
    )


def add_rating_category(df: pd.DataFrame) -> pd.DataFrame:
    """Adicione a coluna ``rating_category`` com as faixas: "Baixa" (< 85),
    "Média" (85 a 90) e "Alta" (> 90)."""
    result = df.copy()
    result["rating_category"] = pd.Series(pd.NA, index=result.index, dtype="object")
    result.loc[result["rating"] < 85, "rating_category"] = "Baixa"
    result.loc[result["rating"].between(85, 90), "rating_category"] = "Média"
    result.loc[result["rating"] > 90, "rating_category"] = "Alta"
    return result


def enrich_with_country(df: pd.DataFrame) -> pd.DataFrame:
    """Adicione a coluna ``country`` extraindo o último trecho após a vírgula de
    ``region`` (ex.: "Mendocino, California" -> "California")."""
    result = df.copy()
    result["country"] = result["region"].str.split(",").str[-1].str.strip()
    return result
