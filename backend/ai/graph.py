from langgraph.graph import StateGraph, START, END

from .state import AgentState

from .nodes import (
    analyze_requirement,
    read_source_files,
    generate_code_changes,
)


def create_agent_graph():

    graph = StateGraph(AgentState)

    graph.add_node(
        "analyze_requirement",
        analyze_requirement,
    )

    graph.add_node(
        "read_source_files",
        read_source_files,
    )

    graph.add_node(
        "generate_code_changes",
        generate_code_changes,
    )

    graph.add_edge(
        START,
        "analyze_requirement",
    )

    graph.add_edge(
        "analyze_requirement",
        "read_source_files",
    )

    graph.add_edge(
        "read_source_files",
        "generate_code_changes",
    )

    graph.add_edge(
        "generate_code_changes",
        END,
    )

    return graph.compile()