import streamlit as st
import pandas as pd

from database.db import (
    initialise_database,
    get_requests,
    update_request,
    get_logs,
    get_crime_reports,
    update_crime_report,
    get_medical_requests,
    update_medical_request,
    CRIME_COLUMNS,
    MEDICAL_COLUMNS,
    CRIME_TRANSITIONS,
    MEDICAL_TRANSITIONS
)

from dashboard.theme import apply_theme, badge, feature_header

st.set_page_config(
    page_title="SkyLink AI Coordinator",
    page_icon="🛫",
    layout="wide"
)

initialise_database()

apply_theme("coordinator")

st.title("🛫 Airport Coordinator Centre")

st.caption(
    "TEAM SOARING CRESCENT | GENX AI"
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
crimes = get_crime_reports()
medicals = get_medical_requests()

pending_mobility = [r for r in requests if r[7] == "PENDING"]
pending_crime = [r for r in crimes if r[6] == "PENDING"]
pending_medical = [r for r in medicals if r[6] == "PENDING"]
critical = [r for r in pending_medical if r[4] in ("HIGH", "CRITICAL")]

m1, m2, m3, m4 = st.columns(4)
m1.metric("🦽 Pending mobility", len(pending_mobility))
m2.metric("🚨 Pending crime reports", len(pending_crime))
m3.metric("🩺 Pending medical", len(pending_medical))
m4.metric("⚠️ High/critical medical", len(critical))

if critical:
    st.error(
        f"{len(critical)} high/critical medical request(s) "
        "awaiting action. Review the Medical tab now."
    )

URGENCY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}

tab_mob, tab_crime, tab_med, tab_logs = st.tabs([
    "🦽 Mobility",
    "🚨 Crime reports",
    "🩺 Medical assistance",
    "🧾 AI logs"
])

# ---------------------------------------------------------------
# Mobility
# ---------------------------------------------------------------

with tab_mob:

    feature_header("Mobility Requests", "mobility")

    if requests:

        df = pd.DataFrame(
            requests,
            columns=[
                "ID", "Passenger", "Flight", "Origin",
                "Destination", "Assistance", "Reason",
                "Status", "Coordinator", "Created", "Updated"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Review Requests")

        if not pending_mobility:
            st.caption("Nothing waiting for review.")

        for request in pending_mobility:

            request_id = request[0]

            with st.expander(
                f"Request #{request_id} – {request[1]}"
            ):

                st.write("Flight:", request[2])
                st.write("Route:", request[3], "→", request[4])
                st.write("Assistance:", request[5])
                st.write("Reason:", request[6])

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "Approve",
                        key=f"approve_{request_id}"
                    ):
                        update_request(
                            request_id, "APPROVED", coordinator
                        )
                        st.rerun()

                with col2:
                    if st.button(
                        "Reject",
                        key=f"reject_{request_id}"
                    ):
                        update_request(
                            request_id, "REJECTED", coordinator
                        )
                        st.rerun()

    else:
        st.info("No requests received yet.")

# ---------------------------------------------------------------
# Crime reports
# ---------------------------------------------------------------

with tab_crime:

    feature_header("Crime Reports", "crime")

    if crimes:

        df = pd.DataFrame(crimes, columns=CRIME_COLUMNS)
        df["In progress"] = df["In progress"].map(
            {1: "YES", 0: "no"}
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Review Reports")

        open_reports = [
            r for r in crimes if r[6] in CRIME_TRANSITIONS
        ]

        # In-progress incidents first, then newest
        open_reports.sort(key=lambda r: (not r[5], -r[0]))

        if not open_reports:
            st.caption("No open reports.")

        for r in open_reports:

            flag = "🔴 IN PROGRESS · " if r[5] else ""

            with st.expander(
                f"{flag}Report #{r[0]} – "
                f"{r[2].replace('_', ' ').title()} ({r[6]})"
            ):

                st.markdown(badge(r[6]), unsafe_allow_html=True)
                st.write("Reporter:", r[1])
                st.write("Location:", r[3])
                st.write("Description:", r[4])

                if r[5]:
                    st.error("Reporter says this is happening now.")

                options = sorted(CRIME_TRANSITIONS[r[6]])
                cols = st.columns(len(options))

                for col, new_status in zip(cols, options):
                    with col:
                        if st.button(
                            new_status.title(),
                            key=f"crime_{r[0]}_{new_status}"
                        ):
                            update_crime_report(
                                r[0], new_status, coordinator
                            )
                            st.rerun()

    else:
        st.info("No crime reports received yet.")

# ---------------------------------------------------------------
# Medical
# ---------------------------------------------------------------

with tab_med:

    feature_header("Medical Assistance", "medical")

    if medicals:

        df = pd.DataFrame(medicals, columns=MEDICAL_COLUMNS)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Review Requests")

        open_requests = [
            r for r in medicals if r[6] in MEDICAL_TRANSITIONS
        ]

        # Most urgent first
        open_requests.sort(
            key=lambda r: (URGENCY_ORDER.get(r[4], 9), r[0])
        )

        if not open_requests:
            st.caption("No open requests.")

        for r in open_requests:

            with st.expander(
                f"[{r[4]}] Request #{r[0]} – {r[1]} ({r[6]})"
            ):

                st.markdown(
                    f"{badge(r[4])} {badge(r[6])}",
                    unsafe_allow_html=True
                )
                st.write("Location:", r[2])
                st.write("Reported condition:", r[3])
                st.write("Assistance:", r[5])

                options = sorted(MEDICAL_TRANSITIONS[r[6]])
                cols = st.columns(len(options))

                for col, new_status in zip(cols, options):
                    with col:
                        label = new_status.replace("_", " ").title()
                        if st.button(
                            label,
                            key=f"med_{r[0]}_{new_status}"
                        ):
                            update_medical_request(
                                r[0], new_status, coordinator
                            )
                            st.rerun()

    else:
        st.info("No medical requests received yet.")

# ---------------------------------------------------------------
# Logs
# ---------------------------------------------------------------

with tab_logs:

    st.subheader("AI Activity Logs")

    logs = get_logs()

    if logs:

        log_df = pd.DataFrame(
            logs,
            columns=["ID", "Event", "Details", "Timestamp"]
        )

        st.dataframe(
            log_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.caption("No activity recorded yet.")
