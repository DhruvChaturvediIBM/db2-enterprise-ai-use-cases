"""UC13 command-line entry point."""

import argparse

from crewai import Crew, Process, Task

from agents import enterprise_researcher


DEFAULT_QUERY = (
    "What are our authentication architecture decisions and "
    "how do they relate to recent incidents?"
)


def build_crew(query: str) -> Crew:
    research_task = Task(
        description=(
            f"Answer this enterprise question: {query}\n\n"
            "Use the IBM Db2 Enterprise Knowledge Search tool to find "
            "relevant documents. Search the knowledge base, read the "
            "returned text, and base your answer only on what the tool "
            "returns. Cite document IDs that appear in the results. "
            "If the tool returns no useful evidence, say so."
        ),
        expected_output=(
            "A concise answer grounded in documents returned by the "
            "IBM Db2 search tool, with document IDs cited."
        ),
        agent=enterprise_researcher,
    )

    return Crew(
        agents=[enterprise_researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default=DEFAULT_QUERY)
    args = parser.parse_args()

    result = build_crew(args.query).kickoff()
    print("\n=== Final Answer ===\n")
    print(result)


if __name__ == "__main__":
    main()
