from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_tavily import TavilySearch
from .nodes import *


def build_graph(retriever):
    llm = ChatOllama(model=OLLAMA_WRITER_MODEL, temperature=0.8, num_ctx=32000) 
    planner_llm = ChatOllama(model=OLLAMA_CRITIC_MODEL, temperature=0.5)  
    web_search = TavilySearch(tavily_api_key=TAVILY_API_KEY,max_results=2)

    graph = StateGraph(SeminarState)

    graph.add_node("plan", plan_outline(planner_llm))
    graph.add_node("brainstorm", brainstorm_section(llm))
    graph.add_node("research", research_section(retriever, web_search))
    graph.add_node("write", write_section(llm))
    graph.add_node("validate", validate_section(planner_llm))
    graph.add_node("save", save_and_next)
    graph.add_node("synthesize", synthesize_full_report(llm))

    graph.set_entry_point("plan")

    graph.add_edge("plan", "brainstorm")
    graph.add_edge("brainstorm", "research")
    graph.add_edge("research", "write")
    graph.add_edge("write", "validate")

    graph.add_conditional_edges("validate", route_after_validation, {
        "write": "write",
        "save": "save"
    })

    graph.add_conditional_edges("save", should_continue, {
        "continue": "brainstorm",
        "done": "synthesize"
    })

    graph.add_edge("synthesize", END)
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)