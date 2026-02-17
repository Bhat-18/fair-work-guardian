"""
Session management module.
Generates a unique browser-based user ID using localStorage.
Each browser gets its own isolated data — no login required.
The ID persists across browser sessions via localStorage.
"""
import streamlit as st
import uuid
from streamlit_js_eval import streamlit_js_eval


def get_user_id():
    """Get or create a unique user ID for this browser session.
    Uses localStorage so the ID persists even after closing the browser."""

    # If already resolved in this session, return immediately
    if 'user_id' in st.session_state and st.session_state['user_id']:
        return st.session_state['user_id']

    # Check query params first (for shared links)
    params = st.query_params
    uid_from_params = params.get("uid", None)

    if uid_from_params:
        st.session_state['user_id'] = uid_from_params
        # Also save to localStorage for future visits
        streamlit_js_eval(js_expressions=f'localStorage.setItem("fair_work_uid", "{uid_from_params}")')
        return uid_from_params

    # Try to read from localStorage (persists across browser sessions)
    stored_id = streamlit_js_eval(js_expressions='localStorage.getItem("fair_work_uid")')

    if stored_id is None:
        # JS hasn't executed yet on first render, wait for it
        st.stop()

    if stored_id and stored_id != "null" and stored_id != "":
        st.session_state['user_id'] = stored_id
        st.query_params["uid"] = stored_id
        return stored_id

    # First-time user: generate new ID
    new_id = str(uuid.uuid4())[:8]
    st.session_state['user_id'] = new_id
    st.query_params["uid"] = new_id

    # Save to localStorage for persistence
    streamlit_js_eval(js_expressions=f'localStorage.setItem("fair_work_uid", "{new_id}")')

    return new_id
