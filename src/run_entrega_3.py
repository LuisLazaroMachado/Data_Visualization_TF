from __future__ import annotations

from .config import CLEAN_DATASET, OUTPUTS_REPORTS, OUTPUTS_TABLEAU, RAW_DATASET
from .io_utils import load_csv, save_csv
from .modeling import build_flat_model, build_star_schema, compare_model_options
from .preprocessing import build_quality_summary, clean_ai_models


def main() -> None:
    raw_df = load_csv(RAW_DATASET)
    clean_df = clean_ai_models(raw_df)

    save_csv(clean_df, CLEAN_DATASET)
    save_csv(build_quality_summary(raw_df, clean_df), OUTPUTS_REPORTS / "quality_summary.csv")
    save_csv(compare_model_options(clean_df), OUTPUTS_REPORTS / "model_options_comparison.csv")

    for name, table in build_flat_model(clean_df).items():
        save_csv(table, OUTPUTS_TABLEAU / f"{name}.csv")

    for name, table in build_star_schema(clean_df).items():
        save_csv(table, OUTPUTS_TABLEAU / f"{name}.csv")

    print("Entrega 3 generada correctamente.")
    print(f"Dataset limpio: {CLEAN_DATASET}")
    print(f"Fuentes Tableau: {OUTPUTS_TABLEAU}")
    print(f"Reportes: {OUTPUTS_REPORTS}")


if __name__ == "__main__":
    main()
