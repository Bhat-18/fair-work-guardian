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
        # Try parent window first (Cloud fix), then iframe storage
        js_sync = f"""
        const key = "fair_work_uid";
        const val = "{uid_from_params}";
        try {{ window.parent.localStorage.setItem(key, val); }} 
        catch(e) {{ localStorage.setItem(key, val); }}
        """
        streamlit_js_eval(js_expressions=js_sync, key=f"sync_uid_{uid_from_params}")
        return uid_from_params

    # 2. If no params, try to recover from localStorage (Async)
    # This renders a hidden component. It might return None initially (loading).
    # Try parent first, then fallback
    js_read = 'try { window.parent.localStorage.getItem("fair_work_uid") } catch(e) { localStorage.getItem("fair_work_uid") }'
    
    stored_id = streamlit_js_eval(
        js_expressions=js_read, 
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
    # This checks securely in the browser (synchronous check) to avoid overwrites.
    # Try parent, then iframe.
    js_smart_save = f"""
    const key = "fair_work_uid";
    const val = "{new_id}";
    try {{
        if (!window.parent.localStorage.getItem(key) || window.parent.localStorage.getItem(key) === "null") {{
            window.parent.localStorage.setItem(key, val);
        }}
    }} catch(e) {{
        if (!localStorage.getItem(key) || localStorage.getItem(key) === "null") {{
            localStorage.setItem(key, val);
        }}
    }}
    """
    
    streamlit_js_eval(
        js_expressions=js_smart_save,
        key=f"smart_save_{new_id}"
    )
    
    return new_id
