"""
UI Components module for DigiTwin Analytics
Contains Streamlit interface elements and tab components
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import create_pivot_table, apply_fpso_colors, build_faiss_vectorstore
from visualization import draw_fpso_layout
from config import AGENT_INTROS, module_keywords, rack_keywords, living_quarters_keywords, flare_keywords, fwd_keywords, hexagons_keywords

# PAZ-specific keywords for the new naming convention
paz_module_keywords = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
paz_rack_keywords = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']

def setup_ui():
    """Setup the main UI configuration and styling"""
    st.set_page_config(page_title="DigiTwin Analytics", layout="wide")
    
    # Apply custom styles
    st.markdown("""
        <style>
        @import url('https://fonts.cdnfonts.com/css/tw-cen-mt');
        * {
            font-family: 'Tw Cen MT', sans-serif !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"]::before {
            content: "▶";
            font-size: 1.3rem;
            margin-right: 0.4rem;
        }
        .logo-container {
            position: fixed;
            top: 5rem;
            right: 12rem;
            z-index: 9999;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 16px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display logo
    st.markdown("""
        <div class="logo-container">
            <img src="https://github.com/valonys/DigiTwin/blob/29dd50da95bec35a5abdca4bdda1967f0e5efff6/ValonyLabs_Logo.png?raw=true" width="70">
        </div>
    """, unsafe_allow_html=True)
    
    st.title("📊 DigiTwin Analytics - Powered by AI")

def setup_sidebar():
    """Setup the sidebar with controls"""
    with st.sidebar:
        st.title("DigiTwin Control Panel")
        model_alias = st.selectbox("Choose AI Agent", [
            "EE Smartest Agent", "JI Divine Agent", "EdJa-Valonys", "XAI Inspector", "Valonys Llama"
        ])
        uploaded_files = st.file_uploader("📁 Upload Files for Analysis", type=["pdf", "xlsx"], accept_multiple_files=True)
        prompt_type = st.selectbox("Select Task Type", [
            "Daily Report Summarization", "5-Day Progress Report", "Backlog Extraction", 
            "Inspector Expert", "Complex Reasoning"
        ])
        selected_fpso = st.selectbox("Select FPSO for Layout", ['GIR', 'DAL', 'PAZ', 'CLV'])
    
    return model_alias, uploaded_files, prompt_type, selected_fpso

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    for key in ["vectorstore", "chat_history", "model_intro_done", "current_model", "current_prompt"]:
        if key not in st.session_state:
            st.session_state[key] = [] if key == "chat_history" else None if key == "vectorstore" else False

def handle_agent_intro(model_alias, prompt_type):
    """Handle agent introduction messages"""
    if not st.session_state.model_intro_done or st.session_state.current_model != model_alias or st.session_state.current_prompt != prompt_type:
        st.session_state.chat_history.append({"role": "assistant", "content": AGENT_INTROS.get(model_alias)})
        st.session_state.model_intro_done = True
        st.session_state.current_model = model_alias
        st.session_state.current_prompt = prompt_type

def render_chat_tab(df, generate_response_func):
    """Render the chat tab"""
    st.subheader("Interact with DigiTwin")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"], unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask about reports or notifications..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in generate_response_func(prompt, df):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
            response_placeholder.markdown(full_response, unsafe_allow_html=True)
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

def render_ni_notifications_tab(df):
    """Render the NI notifications tab"""
    st.subheader("NI Notifications Analysis")
    if df is not None and not df[df['Notifictn type'] == 'NI'].empty:
        ni_pivot = create_pivot_table(df[df['Notifictn type'] == 'NI'], index='FPSO', columns='Extracted_Keywords')
        st.write("Pivot Table (Count of Keywords by FPSO):")
        styled_ni_pivot = ni_pivot.style.apply(apply_fpso_colors, axis=None)
        st.dataframe(styled_ni_pivot)
        st.write(f"Total NI Notifications: {df[df['Notifictn type'] == 'NI'].shape[0]}")
    else:
        st.write("No NI notifications found or no files uploaded.")

def render_nc_notifications_tab(df):
    """Render the NC notifications tab"""
    st.subheader("NC Notifications Analysis")
    if df is not None and not df[df['Notifictn type'] == 'NC'].empty:
        nc_pivot = create_pivot_table(df[df['Notifictn type'] == 'NC'], index='FPSO', columns='Extracted_Keywords')
        st.write("Pivot Table (Count of Keywords by FPSO):")
        styled_nc_pivot = nc_pivot.style.apply(apply_fpso_colors, axis=None)
        st.dataframe(styled_nc_pivot)
        st.write(f"Total NC Notifications: {df[df['Notifictn type'] == 'NC'].shape[0]}")
    else:
        st.write("No NC notifications found or no files uploaded.")

def render_summary_stats_tab(df):
    """Render the summary stats tab"""
    st.subheader("2025 Notification Summary")
    if df is not None:
        df_2025 = df[pd.to_datetime(df['Created on']).dt.year == 2025].copy()
        if not df_2025.empty:
            df_2025['Month'] = pd.to_datetime(df_2025['Created on']).dt.strftime('%b')
            months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            df_2025['Month'] = pd.Categorical(df_2025['Month'], categories=months_order, ordered=True)
            summary = df_2025.groupby(['FPSO', 'Month', 'Notifictn type']).size().unstack(fill_value=0)
            ni_summary = summary['NI'].unstack(level='Month').reindex(columns=months_order, fill_value=0)
            nc_summary = summary['NC'].unstack(level='Month').reindex(columns=months_order, fill_value=0)
            st.write("NI Notifications by Month:")
            st.dataframe(ni_summary.style.set_properties(**{'text-align': 'center'}))
            st.write("NC Notifications by Month:")
            st.dataframe(nc_summary.style.set_properties(**{'text-align': 'center'}))
            st.write(f"Grand Total NI Notifications: {df_2025[df_2025['Notifictn type'] == 'NI'].shape[0]}")
            st.write(f"Grand Total NC Notifications: {df_2025[df_2025['Notifictn type'] == 'NC'].shape[0]}")
        else:
            st.write("No notifications found for 2025.")

def render_fpso_layout_tab(df, selected_fpso):
    """Render the FPSO layout tab"""
    st.subheader("FPSO Layout Visualization")
    if df is not None:
        notification_type = st.radio("Select Notification Type", ['NI', 'NC'])
        df_selected = df[df['FPSO'] == selected_fpso].copy()
        df_selected = df_selected[df_selected['Notifictn type'] == notification_type]
        
        # Determine which keywords to use based on selected FPSO
        if selected_fpso == 'PAZ':
            module_keywords_to_use = paz_module_keywords
            rack_keywords_to_use = paz_rack_keywords
        else:  # CLV, GIR, DAL
            module_keywords_to_use = module_keywords
            rack_keywords_to_use = rack_keywords
        
        location_counts = {
            'Modules': pd.DataFrame(index=module_keywords_to_use, columns=['Count']).fillna(0),
            'Racks': pd.DataFrame(index=rack_keywords_to_use, columns=['Count']).fillna(0),
            'LivingQuarters': pd.DataFrame(index=living_quarters_keywords, columns=['Count']).fillna(0),
            'Flare': pd.DataFrame(index=flare_keywords, columns=['Count']).fillna(0),
            'FWD': pd.DataFrame(index=fwd_keywords, columns=['Count']).fillna(0),
            'HeliDeck': pd.DataFrame(index=hexagons_keywords, columns=['Count']).fillna(0)
        }
        
        for location_type, keywords in [
            ('Modules', module_keywords_to_use), ('Racks', rack_keywords_to_use), ('LivingQuarters', living_quarters_keywords),
            ('Flare', flare_keywords), ('FWD', fwd_keywords), ('HeliDeck', hexagons_keywords)
        ]:
            for keyword in keywords:
                count = df_selected[f'Extracted_{location_type}'].str.contains(keyword, na=False).sum()
                location_counts[location_type].loc[keyword, 'Count'] = count
        
        fig = draw_fpso_layout(selected_fpso, df_selected, notification_type, location_counts)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.write("Please upload files to view the FPSO layout.")

def render_all_tabs(df, selected_fpso, generate_response_func):
    """Render all tabs"""
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chat", "NI Notifications", "NC Notifications", "Summary Stats", "FPSO Layout"])
    
    with tab1:
        render_chat_tab(df, generate_response_func)
    
    with tab2:
        render_ni_notifications_tab(df)
    
    with tab3:
        render_nc_notifications_tab(df)
    
    with tab4:
        render_summary_stats_tab(df)
    
    with tab5:
        render_fpso_layout_tab(df, selected_fpso) 