"""Shared visual themes for the Swagon dashboards.

Each dashboard gets its own colour identity so they are instantly
distinguishable, and each feature (mobility / crime / medical) has its
own accent colour so status cards are easy to tell apart.
"""

import streamlit as st

THEMES = {
    # Passenger: calm sky blue, navy text
    "passenger": {
        "bg": "#E3F2FD",
        "surface": "#FFFFFF",
        "heading": "#0D47A1",
        "text": "#10243E",
        "accent": "#1976D2",
    },
    # Coordinator: warm sand, burnt-orange headings
    "coordinator": {
        "bg": "#FFF3E0",
        "surface": "#FFFFFF",
        "heading": "#BF360C",
        "text": "#2B1A10",
        "accent": "#E65100",
    },
}

# Accent colour per feature
FEATURE_COLORS = {
    "mobility": "#1565C0",   # blue
    "crime": "#C62828",      # red
    "medical": "#00897B",    # teal
}

# Colour per status / urgency badge
STATUS_COLORS = {
    "PENDING": "#F9A825",
    "APPROVED": "#2E7D32",
    "REJECTED": "#C62828",
    "ACKNOWLEDGED": "#1565C0",
    "ESCALATED": "#6A1B9A",
    "CLOSED": "#546E7A",
    "DISPATCHED": "#00897B",
    "RESOLVED": "#2E7D32",
    "UNABLE_TO_DISPATCH": "#C62828",
    "LOW": "#558B2F",
    "MEDIUM": "#F9A825",
    "HIGH": "#EF6C00",
    "CRITICAL": "#B71C1C",
}


def badge(label):
    """Small coloured pill for a status or urgency value."""
    colour = STATUS_COLORS.get(str(label).upper(), "#546E7A")
    return (
        f"<span style='background:{colour};color:#fff;"
        f"padding:2px 10px;border-radius:12px;"
        f"font-size:0.8rem;font-weight:600'>{label}</span>"
    )


def feature_header(text, feature):
    """Section heading with a coloured left bar for the feature."""
    colour = FEATURE_COLORS[feature]
    st.markdown(
        f"<h3 style='border-left:8px solid {colour};"
        f"padding-left:12px;margin-top:0.5rem'>{text}</h3>",
        unsafe_allow_html=True,
    )


def apply_theme(role):
    t = THEMES[role]
    st.markdown(f"""
<style>
.stApp {{
    background: {t['bg']};
    color: {t['text']};
}}
.stApp p, .stApp label, .stApp li, .stApp span,
.stApp [data-testid="stCaptionContainer"] {{
    color: {t['text']};
}}
h1, h2, h3 {{
    color: {t['heading']} !important;
}}
[data-testid="stMetric"] {{
    background: {t['surface']};
    border-left: 6px solid {t['accent']};
    border-radius: 8px;
    padding: 10px 14px;
}}
[data-testid="stChatMessage"] {{
    background: {t['surface']};
    border-radius: 10px;
}}
[data-testid="stExpander"] {{
    background: {t['surface']};
    border-radius: 8px;
}}
button[data-baseweb="tab"] {{
    font-weight: 600;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {t['heading']};
}}
.stButton > button {{
    border: 2px solid {t['accent']};
    color: {t['accent']};
    background: {t['surface']};
    font-weight: 600;
}}
.stButton > button:hover {{
    background: {t['accent']};
    color: #fff;
}}
</style>
""", unsafe_allow_html=True)
