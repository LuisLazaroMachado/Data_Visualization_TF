# Entrega 3 - Modelo, metricas y preprocesamiento

## Proyecto

**The AI Power Map** analiza la evolucion y concentracion de modelos de inteligencia artificial registrados en el dataset publico de Epoch AI.

## Alcance de esta entrega

Esta entrega no desarrolla dashboard ni visualizacion exploratoria como componente principal. Su objetivo es dejar un pipeline reproducible para preparar el dataset, comparar dos estructuras de modelo de datos y seleccionar la fuente recomendada para Tableau.

## Fuente esperada

- Archivo requerido: `data/raw/all_ai_models.csv`
- Dataset usado por los notebooks previos: `all_ai_models.csv` de Epoch AI
- Unidad de analisis: un modelo de IA registrado
- Granularidad esperada: una fila por modelo despues de eliminar duplicados por `Model`

## Resultado de ejecucion

El pipeline fue ejecutado con el archivo real `data/raw/all_ai_models.csv`.

| Indicador | Resultado |
|---|---:|
| Filas originales | 3,509 |
| Columnas originales | 57 |
| Filas limpias | 3,405 |
| Columnas limpias | 22 |
| Duplicados por `Model` despues de limpiar | 0 |
| Filas con nulos criticos despues de limpiar | 0 |
| Anio minimo | 1950 |
| Anio maximo | 2026 |

Cobertura de variables numericas principales:

| Variable | Cobertura |
|---|---:|
| `Parameters` | 65.87% |
| `Training compute (FLOP)` | 40.12% |
| `Training dataset size (total)` | 40.50% |
| `Training time (hours)` | 15.98% |
| `Training compute cost (2023 USD)` | 6.58% |
| `Hardware quantity` | 24.61% |
| `Citations` | 42.94% |

## Reglas de preprocesamiento documentadas

Las reglas se trasladan desde el notebook de perfilado y limpieza existente:

1. Seleccionar las 20 columnas utiles documentadas para identificacion, clasificacion, escala tecnica, costo, hardware, accesibilidad y referencias.
2. Convertir `Publication date` a fecha y derivar `Year` y `Month`.
3. Convertir `Training dataset size (total)` a numerico.
4. Eliminar duplicados por `Model`, conservando el primer registro, como en el notebook previo.
5. Eliminar filas sin pais, organizacion o fecha de publicacion, porque son dimensiones criticas del analisis.
6. En pais, categoria de organizacion y dominio, conservar el primer valor cuando el campo trae categorias separadas por coma.
7. Imputar categoricas documentadas con `Unknown`.
8. Mantener nulos numericos, porque representan cobertura incompleta de mediciones tecnicas y no deben inventarse.

## Opciones de modelo comparadas

### Opcion A - Tabla plana

Una sola tabla limpia (`models_flat.csv`) conectable directamente en Tableau. Es simple y util para exploracion rapida, pero mezcla hechos, dimensiones y atributos descriptivos.

Esta tabla se conserva en la entrega porque sirve como fuente de respaldo, validacion y comparacion directa contra el esquema estrella. Tambien puede usarse en Tableau si se necesita una conexion rapida sin relaciones entre tablas.

### Opcion B - Esquema estrella

Una tabla de hechos (`fact_models.csv`) y dimensiones para pais, organizacion, dominio y accesibilidad. Esta estructura reduce repeticion y deja relaciones mas explicitas para Tableau.

## Metricas de evaluacion

Las metricas son de validacion estructural, no formulas analiticas inventadas:

- cantidad de tablas
- filas en tabla principal o de hechos
- cantidad de modelos unicos
- duplicados por `Model`
- filas con nulos en campos criticos
- filas con llaves relacionales nulas

## Decision del modelo

| Opcion | Tablas | Filas principales | Modelos unicos | Duplicados por `Model` | Nulos criticos | Llaves relacionales nulas | Recomendacion |
|---|---:|---:|---:|---:|---:|---:|---|
| Tabla plana | 1 | 3,405 | 3,405 | 0 | 0 | 0 | Respaldo |
| Esquema estrella | 5 | 3,405 | 3,405 | 0 | 0 | 0 | Seleccionada |

Se recomienda la **Opcion B - esquema estrella** porque conserva todas las filas del dataset limpio, mantiene `Model` como llave unica de la unidad de analisis y no genera llaves relacionales nulas. La opcion plana se mantiene porque es util para validar totales, revisar discrepancias y conectar rapidamente a Tableau cuando no se requiere modelado relacional.

## Archivos generados

- `data/processed/all_ai_models_clean.csv`
- `outputs/reports/quality_summary.csv`
- `outputs/reports/model_options_comparison.csv`
- `outputs/tableau/models_flat.csv`
- `outputs/tableau/fact_models.csv`
- `outputs/tableau/dim_country.csv`
- `outputs/tableau/dim_organization.csv`
- `outputs/tableau/dim_domain.csv`
- `outputs/tableau/dim_accessibility.csv`
