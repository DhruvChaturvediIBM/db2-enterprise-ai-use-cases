# Implementation Notes

## Runtime retrieval

UC13 uses the actual `DB2VectorSearchTool` from `crewai_tools`.

The current IBM Db2/CrewAI example configures:

- `connection_string`
- `table_name`
- `vector_column`
- `return_columns`
- `limit`
- `distance_metric`
- `custom_embedding_fn`

The tool is retrieval-only. It does not perform ingestion.

## Ingestion

Haystack is isolated in `ingestion/ingest.py`.

If the installed `ibm-db-haystack` release exposes a different constructor signature, update only this ingestion adapter. Do not replace the runtime `DB2VectorSearchTool`.

## Model compatibility

The same embedding model and vector dimension must be used when writing vectors and querying them.

Default demonstration model:

`ibm-granite/granite-embedding-125m-english`

Default dimension:

`768`

Default distance:

`COSINE`

## LLM

Runtime reasoning is configured for:

`granite3.1-dense:8b`

The project keeps the LLM separate from Db2 retrieval so the search tool remains an explicit CrewAI capability.
