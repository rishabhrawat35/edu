import json
import os

from agenticorg import AgenticOrg

client = AgenticOrg(
    api_key=os.environ["AGENTICORG_API_KEY"],
    base_url="https://agenticorg.hackathon.pinelabs.com",
)
result = client.agents.run(
    "cce86119-3070-487e-bd19-dc02281ac265",
    inputs={"message": "hey send todays time", "query": "hey send todays time"},
)
print(result.status, result.confidence)
print(json.dumps(result.output, indent=2, default=str))
