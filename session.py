"""
Session management module.
Generates a unique browser-based user ID using localStorage.
Each browser gets its own isolated data — no login required.
"""
import streamlit as st
import uuid


def get_user_id():
    """Get or create a unique user ID for this browser session."""
    # If already in session state, return it
    if 'user_id' in st.session_state and st.session_state['user_id']:
        return st.session_state['user_id']

    # Check query params for returning users
    params = st.query_params
    uid = params.get("uid", None)

    if uid:
        st.session_state['user_id'] = uid
        return uid

    # Generate new ID for first-time users
    new_id = str(uuid.uuid4())[:8]  # Short 8-char ID
    st.session_state['user_id'] = new_id

    # Set it in query params so it persists across page navigation
    st.query_params["uid"] = new_id

    return new_id
