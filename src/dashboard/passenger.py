
import streamlit as st

from agent import run_agent

from database.db import (
    initialise_database,
    get_request,
    get_crime_report,
    get_medical_request
)

from dashboard.theme import apply_theme, badge, feature_header

st.set_page_config(
    page_title="SkyLink AI Passenger",
    page_icon="✈️",
    layout="wide"
)

initialise_database()

apply_theme("passenger")

st.title("✈️ SkyLink AI")
st.caption(
    "Your intelligent airport journey assistant"
)

st.info(
    "Demonstration environment: "
    "All flight and airport data is simulated."
)

st.error(
    "**Emergency?** If anyone is in danger or a medical "
    "situation is life-threatening, alert the nearest airport "
    "staff or call the local emergency number immediately. "
    "Do not wait for an online request to be approved."
)

if "chat" not in st.session_state:
    st.session_state.chat = []

if "submissions" not in st.session_state:
    st.session_state.submissions = []

if "queued_prompt" not in st.session_state:
    st.session_state.queued_prompt = None

# ---------------------------------------------------------------
# Quick actions
# ---------------------------------------------------------------

st.subheader("How can we help?")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🦽 Mobility assistance", use_container_width=True):
        st.session_state.queued_prompt = (
            "I need mobility assistance for my connection."
        )

with col2:
    if st.button("🚨 Report a crime", use_container_width=True):
        st.session_state.queued_prompt = (
            "I would like to report a crime or security concern."
        )

with col3:
    if st.button("🩺 Medical assistance", use_container_width=True):
        st.session_state.queued_prompt = (
            "I need medical assistance."
        )

# ---------------------------------------------------------------
# Chat
# ---------------------------------------------------------------

st.subheader("Passenger Assistance")

for message in st.session_state.chat:

    with st.chat_message(message["role"]):
        st.write(message["content"])

typed = st.chat_input(
    "How can we help with your airport journey?"
)

prompt = typed or st.session_state.queued_prompt
st.session_state.queued_prompt = None

if prompt:

    history = list(st.session_state.chat)

    st.session_state.chat.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Checking your journey..."):

            result = run_agent(prompt, history)

            st.write(result["answer"])

            for item in result.get("submissions", []):
                st.session_state.submissions.append(item)

            with st.expander("AI tool activity"):

                for item in result["activity"]:

                    st.write("Tool:", item["tool"])
                    st.json(item["result"])

    st.session_state.chat.append({
        "role": "assistant",
        "content": result["answer"]
    })

st.divider()

# ---------------------------------------------------------------
# Status of submissions
# ---------------------------------------------------------------

st.subheader("My Requests")

if st.button("Refresh status"):
    st.rerun()

subs = st.session_state.submissions

if not subs:
    st.caption("No requests submitted in this session.")

for sub in reversed(subs):

    if sub["type"] == "mobility":

        request = get_request(sub["id"])
        feature_header(f"🦽 Mobility request #{sub['id']}", "mobility")

        if not request:
            st.error("Request not found.")
            continue

        status = request[7]
        st.markdown(
            f"Flight **{request[2]}** · {badge(status)}",
            unsafe_allow_html=True
        )

        if status == "PENDING":
            st.warning("Waiting for airport coordinator approval.")
        elif status == "APPROVED":
            st.success("Mobility assistance request approved.")
            st.write("Coordinator:", request[8])
        elif status == "REJECTED":
            st.error("Mobility assistance request was rejected.")
            st.write("Please contact airport assistance staff.")

    elif sub["type"] == "crime":

        report = get_crime_report(sub["id"])
        feature_header(f"🚨 Crime report #{sub['id']}", "crime")

        if not report:
            st.error("Report not found.")
            continue

        status = report[6]
        st.markdown(
            f"{report[2].replace('_', ' ').title()} at "
            f"**{report[3]}** · {badge(status)}",
            unsafe_allow_html=True
        )

        if status == "PENDING":
            st.warning("Submitted. Waiting for security review.")
        elif status == "ACKNOWLEDGED":
            st.info("Security has acknowledged your report.")
        elif status == "ESCALATED":
            st.info("Your report has been escalated to security.")
        elif status == "CLOSED":
            st.success("Your report has been reviewed and closed.")

        if status != "PENDING":
            st.write("Coordinator:", report[7])

    elif sub["type"] == "medical":

        med = get_medical_request(sub["id"])
        feature_header(f"🩺 Medical request #{sub['id']}", "medical")

        if not med:
            st.error("Request not found.")
            continue

        status = med[6]
        st.markdown(
            f"At **{med[2]}** · Urgency {badge(med[4])} · "
            f"{badge(status)}",
            unsafe_allow_html=True
        )

        if status == "PENDING":
            st.warning(
                "Waiting for coordinator confirmation. "
                "If life-threatening, call the local emergency "
                "number or alert the nearest staff now."
            )
        elif status == "DISPATCHED":
            st.success("A medical team has been dispatched.")
        elif status == "RESOLVED":
            st.success("This request has been marked resolved.")
        elif status == "UNABLE_TO_DISPATCH":
            st.error(
                "We could not dispatch help for this request. "
                "Please alert the nearest staff or call the "
                "local emergency number now."
            )

        if status != "PENDING":
            st.write("Coordinator:", med[7])
