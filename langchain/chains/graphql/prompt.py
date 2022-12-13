# flake8: noqa
from langchain.prompts.prompt import PromptTemplate

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct GraphQL query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
Query: "Query to run"
Result: "Result of the GraphQL query"
Answer: "Final answer here"

Only use the following GraphQL Schema:

{schema}

Only include the fields in the query that are needed to answer the question.
For example, if the question is "Today is 12/13/2022, who does LSU play?", you can query getGameDetailsByTeamName(teamName: "LSU")

Question: {input}

"""

PROMPT = PromptTemplate(
    input_variables=["input", "schema"],
    template=_DEFAULT_TEMPLATE,
)
