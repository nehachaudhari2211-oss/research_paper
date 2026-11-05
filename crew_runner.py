from crewai import Crew, Process

from agents import (
    discovery_agent,
    summarization_agent,
    literature_agent,
    gap_agent,
    report_agent
)

from tasks import create_tasks


def run_research(topic, papers):

    tasks = create_tasks(topic, papers)

    crew = Crew(

        agents=[
            discovery_agent,
            summarization_agent,
            literature_agent,
            gap_agent,
            report_agent
        ],

        tasks=tasks,

        process=Process.sequential,

        verbose=True
    )

    result = crew.kickoff()

    return str(result)