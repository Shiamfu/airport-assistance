
import json

from client import client
from config import MODEL

from tools.flight import get_flight_and_gate_status
from tools.routing import calculate_terminal_transfer_time
from tools.mobility import request_mobility_dispatch_async

from safety.check import check_connection_feasibility

from database.db import log_event


SYSTEM_PROMPT = """
You are SkyLink AI, an airport passenger assistance agent
created by Team Soaring Crescent.

Your responsibilities:

1. Understand passenger requests.
2. Identify wheelchair and accessibility needs.
3. Check flight and gate information using Python tools.
4. Calculate transfer times using Python tools.
5. Explain connection feasibility.
6. Request mobility assistance when needed.
7. Clearly communicate pending and confirmed approvals.

STRICT RULES:

- Never invent a flight, gate or boarding time.
- Never invent airport routes or distances.
- Never claim that mobility assistance is confirmed
  while its status is pending.
- Never approve your own mobility request.
- Never guarantee that a passenger will make a flight.
- Use verified route information only.
- If information is missing, explain that it is unavailable.
- Be polite, calm and accessible.
- Explain the next step clearly.
- All flight and terminal information is simulated.
"""


FUNCTIONS = {
    "get_flight_and_gate_status":
        get_flight_and_gate_status,

    "calculate_terminal_transfer_time":
        calculate_terminal_transfer_time,

    "request_mobility_dispatch_async":
        request_mobility_dispatch_async,

    "check_connection_feasibility":
        check_connection_feasibility
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_flight_and_gate_status",
            "description": "Retrieve flight and gate details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {
                        "type": "string"
                    }
                },
                "required": ["flight_number"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_terminal_transfer_time",
            "description": "Calculate terminal transfer time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin_gate": {
                        "type": "string"
                    },
                    "destination_gate": {
                        "type": "string"
                    },
                    "mobility_mode": {
                        "type": "string",
                        "enum": ["walking", "wheelchair"]
                    },
                    "family_travelling": {
                        "type": "boolean"
                    }
                },
                "required": [
                    "origin_gate",
                    "destination_gate",
                    "mobility_mode"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "request_mobility_dispatch_async",
            "description": "Create a mobility request that requires human approval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "passenger": {
                        "type": "string"
                    },
                    "flight": {
                        "type": "string"
                    },
                    "origin_gate": {
                        "type": "string"
                    },
                    "destination_gate": {
                        "type": "string"
                    },
                    "assistance_type": {
                        "type": "string"
                    },
                    "reason": {
                        "type": "string"
                    }
                },
                "required": [
                    "passenger",
                    "flight",
                    "origin_gate",
                    "destination_gate",
                    "assistance_type",
                    "reason"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_connection_feasibility",
            "description": "Check the connection timing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "boarding_minutes": {
                        "type": "integer"
                    },
                    "transfer_minutes": {
                        "type": "integer"
                    },
                    "extra_requirements": {
                        "type": "boolean"
                    }
                },
                "required": [
                    "boarding_minutes",
                    "transfer_minutes"
                ]
            }
        }
    }
]


def run_agent(user_message):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    activity = []

    for _ in range(8):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.1
        )

        message = response.choices[0].message

        if not message.tool_calls:

            log_event(
                "AGENT_RESPONSE",
                message.content
            )

            return {
                "answer": message.content,
                "activity": activity
            }

        messages.append(
            message.model_dump(exclude_none=True)
        )

        for call in message.tool_calls:

            name = call.function.name

            arguments = json.loads(
                call.function.arguments
            )

            if name not in FUNCTIONS:

                result = {
                    "error": "Tool not registered"
                }

            else:

                try:

                    result = FUNCTIONS[name](
                        **arguments
                    )

                except Exception as error:

                    result = {
                        "error": str(error)
                    }

            activity.append({
                "tool": name,
                "arguments": arguments,
                "result": result
            })

            log_event(name, result)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result)
            })

            # Stop the AI from making further
            # consequential requests while approval
            # is pending.

            if (
                name == "request_mobility_dispatch_async"
                and result.get("status")
                == "PENDING_HUMAN_APPROVAL"
            ):

                return {
                    "answer": (
                        "Your mobility assistance request "
                        "has been submitted. It is awaiting "
                        "airport coordinator approval. "
                        "It is not confirmed yet."
                    ),
                    "activity": activity,
                    "pending_approval": True,
                    "request_id": result["request_id"]
                }

    return {
        "answer": "Maximum tool-call limit reached.",
        "activity": activity
    }

