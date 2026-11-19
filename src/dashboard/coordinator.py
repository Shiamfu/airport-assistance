import streamlit as st
import pandas as pd

from database.db import (
    initialise_database,
    get_requests,
    update_request,
    get_logs
)

st.set_page_config(
    page_title="SkyLink AI Coordinator",
    page_icon="🛫",
    layout="wide"
)

initialise_database()

st.markdown("""
<style>
.stApp {
    background: #E75480;
}
h1, h2, h3 {
    color: #ADD8E6;
}
</style>
""", unsafe_allow_html=True)

st.title("🛫 Airport Coordinator Centre")

st.caption(
    "TEAM SOARING CRESCENT | SKYLINK AI"
)

st.info(
    "Simulated airport coordination environment."
)

coordinator = st.text_input(
    "Coordinator name",
    value="Demo Coordinator"
)

if st.button("Refresh requests"):
    st.rerun()

requests = get_requests()

if requests:

    df = pd.DataFrame(
        requests,
        columns=[
            "ID",
            "Passenger",
            "Flight",
            "Origin",
            "Destination",
            "Assistance",
            "Reason",
            "Status",
            "Coordinator",
            "Created",
            "Updated"
        ]
    )

    st.subheader("Mobility Requests")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    pending = [
        row for row in requests
        if row[7] == "PENDING"
    ]

    st.metric(
        "Pending requests",
        len(pending)
    )

    st.divider()

    st.subheader("Review Requests")

    for request in pending:

        request_id = request[0]

        with st.expander(
            f"Request #{request_id} – {request[1]}"
        ):

            st.write("Flight:", request[2])

            st.write(
                "Route:",
                request[3],
                "→",
                request[4]
            )

            st.write(
                "Assistance:",
                request[5]
            )

            st.write(
                "Reason:",
                request[6]
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Approve",
                    key=f"approve_{request_id}"
                ):

                    update_request(
                        request_id,
                        "APPROVED",
                        coordinator
                    )

                    st.success("Approval recorded.")
                    st.rerun()

            with col2:

                if st.button(
                    "Reject",
                    key=f"reject_{request_id}"
                ):

                    update_request(
                        request_id,
                        "REJECTED",
                        coordinator
                    )

                    st.warning("Rejection recorded.")
                    st.rerun()

else:

    st.info("No requests received yet.")

st.divider()

st.subheader("AI Activity Logs")

logs = get_logs()

if logs:

    log_df = pd.DataFrame(
        logs,
        columns=[
            "ID",
            "Event",
            "Details",
            "Timestamp"
        ]
    )

    st.dataframe(
        log_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.caption("No activity recorded yet.")
