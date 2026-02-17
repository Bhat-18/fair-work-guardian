"""
Session management module.
Uses query params + localStorage for persistence.

KEY INSIGHT: 
- components.html() runs in a SANDBOXED iframe (about:srcdoc) 
  which CANNOT redirect the parent window.
- streamlit_js_eval runs in the STREAMLIT iframe context,
  which CAN read localStorage properly.
- So we use streamlit_js_eval for READING and 
  components.html for WRITING (writing works fine from sandbox).
"""
import streamlit as st
import uuid
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval


def _save_uid_to_storage(uid):
    """Save UID to localStorage using components.html (write works from sandbox)."""
    js = f"""
    <script>
        try {{ localStorage.setItem("fair_work_uid", "{uid}"); }} catch(e) {{}}
    </script>
    """
    components.html(js, height=0, width=0)


def get_user_id():
    """Get or create a unique user ID."""
    
    # 1. Check Query Params (Fastest, always available on refresh)
    params = st.query_params
    uid_from_params = params.get("uid", None)
    
    if uid_from_params:
        st.session_state['user_id'] = uid_from_params
        # Sync to localStorage for cross-session persistence
        _save_uid_to_storage(uid_from_params)
        return uid_from_params
    
    # 2. Try to recover from localStorage using streamlit_js_eval
    # This runs in the Streamlit context (NOT sandboxed), so it can read localStorage
    stored_id = streamlit_js_eval(
        js_expressions='localStorage.getItem("fair_work_uid")',
        key="read_uid_from_storage"
    )
    
    if stored_id and stored_id != "null" and str(stored_id).strip():
        # Found existing session! Set query param and rerun
        st.query_params["uid"] = stored_id
        st.session_state['user_id'] = stored_id
        st.rerun()  # Python-side redirect (no sandbox issues)
    
    # 3. Fallback: Generate new ID
    new_id = str(uuid.uuid4())[:8]
    st.query_params["uid"] = new_id
    st.session_state['user_id'] = new_id
    
    # Save to localStorage for next session
    _save_uid_to_storage(new_id)
    
    return new_id
