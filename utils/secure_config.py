# utils/secure_config.py
import os
import streamlit as st
from pathlib import Path

def get_openai_api_key():
    """
    Get OpenAI API key using Streamlit's secure secrets management.
    Priority order:
    1. Streamlit secrets (most secure)
    2. Environment variables
    3. User-provided session state (entered in UI)
    """
    # First check Streamlit secrets
    if 'openai' in st.secrets and 'api_key' in st.secrets['openai']:
        return st.secrets['openai']['api_key']
    
    # Then check environment variables
    elif os.environ.get('OPENAI_API_KEY'):
        return os.environ.get('OPENAI_API_KEY')
    
    # Finally check session state (set by user in UI)
    elif 'openai_api_key' in st.session_state and st.session_state['openai_api_key']:
        return st.session_state['openai_api_key']
    
    # No API key found
    return None

def save_api_key_to_session(api_key):
    """
    Save API key to session state only (not to disk)
    """
    if api_key:
        st.session_state['openai_api_key'] = api_key
        return True
    return False
