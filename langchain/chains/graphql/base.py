"""Chain for interacting with GraphQL Database."""
from typing import Dict, List

from pydantic import BaseModel, Extra

from langchain.chains.base import Chain
from langchain.chains.graphql.prompt import PROMPT
from langchain.chains.llm import LLMChain
from langchain.graphql import GraphQLClient
from langchain.input import print_text
from langchain.llms.base import LLM


class GraphQLChain(Chain, BaseModel):
    """Chain for interacting with GraphQL API.

    Example:
        .. code-block:: python

            from langchain import SQLDatabaseChain, OpenAI, SQLDatabase
            db = SQLDatabase(...)
            db_chain = SelfAskWithSearchChain(llm=OpenAI(), database=db)
    """

    llm: LLM
    """LLM wrapper to use."""
    client: GraphQLClient
    """GraphQL client to use."""
    input_key: str = "query"  #: :meta private:
    output_key: str = "result"  #: :meta private:

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    def input_keys(self) -> List[str]:
        """Return the singular input key.

        :meta private:
        """
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Return the singular output key.

        :meta private:
        """
        return [self.output_key]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        llm_chain = LLMChain(llm=self.llm, prompt=PROMPT)
        input_text = f"{inputs[self.input_key]} \nQuery:"
        if self.verbose:
            print_text(input_text)
        llm_inputs = {
            "input": input_text,
            "schema": self.client.schema,
            "stop": ["\nResult:"],
        }
        query = llm_chain.predict(**llm_inputs)
        if self.verbose:
            print_text(query, color="green")
        result = self.client.execute_request(query)
        if self.verbose:
            print_text("\nResult: ")
            print_text(result, color="yellow")
            print_text("\nAnswer:")
        input_text += f"{query}\nResult: {result}\nAnswer:"
        llm_inputs["input"] = input_text
        final_result = llm_chain.predict(**llm_inputs)
        if self.verbose:
            print_text(final_result, color="green")
        return {self.output_key: final_result}
