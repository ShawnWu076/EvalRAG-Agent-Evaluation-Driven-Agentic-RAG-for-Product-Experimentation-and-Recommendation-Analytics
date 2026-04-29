"""FastAPI application for EvalRAG Agent."""

from __future__ import annotations

from fastapi import FastAPI, File, Form, UploadFile

from app.rag_pipeline import EvalRAGPipeline, record_to_public_response
from app.schemas import AnalyzeResponse, AskRequest, AskResponse
from app.tools.experiment_stats import generate_experiment_summary_from_csv_text


app = FastAPI(
    title="EvalRAG Agent",
    description="Evaluation-driven agentic RAG for product experimentation analytics.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> dict[str, object]:
    pipeline = EvalRAGPipeline(top_k=request.top_k)
    record = pipeline.answer(
        request.question,
        expected_sources=request.expected_sources,
        expected_concepts=request.expected_concepts,
        expected_decision=request.expected_decision,
    )
    return record_to_public_response(record)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    question: str = Form(...),
    file: UploadFile = File(...),
) -> dict[str, object]:
    contents = await file.read()
    csv_text = contents.decode("utf-8")
    tool_summary = generate_experiment_summary_from_csv_text(csv_text)
    pipeline = EvalRAGPipeline()
    record = pipeline.answer(question, tool_summary=tool_summary)
    response = record_to_public_response(record)
    response["tool_summary"] = tool_summary
    return response

