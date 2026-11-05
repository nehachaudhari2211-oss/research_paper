import streamlit as st

from tools import search_papers
from crew_runner import run_research


st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 CrewAI Research Paper Assistant")

st.write(
    "AI-powered Research Paper Discovery "
    "and Literature Review System"
)


st.sidebar.header("Research Settings")

topic = st.sidebar.text_input(
    "Enter Research Topic",
    placeholder="Generative AI in Healthcare"
)

number = st.sidebar.slider(
    "Number of Papers",
    3, 20, 5
)

start_year = st.sidebar.number_input(
    "Starting Year",
    1900, 2026, 2020
)

end_year = st.sidebar.number_input(
    "Ending Year",
    1900, 2026, 2026
)


if st.button("Generate Research Report"):

    if not topic.strip():

        st.error("Please enter research topic.")

    elif start_year > end_year:

        st.error("Invalid year range.")

    else:

        try:

            with st.spinner("Searching research papers..."):

                papers = search_papers(
                    topic,
                    number,
                    start_year,
                    end_year
                )

            if not papers:
                st.warning("No papers found.")
                st.stop()

            st.success(
                f"{len(papers)} papers discovered!"
            )

            st.header("Discovered Research Papers")

            for i, paper in enumerate(papers, 1):

                with st.expander(
                    f"{i}. {paper['title']}"
                ):

                    st.write("Authors:", ", ".join(
                        paper["authors"]
                    ))

                    st.write("Year:", paper["year"])

                    st.write("Abstract:", paper["abstract"])

                    st.write("DOI:", paper["doi"])

                    st.markdown(
                        f"[Open Paper]({paper['url']})"
                    )

            st.header("AI Agents Working")

            with st.spinner(
                "Five AI Agents are preparing your report..."
            ):

                report = run_research(topic, papers)

            st.success("Research Report Generated!")

            st.header("Final Research Report")

            st.markdown(report)

            st.download_button(
                "Download Research Report",
                report,
                file_name="research_report.md",
                mime="text/markdown"
            )

        except Exception as e:

            st.error(f"Error: {e}")


st.divider()

st.caption(
    "Developed using Python, CrewAI, Groq and OpenAlex"
)