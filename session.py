"""
Session management module.
Generates a unique browser-based user ID.
Uses query parameters as the source of truth for speed.
Asynchronously syncs to localStorage for persistence across sessions.
Non-blocking implementation to ensure immediate app loading.
"""
import streamlit as st
import uuid
from streamlit_js_eval import streamlit_js_eval


def get_user_id():
    """Get or create a unique user ID."""
    
    # 1. Check query params (Source of Truth)
    # This is fast and available immediately.
    params = st.query_params
    uid_from_params = params.get("uid", None)

    if uid_from_params:
        st.session_state['user_id'] = uid_from_params
        
        # Async sync to localStorage (fire and forget)
        # This ensures that if the user comes back later without the URL param, 
        # localStorage will have it.
        streamlit_js_eval(
            js_expressions=f'localStorage.setItem("fair_work_uid", "{uid_from_params}")', 
            key="sync_uid"
        )
        return uid_from_params

    # 2. If no params, try to recover from localStorage (Async)
    # This renders a hidden component. It might return None initially (loading).
    stored_id = streamlit_js_eval(
        js_expressions='localStorage.getItem("fair_work_uid")', 
        key="get_local_uid"
    )
    
    if stored_id and stored_id != "null":
        # Found persistence! Restore it.
        st.query_params["uid"] = stored_id
        st.session_state['user_id'] = stored_id
        st.rerun() # Restart to apply everywhere
        return stored_id

    # 3. Fallback: Generate New ID immediately
    # We do NOT wait for JS (no st.stop) to prevent loading issues.
    new_id = str(uuid.uuid4())[:8]
    st.query_params["uid"] = new_id
    st.session_state['user_id'] = new_id
    
    # SMART SAVE: Only save to localStorage if it's currently empty.
    # This prevents overwriting existing data if we are just "loading" (Step 2 hasn't finished).
    # But ensures new users get persisted immediately.
    streamlit_js_eval(
        js_expressions=f'if (!localStorage.getItem("fair_work_uid") || localStorage.getItem("fair_work_uid") == "null") localStorage.setItem("fair_work_uid", "{new_id}")',
        key="smart_save_uid"
    )
    
    return new_id
