# The AI Power Map

Proyecto de visualizacion de datos para analizar la evolucion, concentracion geografica, dominios, accesibilidad y caracteristicas tecnicas de modelos de inteligencia artificial registrados en una fuente publica verificable.

## Estructura

```text
Data_Visualization_TF/
  data/
    raw/
    processed/
  docs/
  notebooks/
  outputs/
    reports/
    tableau/
  src/
```

## Entrega 3 - Semana 7

La entrega de semana 7 queda centrada en preprocesamiento, comparacion de opciones de modelo de datos y metricas de validacion estructural. No se agregan formulas analiticas sin respaldo: las reglas implementadas vienen de los notebooks existentes.

## Como ejecutar

1. Colocar el archivo original en `data/raw/all_ai_models.csv`.
2. Ejecutar el pipeline desde la raiz del proyecto:

```powershell
python -m src.run_entrega_3
```

Si `python` no esta en PATH, usar el interprete de Python disponible en el entorno local o de Jupyter.

## Salidas principales

- Dataset limpio: `data/processed/all_ai_models_clean.csv`
- Comparacion de modelos: `outputs/reports/model_options_comparison.csv`
- Fuentes para Tableau: `outputs/tableau/`
- Reporte metodologico: `docs/entrega_3_modelo_metricas_preprocesamiento.md`

## Criterio de documentacion

Los archivos `.py` se mantienen enfocados en ejecutar el pipeline. La explicacion metodologica, reglas de limpieza, decision del modelo y criterios de validacion estan documentados en `docs/entrega_3_modelo_metricas_preprocesamiento.md`, para evitar mezclar defensa academica con implementacion.
