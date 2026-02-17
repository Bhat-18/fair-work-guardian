"""
Session management module.
Uses URL query parameters as the SOLE persistence mechanism.

On Streamlit Cloud, all JavaScript-based storage (localStorage, cookies)
fails due to cross-origin iframe restrictions. The URL query parameter
?uid=XXXXXXXX is the only reliable way to maintain identity.

When users bookmark or share their URL, their session persists.
"""
import streamlit as st
import uuid


def get_user_id():
    """Get or create a unique user ID from URL query parameters."""
    
    # Check query params
    uid = st.query_params.get("uid", None)
    
    if uid:
        st.session_state['user_id'] = uid
        return uid
    
    # Check session state (handles in-session navigation)
    if 'user_id' in st.session_state and st.session_state['user_id']:
        uid = st.session_state['user_id']
        st.query_params["uid"] = uid
        return uid
    
    # Generate new ID
    new_id = str(uuid.uuid4())[:8]
    st.query_params["uid"] = new_id
    st.session_state['user_id'] = new_id
    return new_id
