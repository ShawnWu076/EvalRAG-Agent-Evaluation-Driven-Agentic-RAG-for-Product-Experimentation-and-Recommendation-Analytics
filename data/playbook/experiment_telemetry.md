# Experiment Telemetry and RAG Evaluation

## Why Telemetry Matters

Every RAG answer should be inspectable. Store the user question, retrieved chunks, source files, similarity scores, answer, latency, model name, and any expected evaluation labels. Without traces, a good-looking answer cannot be debugged.

## Retrieval Evaluation

Measure whether the retriever found the right sources. Useful metrics include Hit@K, source match rate, context precision, context recall, and mean reciprocal rank. Retrieval errors often explain answer errors.

## Answer Evaluation

Evaluate concept coverage, decision accuracy, and faithfulness to retrieved context. The answer should mention the concepts the playbook says are necessary, choose a decision label appropriate to the scenario, and avoid rules that are not in the retrieved sources.

## Optimization Loop

Use the loop Build, Log, Evaluate, Diagnose, Optimize. Compare chunk sizes, overlap, vector retrieval, BM25 retrieval, hybrid retrieval, and reranking with the same evaluation questions. Report improvements with metrics, not impressions.

