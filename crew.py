# CrewAI + DomeKit Example
#
# DomeKit is an OpenAI-compatible local AI runtime that sits between CrewAI
# and your local LLM. It policy-checks every tool call and audit-logs all
# activity. CrewAI doesn't know DomeKit is there — it just sees an OpenAI
# endpoint. But DomeKit controls what ALL agents in the crew can access.

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Point the LLM at DomeKit's OpenAI-compatible API.
# DomeKit forwards requests to Ollama while enforcing policies from domekit.yaml.
llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
    model="llama3.1:8b",
)

# --- Agents ---

researcher = Agent(
    role="Product Researcher",
    goal="Investigate product data by querying the database to find top products by revenue",
    backstory=(
        "You are a data analyst who specializes in product performance. "
        "You query databases to extract actionable insights about product revenue and trends."
    ),
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Report Writer",
    goal="Write a clear, concise market summary report based on the researcher's findings",
    backstory=(
        "You are a business writer who turns raw data insights into polished summaries. "
        "You focus on clarity and actionable takeaways."
    ),
    llm=llm,
    verbose=True,
)

# --- Tasks ---

research_task = Task(
    description=(
        "Query the products database (data/products.db) to find the top 5 products by revenue. "
        "For each product, include the name, category, price, units sold, and total revenue. "
        "Use the sql_query tool with the database at data/products.db."
    ),
    expected_output="A list of the top 5 products by revenue with their details.",
    agent=researcher,
)

report_task = Task(
    description=(
        "Using the researcher's findings about top products, write a brief market summary report. "
        "Include an overview of the top performers, which categories dominate, "
        "and one or two actionable recommendations."
    ),
    expected_output="A short market summary report (3-5 paragraphs).",
    agent=writer,
)

# --- Crew ---

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, report_task],
    verbose=True,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("CREW RESULT")
    print("=" * 60)
    print(result)
