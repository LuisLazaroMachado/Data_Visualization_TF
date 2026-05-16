from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS_TABLEAU = PROJECT_ROOT / "outputs" / "tableau"
OUTPUTS_REPORTS = PROJECT_ROOT / "outputs" / "reports"

RAW_DATASET = DATA_RAW / "all_ai_models.csv"
CLEAN_DATASET = DATA_PROCESSED / "all_ai_models_clean.csv"

SELECTED_COLUMNS = [
    "Model",
    "Organization",
    "Country (of organization)",
    "Publication date",
    "Organization categorization",
    "Domain",
    "Task",
    "Parameters",
    "Training compute (FLOP)",
    "Training dataset size (total)",
    "Training time (hours)",
    "Training compute cost (2023 USD)",
    "Hardware quantity",
    "Training hardware",
    "Model accessibility",
    "Training code accessibility",
    "Open model weights?",
    "Citations",
    "Confidence",
    "Notability criteria",
]

CRITICAL_COLUMNS = [
    "Country (of organization)",
    "Organization",
    "Publication date",
]

CATEGORICAL_COLUMNS_TO_FILL = [
    "Organization categorization",
    "Domain",
    "Task",
    "Model accessibility",
    "Training code accessibility",
    "Open model weights?",
    "Confidence",
    "Notability criteria",
]

CATEGORICAL_COLUMNS_TO_SPLIT_FIRST = [
    "Country (of organization)",
    "Organization categorization",
    "Domain",
]

NUMERIC_COLUMNS = [
    "Parameters",
    "Training compute (FLOP)",
    "Training dataset size (total)",
    "Training time (hours)",
    "Training compute cost (2023 USD)",
    "Hardware quantity",
    "Citations",
]
