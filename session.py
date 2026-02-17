"""
Session management module.
Uses Cookies for robust persistence across browser sessions.
Includes explicit retry logic to handle async cookie loading.
"""
import streamlit as st
import uuid
import extra_streamlit_components as stx
import time

def get_user_id():
    """Get or create a unique user ID using Cookies with retry logic."""
    
    # Initialize Cookie Manager
    # key is crucial for component state
    cookie_manager = stx.CookieManager(key="cookie_manager")
    
    # 1. Check Query Params (Highest Priority - allows overriding)
    params = st.query_params
    uid_from_params = params.get("uid", None)
    
    if uid_from_params:
        # If we have a param, we trust it.
        # Try to sync it to cookie for future visits
        # Note: .set() might not work if component isn't fully mounted, but param is enough for now.
        if "cookie_set" not in st.session_state:
            try:
                cookie_manager.set("fair_work_uid", uid_from_params, expires_at=datetime.now() + timedelta(days=365))
                st.session_state["cookie_set"] = True
            except:
                pass 
        return uid_from_params
        
    # 2. Check Cookies with Retry Logic
    # Cookie manager often returns None or {} on the very first run.
    # We must be careful not to generate a NEW ID just because cookies haven't loaded yet.
    
    cookies = cookie_manager.get_all()
    
    # If cookies are None (loading), we should wait/rerun?
    # But we can't block indefinitely.
    # Strategy: Use a session state flag to track "Cookie Checked".
    
    uid_cookie = None
    if cookies:
        uid_cookie = cookies.get("fair_work_uid")
    
    if uid_cookie:
        # Found it! Restore session.
        if params.get("uid") != uid_cookie:
            st.query_params["uid"] = uid_cookie
            st.rerun() # Reload to ensure clean state
        return uid_cookie
        
    # 3. If no cookie found, are we sure they loaded?
    # If this is the *first* script run, cookies might be empty but valid.
    # If we generate new ID now, we might overwrite an existing user!
    # BUT, we can't wait forever.
    
    # Check if we've already waited/checked
    if "cookie_checked" not in st.session_state:
        st.session_state["cookie_checked"] = True
        # Rerun once to give cookie manager a chance to sync
        time.sleep(0.5) 
        st.rerun()
        
    # 4. If we are here, we checked cookies and found nothing.
    # Generate NEW ID.
    new_id = str(uuid.uuid4())[:8]
    
    # Set Param immediately
    st.query_params["uid"] = new_id
    
    # Set Cookie
    from datetime import datetime, timedelta
    try:
        cookie_manager.set("fair_work_uid", new_id, expires_at=datetime.now() + timedelta(days=365))
    except:
        pass
        
    return new_id
