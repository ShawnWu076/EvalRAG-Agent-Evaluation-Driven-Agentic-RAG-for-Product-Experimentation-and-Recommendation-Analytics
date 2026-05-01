"""LangGraph workflow for bounded experimentation analysis."""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.graph.nodes import GraphDependencies, GraphNodes
from app.graph.state import ExperimentGraphState


def _route_after_evidence(state: ExperimentGraphState) -> str:
    if state.get("evidence_sufficiency") == "insufficient" and state.get("retry_count", 0) < state.get("max_retries", 1):
        return "replan"
    return "decision"


def _route_after_policy(state: ExperimentGraphState) -> str:
    policy_validation = state.get("policy_validation") or {}
    if policy_validation.get("policy_override") and state.get("retry_count", 0) < state.get("max_retries", 1):
        return "revise"
    return "memo"


def build_workflow(deps: GraphDependencies):
    nodes = GraphNodes(deps)
    graph = StateGraph(ExperimentGraphState)

    graph.add_node("intake_node", nodes.intake_node)
    graph.add_node("classify_task_node", nodes.classify_task_node)
    graph.add_node("tool_planner_node", nodes.tool_planner_node)
    graph.add_node("tool_executor_node", nodes.tool_executor_node)
    graph.add_node("retrieval_node", nodes.retrieval_node)
    graph.add_node("evidence_bundle_node", nodes.evidence_bundle_node)
    graph.add_node("evidence_checker_node", nodes.evidence_checker_node)
    graph.add_node("replan_node", nodes.replan_node)
    graph.add_node("decision_node", nodes.decision_node)
    graph.add_node("policy_validator_node", nodes.policy_validator_node)
    graph.add_node("revise_decision_node", nodes.revise_decision_node)
    graph.add_node("memo_generator_node", nodes.memo_generator_node)
    graph.add_node("eval_node", nodes.eval_node)

    graph.add_edge(START, "intake_node")
    graph.add_edge("intake_node", "classify_task_node")
    graph.add_edge("classify_task_node", "tool_planner_node")
    graph.add_edge("tool_planner_node", "tool_executor_node")
    graph.add_edge("tool_executor_node", "retrieval_node")
    graph.add_edge("retrieval_node", "evidence_bundle_node")
    graph.add_edge("evidence_bundle_node", "evidence_checker_node")
    graph.add_conditional_edges(
        "evidence_checker_node",
        _route_after_evidence,
        {
            "replan": "replan_node",
            "decision": "decision_node",
        },
    )
    graph.add_edge("replan_node", "tool_executor_node")
    graph.add_edge("decision_node", "policy_validator_node")
    graph.add_conditional_edges(
        "policy_validator_node",
        _route_after_policy,
        {
            "revise": "revise_decision_node",
            "memo": "memo_generator_node",
        },
    )
    graph.add_edge("revise_decision_node", "policy_validator_node")
    graph.add_edge("memo_generator_node", "eval_node")
    graph.add_edge("eval_node", END)
    return graph.compile()


def run_workflow(initial_state: ExperimentGraphState, deps: GraphDependencies) -> ExperimentGraphState:
    workflow = build_workflow(deps)
    return workflow.invoke(initial_state)
