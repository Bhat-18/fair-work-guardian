"""
Session management module.
Uses a two-phase approach to handle the async nature of JS communication:

Phase 1 (First Run): 
  - streamlit_js_eval returns None (component mounting)
  - We DON'T generate a new ID yet. We wait.
  
Phase 2 (After Rerun):
  - streamlit_js_eval returns the actual localStorage value (or "null" if empty)
  - NOW we can safely decide: use stored ID or generate new one.

This prevents the race condition where a new ID overwrites the stored one.
"""
import streamlit as st
import uuid
from streamlit_js_eval import streamlit_js_eval


def get_user_id():
    """Get or create a unique user ID with two-phase localStorage check."""
    
    # 1. If uid is already in query params, we're good. Just use it.
    params = st.query_params
    uid_from_params = params.get("uid", None)
    
    if uid_from_params:
        st.session_state['user_id'] = uid_from_params
        # Sync to localStorage (fire and forget)
        streamlit_js_eval(
            js_expressions=f'localStorage.setItem("fair_work_uid", "{uid_from_params}")',
            key="save_uid"
        )
        return uid_from_params
    
    # 2. No uid in params. Check localStorage.
    # On first component mount, this returns None (not ready yet).
    # On subsequent runs (after rerun), it returns the actual value.
    stored = streamlit_js_eval(
        js_expressions='localStorage.getItem("fair_work_uid")',
        key="load_uid"
    )
    
    # Phase 1: Component not ready yet (returns None)
    if stored is None:
        # Don't generate ID yet! Wait for JS to be ready.
        # Use a temporary placeholder and trigger a rerun.
        if 'uid_check_done' not in st.session_state:
            st.session_state['uid_check_done'] = False
        
        if not st.session_state['uid_check_done']:
            st.session_state['uid_check_done'] = True
            st.rerun()  # Rerun to give JS time to mount and return value
        
        # If we already reran and STILL got None, fall through to generate new ID
    
    # Phase 2: JS responded
    if stored and stored != "null" and str(stored).strip():
        # Found existing session! Restore it.
        st.query_params["uid"] = stored
        st.session_state['user_id'] = stored
        st.session_state['uid_check_done'] = True
        st.rerun()
    
    # 3. No stored ID found (truly new user). Generate one.
    new_id = str(uuid.uuid4())[:8]
    st.query_params["uid"] = new_id
    st.session_state['user_id'] = new_id
    st.session_state['uid_check_done'] = True
    
    # Save to localStorage
    streamlit_js_eval(
        js_expressions=f'localStorage.setItem("fair_work_uid", "{new_id}")',
        key="save_new_uid"
    )
    
    return new_id
