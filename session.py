"""
Session management module.
Uses a hybrid approach:
1. Query Params (Highest Priority)
2. LocalStorage (via simple JS injection)
Fallbacks to new ID if neither found.
No external dependencies for storage to ensure robustness.
"""
import streamlit as st
import uuid
import streamlit.components.v1 as components

def get_user_id():
    """Get or create a unique user ID."""
    
    # 1. Check Query Params (Fastest)
    params = st.query_params
    uid_from_params = params.get("uid", None)
    
    if uid_from_params:
        st.session_state['user_id'] = uid_from_params
        
        # Force sync to localStorage (Parent + Iframe)
        # We use simple JS injection which is more reliable than complex components
        js = f"""
        <script>
            const uid = "{uid_from_params}";
            try {{ window.parent.localStorage.setItem("fair_work_uid", uid); }} catch(e) {{}}
            try {{ localStorage.setItem("fair_work_uid", uid); }} catch(e) {{}}
        </script>
        """
        components.html(js, height=0, width=0)
        return uid_from_params
    
    # 2. If no params, we need to check localStorage.
    # Since we can't synchronously read from JS to Python without a component,
    # and components are failing, we accept a trade-off:
    # We generate a NEW ID, but we inject JS that says:
    # "Hey, if you actually have an OLD ID in storage, reload the page with ?uid=OLD_ID"
    
    new_id = str(uuid.uuid4())[:8]
    
    # JS Logic:
    # Check storage. 
    # If found -> Redirect to ?uid=FOUND
    # If empty -> Save NEW_ID
    
    js_recover = f"""
    <script>
        const new_id = "{new_id}";
        const key = "fair_work_uid";
        
        let stored = null;
        try {{ stored = window.parent.localStorage.getItem(key); }} catch(e) {{}}
        if (!stored) {{
            try {{ stored = localStorage.getItem(key); }} catch(e) {{}}
        }}
        
        if (stored && stored !== "null" && stored !== "{new_id}") {{
            // Found existing ID! Redirect to use it.
            const url = new URL(window.location.href);
            url.searchParams.set("uid", stored);
            window.parent.location.href = url.toString();
        }} else {{
            // No existing ID. Save the new one we just generated.
            try {{ window.parent.localStorage.setItem(key, new_id); }} catch(e) {{}}
            try {{ localStorage.setItem(key, new_id); }} catch(e) {{}}
        }}
    </script>
    """
    
    # Inject the script
    components.html(js_recover, height=0, width=0)
    
    # For this render cycle, use the new ID.
    # If the JS finds an old ID, it will reload the page immediately.
    st.query_params["uid"] = new_id
    st.session_state['user_id'] = new_id
    
    return new_id
