
import streamlit as st

from agent import run_agent

from database.db import (
    initialise_database,
    get_request
)

st.set_page_config(
    page_title="SkyLink AI Passenger",
    page_icon="✈️",
    layout="wide"
)

initialise_database()

st.markdown("""
<style>
.stApp {
    background: #F3F8FD;
}
h1, h2, h3 {
    color: #173D60;
}
</style>
""", unsafe_allow_html=True)

st.title("✈️ SkyLink AI")
st.caption(
    "Your intelligent airport journey assistant"
)

st.info(
    "Demonstration environment: "
    "All flight and airport data is simulated."
)

st.subheader("Passenger Assistance")

if "chat" not in st.session_state:
    st.session_state.chat = []

if "request_id" not in st.session_state:
    st.session_state.request_id = None

for message in st.session_state.chat:

    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input(
    "How can we help with your airport journey?"
)

if prompt:

    st.session_state.chat.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Checking your journey..."):

            result = run_agent(prompt)

            st.write(result["answer"])

            if result.get("request_id"):

                st.session_state.request_id = (
                    result["request_id"]
                )

            with st.expander("AI tool activity"):

                for item in result["activity"]:

                    st.write("Tool:", item["tool"])
                    st.json(item["result"])

    st.session_state.chat.append({
        "role": "assistant",
        "content": result["answer"]
    })

st.divider()

st.subheader("Mobility Assistance Status")

request_id = st.session_state.request_id

if request_id:

    request = get_request(request_id)

    if request:

        st.write("Request ID:", request[0])
        st.write("Passenger:", request[1])
        st.write("Flight:", request[2])

        status = request[7]

        if status == "PENDING":
            st.warning(
                "Waiting for airport coordinator approval."
            )

        elif status == "APPROVED":
            st.success(
                "Mobility assistance request approved."
            )

            st.write(
                "Coordinator:", request[8]
            )

        elif status == "REJECTED":
            st.error(
                "Mobility assistance request was rejected."
            )

            st.write(
                "Please contact airport assistance staff."
            )

    else:
        st.error("Request not found.")

else:
    st.caption(
        "No mobility request has been submitted in this session."
    )

if st.button("Refresh assistance status"):

    st.rerun()
