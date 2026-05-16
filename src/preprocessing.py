from __future__ import annotations

import pandas as pd

from .config import (
    CATEGORICAL_COLUMNS_TO_FILL,
    CATEGORICAL_COLUMNS_TO_SPLIT_FIRST,
    CRITICAL_COLUMNS,
    NUMERIC_COLUMNS,
    SELECTED_COLUMNS,
)


def _require_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise KeyError(f"Faltan columnas requeridas en el dataset: {missing}")


def select_analysis_columns(df: pd.DataFrame) -> pd.DataFrame:
    _require_columns(df, SELECTED_COLUMNS)
    return df.loc[:, SELECTED_COLUMNS].copy()


def correct_types(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Publication date"] = pd.to_datetime(out["Publication date"], errors="coerce")
    out["Training dataset size (total)"] = pd.to_numeric(
        out["Training dataset size (total)"], errors="coerce"
    )
    out["Year"] = out["Publication date"].dt.year
    out["Month"] = out["Publication date"].dt.month
    return out


def drop_duplicate_models(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(subset=["Model"], keep="first").copy()


def drop_missing_critical_dimensions(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=CRITICAL_COLUMNS).copy()


def keep_first_category_value(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for column in CATEGORICAL_COLUMNS_TO_SPLIT_FIRST:
        out[column] = out[column].astype("string").str.split(",").str[0].str.strip()
    return out


def fill_categorical_unknowns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for column in CATEGORICAL_COLUMNS_TO_FILL:
        out[column] = out[column].fillna("Unknown")
    return out


def clean_ai_models(df: pd.DataFrame) -> pd.DataFrame:
    out = select_analysis_columns(df)
    out = correct_types(out)
    out = drop_duplicate_models(out)
    out = drop_missing_critical_dimensions(out)
    out = keep_first_category_value(out)
    out = fill_categorical_unknowns(out)
    return out.reset_index(drop=True)


def build_quality_summary(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {"metric": "raw_rows", "value": len(raw_df)},
        {"metric": "raw_columns", "value": raw_df.shape[1]},
        {"metric": "clean_rows", "value": len(clean_df)},
        {"metric": "clean_columns", "value": clean_df.shape[1]},
        {"metric": "duplicate_model_rows_after_cleaning", "value": clean_df.duplicated(subset=["Model"]).sum()},
        {"metric": "critical_null_rows_after_cleaning", "value": clean_df[CRITICAL_COLUMNS].isna().any(axis=1).sum()},
        {"metric": "min_year", "value": int(clean_df["Year"].min()) if clean_df["Year"].notna().any() else None},
        {"metric": "max_year", "value": int(clean_df["Year"].max()) if clean_df["Year"].notna().any() else None},
    ]
    for column in NUMERIC_COLUMNS:
        rows.append({
            "metric": f"coverage_pct__{column}",
            "value": round(float(clean_df[column].notna().mean() * 100), 2),
        })
    return pd.DataFrame(rows)
