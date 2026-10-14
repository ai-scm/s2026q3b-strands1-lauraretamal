from strands import Agent, tool
from strands_tools import http_request
from typing import Dict, Any
import boto3
import os
import json

REGION = "us-east-1"
KNOWLEDGE_BASE_ID = os.environ["KNOWLEDGE_BASE_ID"]

ddb = boto3.resource("dynamodb", region_name=REGION)
table = ddb.Table(os.environ["SESSIONS_TABLE"])

bedrock_agent = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION
)


def get_session_history(session_id: str) -> list:
    try:
        response = table.get_item(Key={"sessionID": session_id})
        if "Item" in response:
            return json.loads(response["Item"]["messages"])
        return []
    except Exception as e:
        print(f"Error retrieving session history: {e}")
        return []


def update_session_history(session_id: str, messages: list):
    try:
        table.put_item(
            Item={
                "sessionID": session_id,
                "messages": json.dumps(messages)
            }
        )
    except Exception as e:
        print(f"Error updating session history: {e}")


@tool
def flight_search(city: str) -> dict:
    """Get available flight options to a city."""
    flights = {
        "Atlanta": ["AnyCompany 1 Airlines", "AnyCompany 2 Airlines"],
        "Seattle": ["AnyCompany 1 Airlines", "AnyCompany 3 Airlines"],
        "New York": ["AnyCompany 1 Airlines", "AnyCompany 4"]
    }
    return flights.get(city, {"error": f"No flights found for {city}"})


@tool
def search_tours(query: str) -> str:
    """Search the travel knowledge base for tour operators and activities."""
    try:
        response = bedrock_agent.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": query},
            retrievalConfiguration={
                "managedSearchConfiguration": {
                    "numberOfResults": 5
                }
            }
        )

        results = response.get("retrievalResults", [])

        if not results:
            return "No matching tour information was found."

        return "\n".join(
            item.get("content", {}).get("text", "")
            for item in results
        )

    except Exception as e:
        print(f"Knowledge Base retrieval failed: {e}")
        return f"Knowledge Base retrieval failed: {e}"


TRAVEL_AGENT_PROMPT = """You are a travel assistant.

Use flight_search for flight options.
Use search_tours for tour operators and activities.
Only recommend operators supported by the search results.
Never invent tour operators.
If the search fails or returns no results, explain that clearly.

For US weather, use http_request with the National Weather Service API.
Seattle ZIP code is 98101 and its coordinates are 47.6061, -122.3328.
Query the points endpoint first, then use the returned forecast URL.

Keep responses friendly, accurate, and concise.
"""


def handler(event: Dict[str, Any], _context) -> str:
    session_id = event["user"]["session_id"]
    history = get_session_history(session_id)

    agent = Agent(
        model="us.amazon.nova-lite-v1:0",
        system_prompt=TRAVEL_AGENT_PROMPT,
        tools=[flight_search, search_tours, http_request],
        messages=history
    )

    response = agent(event.get("prompt", ""))
    update_session_history(session_id, agent.messages)

    return str(response)