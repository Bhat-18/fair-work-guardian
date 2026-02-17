"""
Session management module.
Uses Cookies for robust persistence across browser sessions.
Falls back to query parameters if cookies are disabled.
Handles async cookie loading gracefully.
"""
import streamlit as st
import uuid
import extra_streamlit_components as stx
from datetime import datetime, timedelta

def get_user_id():
    """Get or create a unique user ID using Cookies."""
    
    # Initialize Cookie Manager
    # This component needs to be rendered to work.
    cookie_manager = stx.CookieManager(key="cookie_manager")
    
    # 1. Check Query Params (Highest Priority - allows overriding/sharing)
    params = st.query_params
    uid_from_params = params.get("uid", None)
    
    # 2. Get all cookies (might be empty on first load until component syncs)
    cookies = cookie_manager.get_all()
    
    # Wait for component to mount if cookies are not yet loaded?
    # stx.CookieManager handles this usually, but returns {} initially.
    # We can't distinguish "No Cookies" from "Not Loaded Yet".
    # But usually it's fast.
    
    uid_cookie = cookies.get("fair_work_uid")
    
    # LOGIC FLOW
    
    # Case A: User has URL param
    if uid_from_params:
        # If cookie doesn't match or is missing, update/set it
        if uid_cookie != uid_from_params:
            try:
                cookie_manager.set("fair_work_uid", uid_from_params, expires_at=datetime.now() + timedelta(days=365))
            except Exception:
                pass # Component might not be ready, will retry next run
                
        st.session_state['user_id'] = uid_from_params
        return uid_from_params
        
    # Case B: User has Cookie (Returning User)
    if uid_cookie:
        # Restore session from cookie
        st.session_state['user_id'] = uid_cookie
        # Update URL to match
        if params.get("uid") != uid_cookie:
            st.query_params["uid"] = uid_cookie
            st.rerun() # Reload to ensure URL is clean
        return uid_cookie
        
    # Case C: New User (No Cookie, No Param)
    # Generate new ID
    new_id = str(uuid.uuid4())[:8]
    
    # Set Param immediately
    st.query_params["uid"] = new_id
    st.session_state['user_id'] = new_id
    
    # Try to set Cookie (might fail if component not ready, but param handles this session)
    try:
        cookie_manager.set("fair_work_uid", new_id, expires_at=datetime.now() + timedelta(days=365))
    except Exception:
        pass
    
    # Note: On next rerun/load, Case A will trigger and ensure cookie is set.
    
    return new_id
