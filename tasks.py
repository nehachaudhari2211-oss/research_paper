
from crewai import Task

from agents import (
    discovery_agent,
    summarization_agent,
    literature_agent,
    gap_agent,
    report_agent
)


def create_tasks(topic, papers):

    # Reduce input size to stay within Groq token limits
    paper_details = []

    for p in papers[:2]:
        paper_details.append({
            "title": p.get("title"),
            "authors": p.get("authors", [])[:2],
            "year": p.get("year"),
            "abstract": p.get("abstract", "")[:300],
            "doi": p.get("doi"),
            "url": p.get("url")
        })


    discovery_task = Task(
        description=f"""
        Research Topic: {topic}

        Analyze these OpenAlex papers:
        {paper_details}

        Organize the papers with title, authors,
        year, DOI, abstract and source URL.

        Never invent references.
        """,
        expected_output="Organized academic paper metadata.",
        agent=discovery_agent
    )


    summary_task = Task(
        description="""
        Summarize each paper briefly using only
        the information provided.

        Include:
        1. Objective
        2. Methodology
        3. Findings
        4. Conclusion
        5. Limitations

        If information is unavailable, mention it.
        Do not invent information.
        """,
        expected_output="Brief individual research paper summaries.",
        agent=summarization_agent,
        context=[discovery_task]
    )


    literature_task = Task(
        description=f"""
        Prepare a concise literature review on {topic}.

        Compare:
        1. Research methods
        2. Findings
        3. Similarities and differences
        4. Research trends

        Use only the supplied paper information.
        """,
        expected_output="Concise comparative literature review.",
        agent=literature_agent,
        context=[summary_task]
    )


    gap_task = Task(
        description="""
        Identify research gaps based on the literature review.

        Include:
        1. Existing limitations
        2. Unexplored areas
        3. Research opportunities
        4. Future research questions

        Support each gap with paper evidence.
        Do not invent evidence.
        """,
        expected_output="Evidence-supported research gaps.",
        agent=gap_agent,
        context=[literature_task]
    )


    report_task = Task(
        description=f"""
        Create a concise research report on {topic}.

        Sections:
        1. Introduction
        2. Discovered Papers
        3. Paper Summaries
        4. Literature Review
        5. Research Gaps
        6. Future Research Directions
        7. References

        Preserve original citations and DOI.
        Never fabricate references.
        """,
        expected_output="Concise academic research report.",
        agent=report_agent,
        context=[
            discovery_task,
            summary_task,
            literature_task,
            gap_task
        ]
    )

    return [
        discovery_task,
        summary_task,
        literature_task,
        gap_task,
        report_task
    ]
