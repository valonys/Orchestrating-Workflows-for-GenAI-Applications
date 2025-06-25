"""
Configuration module for DigiTwin Analytics
Contains all constants, keywords, and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- AVATARS ---
USER_AVATAR = "https://raw.githubusercontent.com/achilela/vila_fofoka_analysis/9904d9a0d445ab0488cf7395cb863cce7621d897/USER_AVATAR.png"
BOT_AVATAR = "https://raw.githubusercontent.com/achilela/vila_fofoka_analysis/991f4c6e4e1dc7a8e24876ca5aae5228bcdb4dba/Ataliba_Avatar.jpg"

# --- SYSTEM PROMPTS ---
PROMPTS = {
    "Daily Report Summarization": """You are DigiTwin, an expert inspector and maintenance engineer...""",
    "5-Day Progress Report": """You are DigiTwin, an expert inspector with deep knowledge in KPIs, GM, CR...""",
    "Backlog Extraction": """You are DigiTwin, an expert inspector trained to extract and classify backlogs...""",
    "Inspector Expert": """You are DigiTwin, an expert inspector for advanced diagnosis and recommendation...""",
    "Complex Reasoning": """You are DigiTwin, trained to analyze multi-day reports using GS-OT-MIT-511 rules..."""
}

# --- NOTIFICATION KEYWORDS AND MAPPINGS ---
NI_keywords = ['WRAP', 'WELD', 'TBR', 'PACH', 'PATCH', 'OTHE', 'CLMP', 'REPL', 
               'BOND', 'BOLT', 'SUPP', 'OT', 'GASK']
NC_keywords = ['COA', 'ICOA', 'CUSP', 'WELD', 'REPL', 'CUSP1', 'CUSP2']
module_keywords = ['M110', 'M111', 'M112', 'M113', 'M114', 'M115', 'M116', 'H151',
                  'M120', 'M121', 'M122', 'M123', 'M124', 'M125', 'M126', 'M151']
rack_keywords = ['141', '142', '143', '144', '145', '146']
living_quarters_keywords = ['LQ', 'LQ1', 'LQ2', 'LQ3', 'LQ4', 'LQL0', 'LQPS', 'LQSB', 'LQROOF', 'LQL4', 'LQL2', 'LQ-5', 'LQPD', 'LQ PS', 'LQAFT', 'LQ-T', 'LQL1S']
flare_keywords = ['131']
fwd_keywords = ['FWD']
hexagons_keywords = ['HELIDECK']

NI_keyword_map = {'TBR1': 'TBR', 'TBR2': 'TBR', 'TBR3': 'TBR', 'TBR4': 'TBR'}
NC_keyword_map = {'COA1': 'COA', 'COA2': 'COA', 'COA3': 'COA', 'COA4': 'COA'}

# CLV location dictionaries
clv_modules = {
    'M120': (0.75, 2), 'M121': (0.5, 3), 'M122': (0.5, 4), 'M123': (0.5, 5),
    'M124': (0.5, 6), 'M125': (0.5, 7), 'M126': (0.5, 8), 'M151': (0.5, 9), 'M110': (1.75, 2),
    'M111': (2, 3), 'M112': (2, 4), 'M113': (2, 5), 'M114': (2, 6),
    'M115': (2, 7), 'M116': (2, 8), 'H151': (2, 9)
}
clv_racks = {'141': (1.5, 3), '142': (1.5, 4), '143': (1.5, 5),
             '144': (1.5, 6), '145': (1.5, 7), '146': (1.5, 8)}
clv_flare = {'131': (1.5, 9)}
clv_living_quarters = {'LQ': (0.5, 1)}
clv_hexagons = {'HELIDECK': (2.75, 1)}
clv_fwd = {'FWD': (0.5, 10)}

# PAZ location dictionaries
paz_modules = {
    'P1': (0.75, 2), 'P2': (0.5, 3), 'P3': (0.5, 4), 'P4': (0.5, 5),
    'P5': (0.5, 6), 'P6': (0.5, 7), 'P7': (0.5, 8), 'P8': (0.5, 9), 'S1': (1.75, 2),
    'S2': (2, 3), 'S3': (2, 4), 'S4': (2, 5), 'S5': (2, 6),
    'S6': (2, 7), 'S7': (2, 8), 'S8': (2, 9)
}
paz_racks = {'R1': (1.5, 3), 'R2': (1.5, 4), 'R3': (1.5, 5),
             'R4': (1.5, 6), 'R5': (1.5, 7), 'R6': (1.5, 8)}
paz_flare = {'131': (1.5, 9)}
paz_living_quarters = {'LQ': (0.5, 1)}
paz_hexagons = {'HELIDECK': (2.75, 1)}
paz_fwd = {'FWD': (0.5, 10)}

# --- MODEL CONFIGURATIONS ---
MODEL_CONFIGS = {
    "EE Smartest Agent": {
        "provider": "openai",
        "api_key_env": "API_KEY",
        "base_url": "https://api.x.ai/v1",
        "model": "grok-3",
        "stream": True
    },
    "JI Divine Agent": {
        "provider": "openai",
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.sambanova.ai/v1",
        "model": "DeepSeek-R1-Distill-Llama-70B",
        "stream": True
    },
    "EdJa-Valonys": {
        "provider": "cerebras",
        "api_key_env": "CEREBRAS_API_KEY",
        "model": "llama-4-scout-17b-16e-instruct",
        "stream": False
    },
    "XAI Inspector": {
        "provider": "huggingface",
        "model_id": "amiguel/GM_Qwen1.8B_Finetune",
        "api_key_env": "HF_TOKEN"
    },
    "Valonys Llama": {
        "provider": "huggingface",
        "model_id": "amiguel/Llama3_8B_Instruct_FP16",
        "api_key_env": "HF_TOKEN"
    }
}

# --- UI STYLES ---
UI_STYLES = """
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
"""

LOGO_HTML = """
    <div class="logo-container">
        <img src="https://github.com/valonys/DigiTwin/blob/29dd50da95bec35a5abdca4bdda1967f0e5efff6/ValonyLabs_Logo.png?raw=true" width="70">
    </div>
"""

# --- AGENT INTROS ---
AGENT_INTROS = {
    "EE Smartest Agent": "💡 EE Agent Activated — Pragmatic & Smart",
    "JI Divine Agent": "✨ JI Agent Activated — DeepSeek Reasoning",
    "EdJa-Valonys": "⚡ EdJa Agent Activated — Cerebras Speed",
    "XAI Inspector": "🔍 XAI Inspector — Qwen Custom Fine-tune",
    "Valonys Llama": "🦙 Valonys Llama — LLaMA3-Based Reasoning"
} 