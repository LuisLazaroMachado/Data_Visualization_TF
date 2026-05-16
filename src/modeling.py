from __future__ import annotations

import pandas as pd

from .config import NUMERIC_COLUMNS


def build_flat_model(clean_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {"models_flat": clean_df.copy()}


def _dimension(df: pd.DataFrame, columns: list[str], key_name: str) -> pd.DataFrame:
    dim = df.loc[:, columns].drop_duplicates().reset_index(drop=True).copy()
    dim.insert(0, key_name, range(1, len(dim) + 1))
    return dim


def build_star_schema(clean_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    dim_country = _dimension(clean_df, ["Country (of organization)"], "country_id")
    dim_organization = _dimension(
        clean_df,
        ["Organization", "Organization categorization", "Country (of organization)"],
        "organization_id",
    )
    dim_domain = _dimension(clean_df, ["Domain", "Task"], "domain_id")
    dim_accessibility = _dimension(
        clean_df,
        ["Model accessibility", "Training code accessibility", "Open model weights?"],
        "accessibility_id",
    )

    fact = clean_df.copy()
    fact = fact.merge(dim_country, on="Country (of organization)", how="left")
    fact = fact.merge(
        dim_organization,
        on=["Organization", "Organization categorization", "Country (of organization)"],
        how="left",
    )
    fact = fact.merge(dim_domain, on=["Domain", "Task"], how="left")
    fact = fact.merge(
        dim_accessibility,
        on=["Model accessibility", "Training code accessibility", "Open model weights?"],
        how="left",
    )

    fact_columns = [
        "Model",
        "Publication date",
        "Year",
        "Month",
        "country_id",
        "organization_id",
        "domain_id",
        "accessibility_id",
        "Training hardware",
        "Confidence",
        "Notability criteria",
        *NUMERIC_COLUMNS,
    ]
    fact_models = fact.loc[:, fact_columns].copy()

    return {
        "fact_models": fact_models,
        "dim_country": dim_country,
        "dim_organization": dim_organization,
        "dim_domain": dim_domain,
        "dim_accessibility": dim_accessibility,
    }


def compare_model_options(clean_df: pd.DataFrame) -> pd.DataFrame:
    star = build_star_schema(clean_df)
    fact = star["fact_models"]
    rows = [
        {
            "option": "A_flat_table",
            "description": "Tabla limpia unica para Tableau",
            "tables": 1,
            "fact_rows": len(clean_df),
            "unique_model_keys": clean_df["Model"].nunique(),
            "duplicate_model_rows": clean_df.duplicated(subset=["Model"]).sum(),
            "critical_null_rows": clean_df[["Country (of organization)", "Organization", "Publication date"]].isna().any(axis=1).sum(),
            "relationship_null_keys": 0,
            "recommended": "No",
        },
        {
            "option": "B_star_schema",
            "description": "Tabla de hechos con dimensiones de pais, organizacion, dominio y accesibilidad",
            "tables": len(star),
            "fact_rows": len(fact),
            "unique_model_keys": fact["Model"].nunique(),
            "duplicate_model_rows": fact.duplicated(subset=["Model"]).sum(),
            "critical_null_rows": fact[["Publication date"]].isna().any(axis=1).sum(),
            "relationship_null_keys": fact[["country_id", "organization_id", "domain_id", "accessibility_id"]].isna().any(axis=1).sum(),
            "recommended": "Si",
        },
    ]
    return pd.DataFrame(rows)
