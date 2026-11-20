# PLAN.md
# SWAGON AI — TEAM SOARING CRESCENT
## Autonomous Airport Passenger Journey & Mobility Coordination Agent

**Competition:** IEEE CS SYP TECHX Dubai '26  
**Track:** High School — Foundational AI Agent  
**Domain:** Aviation & Airport Operations  
**Product:** Swagon AI  
**Team:** Soaring Crescent  
**Development environment:** PyCharm  
**Primary language:** Python  
**AI provider:** OpenRouter API  

---

# 0. PROJECT OBJECTIVE

Build an intelligent airport passenger assistance agent that helps passengers navigate connecting flights, gate changes, terminal transfers and accessibility assistance.

The system must be able to:

- Understand natural-language passenger messages.
- Identify connecting flights, gate changes and accessibility needs.
- Retrieve flight and gate information from a structured dataset.
- Calculate walking and wheelchair transfer times using deterministic Python functions.
- Evaluate connecting-flight feasibility.
- Create mobility assistance and gate-hold requests.
- Pause workflows while awaiting human coordinator approval.
- Resume workflows after an asynchronous approval callback.
- Update the passenger interface with the actual confirmed status.
- Record activities, decisions and workflow history.
- Demonstrate accurate operation across at least ten test scenarios.

## Central demonstration scenario

A family sends:

"Our inbound flight DXB-402 just parked at Concourse C, our connecting gate changed to B14, my grandmother needs her wheelchair at the aircraft door, and we only have 35 minutes before boarding closes!"

Swagon AI must understand the urgency, retrieve the relevant flight information, calculate the transfer requirements, identify the assistance requirement, submit an approval request and keep the family informed.

**Important:** The system must never invent live flight information, guarantee a connection based on an estimate, or claim physical assistance has been dispatched before authorised approval.

---

# 1. SYSTEM ARCHITECTURE & HACKATHON TECH STACK

## 1.1 Architecture overview

Use a modular Python architecture with:

- Streamlit frontend.
- FastAPI backend.
- OpenRouter-powered LLM.
- Python tool execution layer.
- SQLite database.
- Asynchronous workflow and approval engine.

The frontend and backend must remain separate so the project can be upgraded without rebuilding its entire interface.

## 1.2 End-to-end architecture

Passenger Interface
    |
    | Natural-language message
    v
Streamlit Frontend
    |
    | HTTP request
    v
FastAPI Backend
    |
    v
Conversation / Agent Service
    |
    +------------------------------+
    |                              |
    v                              v
OpenRouter LLM                Python Validation
    |                              |
    | Tool selection               |
    v                              |
Python Tool Registry <-------------+
    |
    +--> Flight and Gate Service
    |
    +--> Terminal Routing Service
    |
    +--> Connection Feasibility Service
    |
    +--> Mobility Dispatch Service
    |
    v
SQLite Database
    |
    +--> Flight records
    +--> Terminal maps
    +--> Passenger sessions
    +--> Assistance requests
    +--> Workflow states
    +--> Human decisions
    +--> Activity logs
    |
    v
Human Approval Engine
    |
    v
Coordinator Dashboard
    |
    | Approve / Reject
    v
FastAPI Approval Callback
    |
    v
Persist Decision + Resume Workflow
    |
    v
Passenger Dashboard Updates
    |
    v
Confirmed Status / Next Instructions

## 1.3 Technology stack

| Component | Technology | Purpose |
|---|---|---|
| Programming | Python 3.12 | Main application |
| IDE | PyCharm | Development |
| Frontend | Streamlit | Passenger and coordinator interfaces |
| Backend | FastAPI | REST API and workflow endpoints |
| AI | OpenRouter | LLM access |
| HTTP | HTTPX | Async API communication |
| Database | SQLite | Persistent storage |
| ORM | SQLAlchemy | Database operations |
| Validation | Pydantic | Request and response validation |
| AI schemas | JSON Schema | Structured tool arguments |
| Testing | Pytest | Automated tests |
| Async processing | asyncio | Non-blocking workflow execution |
| Logging | Python logging | Activity and error tracking |
| Configuration | python-dotenv | Environment variables |

### Why this stack?

Streamlit gives us fast dashboard development.

FastAPI gives us a proper backend with asynchronous endpoints and API documentation.

SQLite avoids the need to configure an external database.

OpenRouter lets us change the underlying AI model without rebuilding the agent.

Python performs all operational calculations, so the LLM cannot invent transfer times.

## 1.4 Third-party services and APIs

### Required: OpenRouter

Purpose:
- Natural-language understanding.
- Passenger intent extraction.
- Tool selection.
- Response generation.
- Multilingual response generation where supported.

Use the OpenAI-compatible Chat Completions API through HTTPX.

Endpoint:

https://openrouter.ai/api/v1/chat/completions

Environment variables:

OPENROUTER_API_KEY=
OPENROUTER_MODEL=

The model must support tool calling. Verify the selected model's current tool-calling support before implementation.

Do not hardcode a particular model into business logic.

### Optional: OpenSky Network

Purpose:
- Experimental aircraft tracking.
- Aircraft position or flight movement context, where supported.

Important:
OpenSky data does not automatically provide verified airport gate assignments, boarding cutoffs or mobility dispatch information.

It must never be used as a substitute for an airport's authoritative operational database.

### Required for MVP: Custom synthetic airport dataset

There is no guaranteed public source for the exact airport gate and mobility information required by this challenge.

Build a controlled synthetic airport dataset.

Use the same dataset consistently across all ten demonstration scenarios.

Mark all simulated information clearly in the dashboard.

### External service decision

The MVP must work without any external aviation API.

OpenRouter is the only required external runtime API.

If OpenRouter is unavailable, provide a deterministic mock-agent mode for the demonstration.

---

## 1.5 Separation of AI and deterministic Python

This separation is essential.

### AI responsibilities

- Understand passenger messages.
- Identify passenger intent.
- Extract flight numbers and gate references.
- Identify wheelchair, stroller and family assistance needs.
- Select the appropriate tools.
- Explain verified results in simple language.
- Ask for missing information.

### Python responsibilities

- Validate flight numbers.
- Retrieve flight and gate records.
- Calculate actual distances from the dataset.
- Calculate walking and wheelchair journey estimates.
- Apply mandatory safety buffers.
- Evaluate connection feasibility.
- Create assistance requests.
- Enforce approval requirements.
- Save workflow state.
- Verify human decisions.

### Non-negotiable rule

The LLM must never calculate or invent operational flight timings, terminal distances, wheelchair dispatch confirmations or official connection feasibility.

Those operations must be performed by deterministic Python functions.

---

# 2. COMPLETE FILE-BY-FILE PROJECT STRUCTURE

## 2.1 Repository directory tree

Create the following structure:

SWAGON-AI/
|
|-- PLAN.md
|-- README.md
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- run.py
|
|-- config/
|   |-- settings.py
|   |-- constants.py
|   |-- prompts.py
|
|-- data/
|   |-- airport_terminal.json
|   |-- flights.json
|   |-- mobility_services.json
|   |-- demo_scenarios.json
|
|-- database/
|   |-- __init__.py
|   |-- connection.py
|   |-- models.py
|   |-- repositories.py
|   |-- seed.py
|
|-- backend/
|   |-- __init__.py
|   |-- main.py
|   |-- schemas.py
|   |-- dependencies.py
|   |
|   |-- api/
|   |   |-- __init__.py
|   |   |-- passenger.py
|   |   |-- coordinator.py
|   |   |-- flights.py
|   |   |-- health.py
|   |
|   |-- services/
|       |-- __init__.py
|       |-- passenger_service.py
|       |-- flight_service.py
|       |-- routing_service.py
|       |-- connection_service.py
|       |-- mobility_service.py
|       |-- notification_service.py
|
|-- agent/
|   |-- __init__.py
|   |-- agent.py
|   |-- openrouter_client.py
|   |-- tool_registry.py
|   |-- tool_executor.py
|   |-- conversation.py
|   |-- response_builder.py
|
|-- tools/
|   |-- __init__.py
|   |-- flight_tools.py
|   |-- routing_tools.py
|   |-- connection_tools.py
|   |-- mobility_tools.py
|
|-- workflows/
|   |-- __init__.py
|   |-- state_machine.py
|   |-- approval_engine.py
|   |-- callback_handler.py
|   |-- resume_service.py
|   |-- workflow_repository.py
|
|-- safety/
|   |-- __init__.py
|   |-- validation.py
|   |-- authorization.py
|   |-- operational_guards.py
|
|-- dashboard/
|   |-- Home.py
|   |-- pages/
|   |   |-- 1_Passenger_Assistant.py
|   |   |-- 2_Coordinator_Centre.py
|   |   |-- 3_Operations_Analytics.py
|   |-- components/
|       |-- chat.py
|       |-- flight_card.py
|       |-- request_card.py
|       |-- status_badge.py
|       |-- route_display.py
|
|-- tests/
|   |-- conftest.py
|   |-- test_flight_tools.py
|   |-- test_routing_tools.py
|   |-- test_connection_tools.py
|   |-- test_mobility_tools.py
|   |-- test_approval_workflow.py
|   |-- test_agent_tools.py
|   |-- test_api.py
|   |-- test_scenarios.py
|
|-- docs/
    |-- ARCHITECTURE.md
    |-- API.md
    |-- DEMO_SCRIPT.md
    |-- BUSINESS_MODEL.md

## 2.2 File responsibilities

### Root files

**PLAN.md**
- Master engineering specification.
- Contains project requirements, architecture, implementation rules and acceptance criteria.
- Must be read before making repository changes.

**README.md**
- Project introduction.
- Setup instructions.
- How to start the backend and dashboard.
- Environment setup and demonstration instructions.

**requirements.txt**
- All Python dependencies with compatible version constraints.
- Include Streamlit, FastAPI, Uvicorn, HTTPX, SQLAlchemy, Pydantic, python-dotenv and pytest.

**.env.example**
- Template for OpenRouter credentials and configuration.
- Contains placeholder values only.

**.gitignore**
- Ignore `.env`, virtual environments, Python cache files, generated databases and temporary files.

**run.py**
- Development launcher.
- Provides convenient commands for starting the backend and frontend.
- Must not contain business logic.

### Configuration directory

**config/settings.py**
- Load environment variables.
- Validate required configuration.
- Expose application settings.

**config/constants.py**
- Workflow status constants.
- Passenger assistance categories.
- Connection status categories.
- Application defaults.

**config/prompts.py**
- System prompt for the AI agent.
- Tool usage instructions.
- Safety restrictions.
- Passenger communication style.

### Data directory

**data/airport_terminal.json**
- Terminal layout.
- Gate identifiers.
- Gate coordinates or graph nodes.
- Connections between gates.
- Accessibility information.
- Route restrictions.

**data/flights.json**
- Synthetic inbound and outbound flights.
- Flight numbers.
- Arrival information.
- Current gates.
- Boarding close times.
- Dataset update timestamps.
- Data source labels.

**data/mobility_services.json**
- Mock wheelchair and mobility-cart services.
- Service categories.
- Availability.
- Operational restrictions.

**data/demo_scenarios.json**
- Ten predefined passenger scenarios.
- Input messages.
- Expected extracted intent.
- Expected tool calls.
- Expected deterministic outcomes.

### Database directory

**database/connection.py**
- Create SQLAlchemy engine.
- Manage SQLite connections.
- Provide session management.

**database/models.py**
Define the database models:

1. PassengerSession
2. ConversationMessage
3. Flight
4. TerminalGate
5. MobilityRequest
6. WorkflowRun
7. ApprovalDecision
8. ActivityLog

**database/repositories.py**
- Database read/write functions.
- Flight lookup.
- Request creation.
- Request status updates.
- Workflow state retrieval.
- Activity log retrieval.

**database/seed.py**
- Load the synthetic JSON datasets.
- Populate the SQLite database.
- Avoid duplicate records.
- Support database reset for demonstrations.

### Backend directory

**backend/main.py**
- Create FastAPI application.
- Register routers.
- Configure CORS.
- Initialise database.
- Register application lifecycle events.

**backend/schemas.py**
- Pydantic API request and response schemas.

**backend/dependencies.py**
- Database session dependencies.
- Shared application service dependencies.

### API directory

**passenger.py**
- Receive passenger chat messages.
- Create passenger sessions.
- Return agent responses.
- Return workflow status.

**coordinator.py**
- List pending assistance requests.
- Retrieve request details.
- Approve or reject requests.
- Submit coordinator decisions.

**flights.py**
- Flight lookup endpoint.
- Gate information endpoint.
- Terminal route endpoint.

**health.py**
- Health check.
- Database readiness.
- AI provider connectivity status.

### Services directory

**passenger_service.py**
- Manage passenger requests.
- Coordinate the agent response lifecycle.
- Save conversation messages.

**flight_service.py**
- Retrieve flight information.
- Validate flight status and freshness.

**routing_service.py**
- Resolve terminal routes.
- Retrieve gate-to-gate distance.
- Check accessible routes.

**connection_service.py**
- Apply deterministic transfer calculations.
- Compare estimated transfer requirements with available time.

**mobility_service.py**
- Create mobility requests.
- Validate assistance types.
- Check request status.

**notification_service.py**
- Generate passenger status notifications.
- Publish coordinator updates.
- Support dashboard refresh.

### Agent directory

**agent.py**
- Main agent loop.
- Send passenger messages to OpenRouter.
- Interpret model responses.
- Handle tool calls.
- Return final responses.

**openrouter_client.py**
- HTTPX API client.
- API authentication.
- Request timeout.
- Error handling.
- Retry policy.
- Model configuration.

**tool_registry.py**
- Register available Python tools.
- Define JSON schemas.
- Provide tool descriptions to the LLM.

**tool_executor.py**
- Validate tool names.
- Validate arguments.
- Execute registered Python functions.
- Return structured results.
- Block unknown or unauthorised operations.

**conversation.py**
- Retrieve conversation history.
- Maintain session context.
- Limit context size.

**response_builder.py**
- Convert structured tool results into passenger-friendly responses.
- Include uncertainty and source information.
- Avoid unconfirmed promises.

### Tools directory

**flight_tools.py**

Required function:

get_flight_and_gate_status(flight_number)

Responsibilities:
- Search the flight dataset.
- Return flight information.
- Return gate information.
- Return boarding cutoff information when available.
- Include data source and last-updated timestamp.
- Return a structured error when information is missing.

**routing_tools.py**

Required function:

calculate_terminal_transfer_time(
    origin_gate,
    destination_gate,
    passenger_type,
    accessibility_required
)

Responsibilities:
- Retrieve terminal route.
- Calculate route distance.
- Apply walking or wheelchair speed assumptions.
- Include route-specific delays.
- Apply configured safety buffers.
- Return the estimated journey time.
- Reject unknown or inaccessible routes.

**connection_tools.py**

Required function:

check_connection_feasibility(
    available_minutes,
    estimated_transfer_minutes,
    required_buffers
)

Responsibilities:
- Validate timing values.
- Compare available time with total estimated requirements.
- Return one of:
  - INVALID
  - NOT_FEASIBLE
  - TIGHT_CONNECTION
  - POTENTIALLY_FEASIBLE

The LLM must not override the result.

**mobility_tools.py**

Required function:

request_mobility_dispatch_async(
    passenger_id,
    flight_number,
    assistance_type,
    pickup_location,
    destination,
    reason
)

Responsibilities:
- Validate assistance details.
- Create a persistent request.
- Generate a unique request ID.
- Set status to PENDING.
- Create or associate a workflow run.
- Trigger the human approval workflow.
- Return the pending status to the agent.

The function must not report dispatch as approved.

### Workflow directory

**state_machine.py**
- Define workflow states.
- Define permitted transitions.
- Reject invalid transitions.

Suggested states:

CREATED
ANALYSING
TOOLS_RUNNING
WAITING_HUMAN
APPROVED
REJECTED
RESUMING
COMPLETED
FAILED
TIMED_OUT

**approval_engine.py**
- Create pending approval records.
- Associate coordinator decisions with requests.
- Enforce human approval requirements.

**callback_handler.py**
- Receive approval decisions.
- Validate the decision.
- Persist the result.
- Trigger the workflow resume operation.

**resume_service.py**
- Resume a paused workflow.
- Retrieve saved context.
- Read the human decision.
- Generate the next passenger-facing response.
- Save completion state.

**workflow_repository.py**
- Persist workflow states and checkpoints.
- Retrieve pending workflows.
- Maintain workflow history.

### Safety directory

**validation.py**
- Validate flight numbers.
- Validate gate identifiers.
- Validate transfer times.
- Validate passenger input.

**authorization.py**
- Restrict coordinator operations.
- Verify coordinator identity and permissions.
- Prevent passengers from approving their own requests.

**operational_guards.py**
- Prevent unapproved dispatch.
- Prevent fabricated flight information.
- Enforce safety buffers.
- Prevent the LLM from directly modifying operational records.
- Require authoritative data before issuing definitive operational claims.

### Dashboard directory

**Home.py**
- Landing page.
- Product introduction.
- Navigation.
- System status.

**1_Passenger_Assistant.py**
- Passenger chat.
- Flight details.
- Gate information.
- Transfer estimates.
- Assistance status.
- Workflow updates.

**2_Coordinator_Centre.py**
- Pending assistance requests.
- Passenger details.
- Flight information.
- Approval and rejection controls.
- Decision history.

**3_Operations_Analytics.py**
- Total requests.
- Pending requests.
- Approved and rejected requests.
- Average processing time.
- Flight connection alerts.
- Request distribution.

### Dashboard components

**chat.py**
- Chat history.
- User input.
- AI response rendering.

**flight_card.py**
- Flight number.
- Origin and destination.
- Gate.
- Boarding cutoff.
- Data freshness.

**request_card.py**
- Passenger assistance details.
- Request ID.
- Approval controls.

**status_badge.py**
- Pending.
- Approved.
- Rejected.
- Completed.

**route_display.py**
- Origin and destination.
- Route steps.
- Estimated distance.
- Estimated transfer time.

### Testing directory

Each test file should focus on one subsystem.

**conftest.py**
- Shared fixtures.
- Temporary SQLite database.
- Test application configuration.

**test_flight_tools.py**
- Valid and invalid flight lookups.
- Missing gate data.
- Stale information.

**test_routing_tools.py**
- Walking routes.
- Wheelchair routes.
- Unknown gates.
- Inaccessible routes.

**test_connection_tools.py**
- Connection calculations.
- Invalid timing.
- Safety buffers.

**test_mobility_tools.py**
- Request creation.
- Required fields.
- Duplicate submissions.
- Initial pending status.

**test_approval_workflow.py**
- Approval callback.
- Rejection callback.
- Workflow resumption.
- Invalid state transitions.
- Timeout handling.

**test_agent_tools.py**
- Tool selection.
- Argument validation.
- Tool execution.
- LLM error handling.

**test_api.py**
- API endpoints.
- HTTP responses.
- Authentication and authorisation.

**test_scenarios.py**
- Ten complete end-to-end passenger scenarios.

### Documentation directory

**ARCHITECTURE.md**
- Architecture diagrams.
- Data flow.
- Component interactions.

**API.md**
- API endpoint documentation.
- Request and response examples.

**DEMO_SCRIPT.md**
- Competition demonstration steps.
- Passenger scenario.
- Coordinator actions.
- Expected results.

**BUSINESS_MODEL.md**
- Target customers.
- Revenue streams.
- Subscription packages.
- Cost assumptions.
- Future commercial deployment.

---

# 3. DATABASE DESIGN

## 3.1 Database

Database name:

airport_terminal_journey.sqlite

Use SQLite with SQLAlchemy.

## 3.2 Required tables

### Table: flights

Fields:
- id
- flight_number
- airline
- origin
- destination
- arrival_gate
- departure_gate
- scheduled_arrival
- estimated_arrival
- boarding_close_time
- status
- data_source
- last_updated

### Table: terminal_gates

Fields:
- id
- gate_code
- terminal
- concourse
- x_coordinate
- y_coordinate
- accessible
- connected_nodes

### Table: mobility_requests

Fields:
- id
- passenger_id
- flight_number
- assistance_type
- pickup_location
- destination
- reason
- priority
- status
- coordinator_id
- created_at
- updated_at

### Table: workflow_runs

Fields:
- id
- session_id
- request_id
- current_state
- checkpoint_data
- created_at
- updated_at

### Table: approval_decisions

Fields:
- id
- request_id
- coordinator_id
- decision
- comments
- created_at

### Table: conversation_messages

Fields:
- id
- session_id
- role
- content
- created_at

### Table: activity_logs

Fields:
- id
- event_type
- description
- session_id
- workflow_id
- created_at

Add primary keys, foreign keys, indexes and appropriate constraints.

Do not store OpenRouter API keys in the database.

---

# 4. ASYNCHRONOUS HUMAN-IN-THE-LOOP ARCHITECTURE

This is a mandatory competition requirement.

## 4.1 Workflow

1. Passenger submits an assistance request.
2. AI determines the assistance required.
3. Python validates the request.
4. Mobility request is inserted into SQLite.
5. Workflow changes to WAITING_HUMAN.
6. Agent returns a pending status to the passenger.
7. Coordinator dashboard displays the request.
8. Coordinator approves or rejects it.
9. FastAPI receives the callback.
10. Decision is stored in SQLite.
11. Callback handler triggers workflow resumption.
12. Passenger interface retrieves the updated result.

## 4.2 Important engineering decision

Do not implement asynchronous approval by keeping the passenger's HTTP request open while waiting for a person.

Instead, persist the workflow checkpoint and return a pending response immediately.

Use a database-backed workflow state machine.

When the coordinator submits a decision, the backend invokes the resume service as an asynchronous background task.

The database remains the source of truth.

The passenger dashboard polls the workflow status endpoint.

This makes the workflow resilient to page refreshes and backend restarts.

## 4.3 Approval endpoint

POST /api/coordinator/requests/{request_id}/decision

Example request:

{
  "decision": "APPROVED",
  "comments": "Demo coordinator approved the request."
}

Possible decisions:

APPROVED
REJECTED

The backend must:
- Authenticate the coordinator.
- Validate the decision.
- Confirm the request is still pending.
- Store the decision.
- Update the request status.
- Trigger workflow resumption.
- Return the updated status.

## 4.4 Safety rules

- AI cannot approve mobility dispatch.
- AI cannot claim a request has been dispatched when it is only pending.
- AI cannot approve gate holds.
- Gate holds require an authorised human decision and the relevant airline or airport operational authority.
- A rejected request must never be presented as approved.
- Duplicate approval callbacks must be rejected safely.
- Every decision must be recorded.

For the hackathon, coordinator authentication can use a seeded demonstration account with a simple login. Clearly identify this as prototype authentication, not production-grade airport security.

---

# 5. API DESIGN

## 5.1 Passenger APIs

POST /api/passenger/chat

Receives:
- session_id
- message

Returns:
- response
- session_id
- tool_activity
- workflow_status
- request_id, if applicable

GET /api/passenger/workflows/{workflow_id}

Returns:
- workflow status
- request status
- approval information
- latest passenger message

GET /api/passenger/sessions/{session_id}/history

Returns conversation history.

## 5.2 Flight APIs

GET /api/flights/{flight_number}

Returns flight and gate information.

GET /api/flights/{flight_number}/connection

Returns the relevant connecting-flight information when available.

POST /api/routes/calculate

Receives:
- origin_gate
- destination_gate
- passenger_type
- accessibility_required

Returns:
- route
- distance
- estimated time
- applied buffers
- accessibility status

## 5.3 Coordinator APIs

GET /api/coordinator/requests

Returns all assistance requests.

GET /api/coordinator/requests/pending

Returns pending requests.

GET /api/coordinator/requests/{request_id}

Returns request details.

POST /api/coordinator/requests/{request_id}/decision

Processes the human approval callback.

## 5.4 System APIs

GET /api/health

Returns:
- backend status
- database status
- OpenRouter configuration status

GET /api/health/ai

Checks the configured AI provider.

Do not expose API keys or sensitive configuration in health responses.

---

# 6. AI AGENT IMPLEMENTATION

## 6.1 OpenRouter integration

Use an OpenAI-compatible HTTPX client.

Agent interaction:

Passenger message
    |
    v
OpenRouter Chat Completions
    |
    v
Model returns normal response or tool call
    |
    v
Validate tool name and arguments
    |
    v
Execute Python tool
    |
    v
Send tool result back to model
    |
    v
Model produces passenger response

## 6.2 Agent system prompt requirements

The agent must:

- Behave as an airport passenger assistance agent.
- Communicate politely and clearly.
- Understand stressful passenger situations.
- Extract flight numbers and gate references.
- Identify accessibility requirements.
- Request missing information when necessary.
- Use tools to retrieve operational information.
- Never invent flight status or terminal distances.
- Never invent official boarding cutoff times.
- Never perform its own connection-time calculations.
- Respect the Python feasibility result.
- Create mobility requests only when justified.
- Explain that physical assistance is pending until human approval.
- Use the callback result before announcing approval.
- Never promise that a flight will be held.
- Clearly distinguish estimated, simulated and confirmed information.

## 6.3 Tool-calling configuration

Register the following tools:

1. get_flight_and_gate_status
2. calculate_terminal_transfer_time
3. check_connection_feasibility
4. request_mobility_dispatch_async

Each tool must have:
- A unique name.
- A clear description.
- A strict JSON argument schema.
- A Python implementation.
- A validated structured return value.

Set a reasonable maximum number of tool iterations.

Handle malformed tool calls, repeated calls, unavailable models and API errors.

Do not let the LLM directly execute arbitrary Python code or SQL.

---

# 7. STEP-BY-STEP BUILD ORDER

Development must follow the sequence below.

The first objective is to get one working passenger-to-coordinator-to-passenger journey running as early as possible.

## PHASE 1 — PROJECT SETUP

Priority: MUST HAVE

Tasks:

1. Create the Swagon-AI project in PyCharm.
2. Configure Python 3.12 virtual environment.
3. Create the directory structure.
4. Create requirements.txt.
5. Install dependencies.
6. Create .env.example.
7. Configure OpenRouter API credentials.
8. Test the OpenRouter connection.
9. Create FastAPI health endpoint.
10. Create basic Streamlit landing page.

Deliverable:

A working backend and frontend.

Acceptance criteria:

- Application starts without import errors.
- FastAPI health endpoint works.
- Streamlit loads.
- OpenRouter connectivity is verified.
- API keys are not exposed.

HUMAN CHECKPOINT 1:

The coding agent must stop.

Our team must:
- Open the project in PyCharm.
- Create the virtual environment.
- Supply the OpenRouter API key locally.
- Choose the initial model.
- Run the health check.
- Confirm the setup works.

Do not continue until we approve.

## PHASE 2 — DATASET AND DATABASE

Priority: MUST HAVE

Tasks:

1. Create synthetic airport terminal data.
2. Create synthetic flight records.
3. Create mobility service records.
4. Create ten demonstration scenarios.
5. Design SQLAlchemy models.
6. Create SQLite database.
7. Implement database repositories.
8. Create seed script.
9. Test database loading.
10. Add dataset source and freshness fields.

Deliverable:

A functioning airport database with repeatable demonstration data.

Acceptance criteria:

- Flight records can be retrieved.
- Gate records can be retrieved.
- Route information exists.
- Mobility requests can be stored.
- Database can be reset and seeded.
- No duplicate records are created during repeated seeding.

HUMAN CHECKPOINT 2:

Our team reviews:
- Airport terminal layout.
- Flight numbers.
- Gate assignments.
- Boarding cutoff values.
- Sample wheelchair routes.
- Ten demonstration scenarios.

The team approves the synthetic data before AI integration.

## PHASE 3 — CORE PYTHON TOOLS

Priority: MUST HAVE

Build tools independently of OpenRouter.

Implementation order:

1. get_flight_and_gate_status()
2. calculate_terminal_transfer_time()
3. check_connection_feasibility()
4. request_mobility_dispatch_async()

Then create the tool registry.

Deliverable:

All Python tools operate independently and return structured data.

Acceptance criteria:

- Valid flight lookup succeeds.
- Invalid flight lookup returns an error.
- Route distance comes from the dataset.
- Wheelchair route accessibility is checked.
- Walking and wheelchair calculations are deterministic.
- Safety buffers are applied.
- Assistance requests begin in PENDING state.

HUMAN CHECKPOINT 3:

Our team manually checks:
- Sample distances.
- Walking speed assumptions.
- Wheelchair speed assumptions.
- Family and accessibility buffers.
- Feasibility classifications.

Do not allow the coding agent to invent or modify these values without approval.

## PHASE 4 — AI AGENT AND OPENROUTER

Priority: MUST HAVE

Tasks:

1. Implement OpenRouter HTTPX client.
2. Add system prompt.
3. Register Python tools.
4. Implement tool-calling loop.
5. Parse tool arguments.
6. Validate tool calls.
7. Execute tools.
8. Return results to the model.
9. Generate passenger responses.
10. Store conversation history.

Deliverable:

A working AI agent that can understand passenger requests and invoke Python tools.

Acceptance criteria:

- Agent understands the DXB-402 scenario.
- Agent detects wheelchair assistance.
- Agent retrieves flight data.
- Agent retrieves route data.
- Agent uses Python feasibility results.
- Agent does not invent operational details.
- Tool failures produce safe responses.

HUMAN CHECKPOINT 4:

Our team tests actual passenger messages.

Review:
- Whether the agent understands the request.
- Whether the correct tools are selected.
- Whether the model produces reliable structured arguments.
- Whether the responses are understandable.
- Whether hallucinations are prevented.

If the selected model fails tool calling, change the model before adding more features.

## PHASE 5 — ASYNCHRONOUS APPROVAL ENGINE

Priority: MUST HAVE

Tasks:

1. Define workflow state machine.
2. Create workflow repository.
3. Create pending mobility requests.
4. Persist workflow checkpoints.
5. Implement approval endpoint.
6. Implement callback handler.
7. Implement workflow resume service.
8. Add coordinator identity checks.
9. Add duplicate-decision protection.
10. Add passenger status retrieval.
11. Add timeout and failure handling.

Deliverable:

A genuine database-backed asynchronous approval workflow.

Acceptance criteria:

- Request begins as PENDING.
- Agent does not claim approval.
- Coordinator receives the request.
- Approval changes status to APPROVED.
- Rejection changes status to REJECTED.
- Callback resumes the associated workflow.
- Passenger can retrieve the updated result.
- Restarting the backend does not erase pending requests.

HUMAN CHECKPOINT 5:

Our team performs the approval test manually.

1. Submit a wheelchair request.
2. Open the coordinator dashboard.
3. Approve the request.
4. Return to the passenger dashboard.
5. Verify the updated status.

Repeat with rejection.

Do not proceed until both paths work.

## PHASE 6 — FRONTEND DASHBOARDS

Priority: MUST HAVE

Build three interfaces.

### A. Passenger assistant

Design:
- Light blue and white theme.
- Clean airport-inspired layout.
- Chat interface.
- Flight information card.
- Route information.
- Accessibility request card.
- Approval status.
- Refresh or automatic status updates.

### B. Coordinator centre

Design:
- Pending request counter.
- Request list.
- Passenger information.
- Flight information.
- Assistance requirements.
- Approve and reject controls.
- Decision history.

### C. Operations analytics

Design:
- Total passenger requests.
- Pending requests.
- Approved requests.
- Rejected requests.
- Connection alerts.
- Average request processing time.

Deliverable:

A coordinated three-page Streamlit application.

Acceptance criteria:

- Passenger can submit a message.
- Passenger receives an AI response.
- Coordinator can view requests.
- Coordinator can approve or reject.
- Passenger sees the updated result.
- Both dashboards display consistent database information.

HUMAN CHECKPOINT 6:

Our team reviews the wireframes and actual dashboards.

Approve:
- Colours.
- Page layout.
- Navigation.
- Flight cards.
- Coordinator request cards.
- Mobile and desktop usability.

Keep the design professional, simple and airport-oriented, not futuristic.

## PHASE 7 — TESTING AND VALIDATION

Priority: MUST HAVE

Tasks:

1. Test all individual tools.
2. Test agent tool calling.
3. Test approval callbacks.
4. Test API endpoints.
5. Test database persistence.
6. Test ten complete passenger scenarios.
7. Test invalid and missing information.
8. Test OpenRouter failure handling.
9. Test repeated approval submissions.
10. Test dashboard refresh.

Deliverable:

A stable demonstration application.

HUMAN CHECKPOINT 7:

Our team runs the ten scenarios and signs off the results.

No fabricated flight data or false approval statuses are acceptable.

## PHASE 8 — BUSINESS AND DEMO POLISH

Priority: MUST HAVE FOR PRESENTATION

Tasks:

1. Add product branding.
2. Add demonstration mode indicator.
3. Add AI activity display.
4. Add clear source labels.
5. Add workflow visualisation.
6. Add request history.
7. Prepare business model page.
8. Prepare demonstration script.
9. Prepare architecture diagram.
10. Prepare presentation slides.

Deliverable:

Competition-ready Swagon AI.

HUMAN CHECKPOINT 8:

Our team conducts a complete timed rehearsal and decides whether there is enough time for stretch goals.

---

# 8. MUST-HAVE MVP VS STRETCH FEATURES

## 8.1 Must-have

These must work before competition presentation:

- OpenRouter connection.
- Natural-language passenger interface.
- Flight and gate lookup.
- Terminal routing.
- Walking transfer calculations.
- Wheelchair transfer calculations.
- Deterministic connection feasibility.
- Mobility dispatch request.
- Persistent SQLite storage.
- Async human approval callback.
- Workflow resumption.
- Passenger dashboard.
- Coordinator dashboard.
- Ten test scenarios.

## 8.2 Stretch goals

Only add these after the mandatory requirements pass.

### Stretch 1: Baggage and mobility equipment tracker

- Simulate baggage or wheelchair delivery status.
- Notify families when delivery is delayed.
- Display equipment status.

### Stretch 2: Family-friendly amenity recommender

- Recommend family facilities.
- Recommend quiet rooms.
- Provide nearby amenity information.

### Stretch 3: Multilingual accessibility guidance

- Support selected passenger languages.
- Generate simple route instructions.
- Add text-to-speech or audio guidance.

### Stretch 4: Interactive terminal map

- Visualise gates.
- Display the route.
- Mark accessible paths.
- Show passenger destination.

### Stretch 5: Operational analytics

- Request patterns.
- Assistance demand.
- Response time.
- Connection risk distribution.

Scope rule: If the mandatory workflow is not fully functional, do not build stretch goals.

---

# 9. HUMAN-IN-THE-LOOP CHECKPOINT POLICY

The AI coding agent must operate incrementally.

It must never silently make major architecture changes.

At each checkpoint:

1. Stop implementation.
2. Summarise completed work.
3. List files created or modified.
4. Report tests executed.
5. Report failures.
6. Ask the team to approve the next phase.

The agent must not:
- Delete working functionality without approval.
- Replace SQLite with another database without approval.
- Replace OpenRouter with another AI provider without approval.
- Rewrite the frontend framework without approval.
- Invent airport operational data.
- Disable safety checks to make tests pass.
- claim a feature is complete without running its tests.

If a requirement is ambiguous, ask before making a major design decision.

---

# 10. BUSINESS MODEL ARCHITECTURE

## 10.1 Product positioning

Swagon AI is an airport passenger assistance and operational coordination platform.

It is designed to connect passengers, airline information and airport assistance staff through one intelligent workflow.

## 10.2 Target customers

Primary:
- International airports.
- Airport ground-handling companies.
- Airline customer-service operations.

Secondary:
- Airport accessibility service providers.
- Airport technology integrators.

## 10.3 Revenue model

Business-to-business SaaS.

Proposed subscription assumptions:

Starter: AED 3,000/month

Professional: AED 8,000/month

Enterprise: AED 20,000+/month

These are hypothetical presentation prices, not verified industry quotations.

## 10.4 Revenue streams

- Monthly software subscriptions.
- Airport integration services.
- Custom dashboard development.
- Annual maintenance.
- Advanced analytics packages.

## 10.5 Main competitive advantage

Swagon AI is not just a flight information chatbot.

It combines:
- Natural-language passenger understanding.
- Deterministic connection calculations.
- Accessibility-focused routing.
- Human-controlled mobility dispatch.
- Persistent workflow management.
- Passenger and coordinator communication.

## 10.6 Commercial expansion

The first commercial step would be a controlled pilot with an airport or ground-handling partner.

A real deployment would require:
- Authoritative flight and gate data.
- Airport system integration.
- Staff authentication.
- Cybersecurity approval.
- Accessibility validation.
- Operational and legal review.
- Reliability and performance testing.

The competition prototype must not be represented as an officially integrated airport system.

---

# 11. TESTING REQUIREMENTS

## 11.1 Ten required demonstration scenarios

Create ten repeatable scenarios.

1. Normal connecting passenger with sufficient time.
2. Passenger with a sudden gate change.
3. Wheelchair passenger with a tight connection.
4. Family travelling with a stroller.
5. Passenger with an unknown flight number.
6. Passenger with an unknown destination gate.
7. Wheelchair passenger with no verified accessible route.
8. Connection with insufficient transfer time.
9. Mobility request approved by coordinator.
10. Mobility request rejected by coordinator.

For each scenario, record:

- Input message.
- Expected passenger intent.
- Expected Python tools.
- Expected tool arguments.
- Expected results.
- Expected workflow state.
- Expected passenger response.

The first eight test operational and routing correctness. The last two explicitly test the human approval lifecycle.

## 11.2 Testing rules

- Use a deterministic test dataset.
- Do not rely on random LLM output for expected calculations.
- Mock OpenRouter calls in automated unit tests.
- Test the actual OpenRouter integration separately.
- Use a temporary database for tests.
- Test both successful and unsuccessful outcomes.

---

# 12. DEMONSTRATION PLAN

## Competition presentation sequence

### Step 1 — Introduce the problem

Explain that families with reduced-mobility passengers can face serious difficulties when flight gates change unexpectedly.

### Step 2 — Enter passenger message

Use the DXB-402 scenario.

### Step 3 — Show the AI agent

Show how it identifies:
- Inbound flight.
- Connecting flight.
- New gate.
- Wheelchair requirement.
- Available time.

### Step 4 — Show Python execution

Display:
- Flight lookup.
- Gate lookup.
- Route calculation.
- Transfer estimate.
- Connection feasibility.

### Step 5 — Show pending approval

Display the mobility request ID and PENDING status.

### Step 6 — Open coordinator dashboard

Show the request and approve it.

### Step 7 — Return to passenger dashboard

Show the updated APPROVED status and passenger notification.

### Step 8 — Explain the business model

Explain how airports or airport service companies could subscribe to the platform.

### Step 9 — Show the architecture

Highlight the separation between LLM intelligence, deterministic Python tools and human decision-making.

### Step 10 — Show testing

Demonstrate that all ten scenarios have been tested.

---

# 13. DEFINITION OF DONE

The project is complete when all the following are true:

[ ] PyCharm project runs successfully.

[ ] OpenRouter connection works.

[ ] Passenger dashboard works.

[ ] Coordinator dashboard works.

[ ] FastAPI backend works.

[ ] SQLite database persists information.

[ ] Synthetic airport dataset is loaded.

[ ] Flight lookup works.

[ ] Terminal route calculation works.

[ ] Wheelchair calculation works.

[ ] Connection feasibility is deterministic.

[ ] Mobility requests are created correctly.

[ ] Human approval callback works.

[ ] Workflow resumes after approval.

[ ] Rejection workflow works.

[ ] Passenger status updates correctly.

[ ] Ten scenarios pass.

[ ] Error handling works.

[ ] API keys are protected.

[ ] Competition demonstration is rehearsed.

Only mark the project complete when the relevant tests have actually passed.

---

# 14. GLOBAL RULES FOR THE AI CODING AGENT

1. Read PLAN.md before starting any implementation.
2. Follow the defined directory structure.
3. Build one phase at a time.
4. Use Python as the source of truth for operational calculations.
5. Use OpenRouter for LLM communication.
6. Keep the code modular and beginner-readable.
7. Add type hints to functions.
8. Add docstrings to important services.
9. Use Pydantic validation for API inputs.
10. Use SQLAlchemy for database access.
11. Use HTTPX for asynchronous external requests.
12. Never expose API keys.
13. Never hardcode operational claims into AI responses.
14. Never allow an LLM to approve physical assistance.
15. Preserve all previously working functionality.
16. Run tests after meaningful changes.
17. Stop at every human checkpoint.
18. Report exact commands to run.
19. Explain setup errors in beginner-friendly language.
20. Do not generate unnecessary features before the MVP works.

**Final development priority:**

A working passenger message → AI tool selection → Python flight and route calculations → mobility request → human approval callback → workflow resumption → passenger update.

Everything else is secondary.