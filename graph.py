from langgraph.graph import StateGraph
from typing import TypedDict
from agents import (
    research_agent,
    answer_drafting_agent,
    refine_agent,
    fact_checker_agent
)

class GraphState(TypedDict):
    query: str
    research: str
    answer: str

def research_node(state: GraphState) -> GraphState:
    research = research_agent(state["query"])
    return {"query": state["query"], "research": research}

def drafting_node(state: GraphState) -> GraphState:
    answer = answer_drafting_agent(state["research"])
    return {"query": state["query"], "research": state["research"], "answer": answer}

def refine_node(state: GraphState) -> GraphState:
    refined = refine_agent(state["answer"])
    return {"query": state["query"], "research": state["research"], "answer": refined}

def fact_checker_node(state: GraphState) -> GraphState:
    fact_checked = fact_checker_agent(state["answer"])
    return {"query": state["query"], "research": state["research"], "answer": fact_checked}

def final_node(state: GraphState) -> GraphState:
    return state

def final_polish_node(state: GraphState) -> GraphState:
    polished = refine_agent(state["answer"])
    return {"query": state["query"], "research": state["research"], "answer": polished}

def choose_path(state: GraphState) -> str:
    answer_text = state["answer"].lower()
    research_text = state["research"].lower()

    print("\n[Routing Decision]")
    print(f"Answer (preview): {answer_text[:150]}")
    print(f"Research (preview): {research_text[:150]}")

    refine_keywords = ["error", "unclear", "not sure", "unknown", "confused", "impossible", "unlikely", "absurd", "weird"]
    fact_check_keywords = ["controversial", "debate", "hoax", "false", "misinformation", "disputed"]

    if any(k in answer_text for k in refine_keywords):
        print("[Routing] Draft unclear — routing to RefinerAgent.")
        return "refine"

    if any(k in research_text for k in fact_check_keywords):
        print("[Routing] Research controversial — routing to FactCheckerAgent.")
        return "fact_check"

    print("[Routing] No special conditions — going to Final.")
    return "final"

def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("ResearchAgent", research_node)
    builder.add_node("AnswerDrafter", drafting_node)
    builder.add_node("RefinerAgent", refine_node)
    builder.add_node("FactCheckerAgent", fact_checker_node)
    builder.add_node("Final", final_node)
    builder.add_node("FinalPolish", final_polish_node)

    builder.set_entry_point("ResearchAgent")
    builder.add_edge("ResearchAgent", "AnswerDrafter")

    builder.add_conditional_edges("AnswerDrafter", choose_path, {
        "refine": "RefinerAgent",
        "fact_check": "FactCheckerAgent",
        "final": "Final"
    })

    builder.add_edge("RefinerAgent", "FinalPolish")
    builder.add_edge("FactCheckerAgent", "FinalPolish")
    builder.add_edge("Final", "FinalPolish")

    builder.set_finish_point("FinalPolish")

    return builder.compile()
