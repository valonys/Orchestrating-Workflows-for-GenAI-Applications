"""
Modularized DigiTwin Analytics Application
Main application file that orchestrates all modules
"""

import streamlit as st
from config import PROMPTS
from utils import process_uploaded_files, build_faiss_vectorstore
from llm_models import generate_response
from ui_components import (
    setup_ui, setup_sidebar, initialize_session_state, 
    handle_agent_intro, render_all_tabs
)

def main():
    """Main application function"""
    # Setup UI
    setup_ui()
    
    # Initialize session state
    initialize_session_state()
    
    # Setup sidebar and get user inputs
    model_alias, uploaded_files, prompt_type, selected_fpso = setup_sidebar()
    
    # Process uploaded files
    parsed_docs = []
    df = None
    if uploaded_files:
        parsed_docs, df = process_uploaded_files(uploaded_files)
        if parsed_docs:  # Only build vectorstore if PDF files were processed
            st.session_state.vectorstore = build_faiss_vectorstore(parsed_docs)
    
    # Handle agent introduction
    handle_agent_intro(model_alias, prompt_type)
    
    # Create response generator function
    def generate_response_wrapper(prompt, df=None):
        return generate_response(
            prompt=prompt,
            model_alias=model_alias,
            prompt_type=prompt_type,
            df=df,
            vectorstore=st.session_state.vectorstore
        )
    
    # Render all tabs
    render_all_tabs(df, selected_fpso, generate_response_wrapper)

if __name__ == "__main__":
    main() 
