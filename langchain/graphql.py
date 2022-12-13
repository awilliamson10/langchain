"""GraphQL API wrapper."""
import json
from typing import Any, Dict, Optional

from graphqlclient import GraphQLClient as _GraphQLClient
from pydantic import BaseModel, Extra, root_validator

from langchain.chains.graphql.queries import SCHEMA_QUERY
from langchain.utils import get_from_dict_or_env


class GraphQLClient:
    """GraphQL API wrapper."""

    def __init__(
        self,
        url: str,
        auth: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
        schema_location: Optional[str] = None,
    ):
        """Initialize the GraphQL client.

        Args:
            url: The URL of the GraphQL API.
            auth: The authentication information to use.
            headers: The headers to use.
            timeout: The timeout to use.
        """
        self.url = url
        self.auth = auth
        self.headers = headers
        self.timeout = timeout
        self.graphql_client = _GraphQLClient(url)

    @property
    def schema(self) -> str:
        """Return the schema of the GraphQL API."""
        schema = self.graphql_client.execute(SCHEMA_QUERY)
        schema = schema.replace('\\"', '"')
        schema = schema.replace("\\n", "\n")
        return schema

    def execute_request(self, query: str, variables: dict = None):
        result = json.loads(self.graphql_client.execute(query, variables))
        if "errors" in result:
            raise Exception(result)
        return result

    def run(self, query: str, variables: dict = None) -> str:
        """Execute a GraphQL query and return a string representing the results.

        If the query returns data, a string of the results is returned.
        If the query returns no data, an empty string is returned.
        """
        result = self.execute_request(query, variables)
        if "data" in result:
            return str(result["data"])
        return ""
