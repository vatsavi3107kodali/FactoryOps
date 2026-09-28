import base64
import os
import textwrap
import urllib.parse
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components


def svg_to_img(svg_str: str, width: int = 20, height: int = 20, extra_style: str = "") -> str:
    encoded = urllib.parse.quote(svg_str.strip())
    return f'<img src="data:image/svg+xml,{encoded}" width="{width}" height="{height}" style="display:inline-block;vertical-align:middle;{extra_style}" alt="icon" />'


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FactoryOps | Predictive Maintenance",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

REQUEST_TIMEOUT = 8


def get_login_bg_base64() -> str:
    paths = [
        os.path.join(
            os.path.dirname(__file__),
            "assets",
            "login_bg.png",
        ),
        os.path.join(
            os.path.dirname(__file__),
            "assets",
            "login_bg.jpg",
        ),
        r"C:\Users\Premalatha N K\.gemini\antigravity-ide\brain\2cb315ff-c089-43c7-a0d9-9a98406fb9a5\.user_uploaded\media_1788876319935.png",
    ]
    for bg_path in paths:
        if os.path.exists(bg_path):
            with open(bg_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return ""


@st.cache_data
def get_banner_img_base64() -> str:
    path = os.path.join(os.path.dirname(__file__), "assets", "isometric_factory.jpg")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


# ============================================================
# LOGIN CREDENTIALS
# ============================================================

ADMIN_USERNAME = os.getenv(
    "STREAMLIT_ADMIN_USERNAME",
    "admin",
)

ADMIN_PASSWORD = os.getenv(
    "STREAMLIT_ADMIN_PASSWORD",
    "admin123",
)

USER_USERNAME = os.getenv(
    "STREAMLIT_USER_USERNAME",
    "user",
)

USER_PASSWORD = os.getenv(
    "STREAMLIT_USER_PASSWORD",
    "user123",
)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# HTML RENDER HELPER
# ============================================================


def render_html(content: str):
    st.html(textwrap.dedent(content).strip())


# ============================================================
# GLOBAL STYLING
# ============================================================

render_html(
    """
    <style>

        /* ==================================================
           GLOBAL APP (Crimson-Rose & Crisp White Foundation)
           ================================================== */

        html {
            scroll-behavior: smooth;
            scroll-padding-top: 140px !important;
        }

        .stApp {
            background-color: #fff5f7 !important;
            background-image: 
                radial-gradient(circle at 12% 10%, rgba(244, 43, 85, 0.18) 0%, transparent 42%),
                radial-gradient(circle at 88% 14%, rgba(244, 43, 85, 0.13) 0%, transparent 45%),
                radial-gradient(circle at 50% 85%, rgba(244, 43, 85, 0.08) 0%, transparent 55%),
                linear-gradient(180deg, #ffffff 0%, #fff5f7 40%, #ffffff 100%) !important;
            background-attachment: fixed !important;
            color: #0f172a !important;
            min-height: 100vh !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        }


        /* ==================================================
           GLOBAL CONTAINER SPACING (Spacious Executive Framing)
           ================================================== */

        .main, .stMain, [data-testid="stMain"] {
            background: transparent !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            width: 100% !important;
        }

        .block-container,
        [data-testid="stAppViewBlockContainer"],
        [data-testid="stMainBlockContainer"],
        .main .block-container {
            max-width: 1320px !important;
            width: 100% !important;
            padding-top: 135px !important;
            padding-bottom: 5rem !important;
            padding-left: clamp(2rem, 4.5vw, 4rem) !important;
            padding-right: clamp(2rem, 4.5vw, 4rem) !important;
            margin-left: auto !important;
            margin-right: auto !important;
            box-sizing: border-box !important;
        }

        [data-testid="stVerticalBlock"] {
            gap: 1.25rem;
        }


        /* ==================================================
           OFFICIAL TOP NAVIGATION & HEADER
           ================================================== */

        [data-testid="stSidebar"] {
            display: none;
        }

        /* Constant Fixed Header & Navigation Bar (Centered to match body content) */
        div[class*="st-key-factory_header_sticky"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            width: 100vw !important;
            z-index: 999999 !important;
            background: rgba(255, 255, 255, 0.96) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(244, 43, 85, 0.16) !important;
            box-shadow: 0 4px 24px rgba(244, 43, 85, 0.08) !important;
            padding: 0.35rem 0 0.5rem 0 !important;
            margin: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            box-sizing: border-box !important;
        }

        div[class*="st-key-factory_header_sticky"] > div,
        div[class*="st-key-factory_header_sticky"] [data-testid="stVerticalBlockBorderWrapper"],
        div[class*="st-key-factory_header_sticky"] [data-testid="stVerticalBlock"] {
            max-width: 1320px !important;
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
            box-sizing: border-box !important;
            gap: 0.25rem !important;
        }

        div[class*="st-key-factory_header_sticky"] .factory-header-bar,
        div[class*="st-key-factory_header_sticky"] [data-testid="stHorizontalBlock"] {
            max-width: 1320px !important;
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-left: clamp(2rem, 4.5vw, 4rem) !important;
            padding-right: clamp(2rem, 4.5vw, 4rem) !important;
            box-sizing: border-box !important;
        }

        .factory-header-bar {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.2rem 0 0.45rem 0;
            margin-bottom: 0.15rem;
            border-bottom: 1px solid rgba(244, 43, 85, 0.12);
        }

        .header-left {
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
        }

        .header-brand-title {
            color: #f42b55;
            font-size: 1.5rem;
            font-weight: 850;
            letter-spacing: -0.03em;
        }

        .header-brand-sub {
            color: #64748b;
            font-size: 0.88rem;
            font-weight: 500;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 1.25rem;
        }

        .header-platform-note {
            color: #64748b;
            font-size: 0.88rem;
            font-weight: 500;
        }

        .header-icon-btn {
            position: relative;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(244, 43, 85, 0.06);
            border: 1px solid rgba(244, 43, 85, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .header-icon-btn:hover {
            background: rgba(244, 43, 85, 0.14);
            border-color: #f42b55;
        }

        .header-badge-dot {
            position: absolute;
            top: 7px;
            right: 7px;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #f42b55;
            box-shadow: 0 0 6px #f42b55;
        }

        .header-profile-badge {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: rgba(244, 43, 85, 0.08);
            border: 1px solid rgba(244, 43, 85, 0.28);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .header-profile-badge:hover {
            border-color: #f42b55;
            box-shadow: 0 0 14px rgba(244, 43, 85, 0.4);
        }

        .factory-nav-container {
            display: flex;
            align-items: center;
            gap: 0.35rem;
            flex-wrap: nowrap;
            width: 100%;
        }

        .factory-nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.45rem 0.72rem !important;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid rgba(244, 43, 85, 0.18) !important;
            color: #475569 !important;
            text-decoration: none !important;
            font-size: 0.82rem !important;
            font-weight: 550 !important;
            line-height: 1 !important;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
            transition: background 0.2s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
            box-sizing: border-box !important;
            height: 34px !important;
            max-height: 34px !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
        }

        .factory-nav-btn img {
            display: inline-block;
            vertical-align: middle;
            transition: filter 0.2s ease;
            filter: none;
        }

        .factory-nav-btn:hover {
            border-color: #f42b55 !important;
            color: #f42b55 !important;
            background: #fff0f3 !important;
        }

        .factory-nav-btn:hover img {
            filter: brightness(0) saturate(100%) invert(26%) sepia(88%) saturate(3475%) hue-rotate(334deg) brightness(98%) contrast(96%);
        }

        .factory-nav-btn.active,
        .factory-nav-btn.nav-item-active {
            background: linear-gradient(135deg, #f42b55 0%, #e11d48 100%) !important;
            border: 1px solid #f42b55 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(244, 43, 85, 0.35) !important;
            transform: none !important;
            height: 34px !important;
            max-height: 34px !important;
            padding: 0.45rem 0.72rem !important;
            font-size: 0.82rem !important;
            font-weight: 550 !important;
            box-sizing: border-box !important;
        }

        .factory-nav-btn.active *,
        .factory-nav-btn.nav-item-active * {
            color: #ffffff !important;
            stroke: #ffffff !important;
        }

        .factory-nav-btn.active img,
        .factory-nav-btn.nav-item-active img {
            filter: brightness(0) invert(1) !important;
        }

        /* Top Action Buttons (Refresh & Logout) */
        div[class*="st-key-top_refresh"] button,
        div[class*="st-key-top_logout"] button {
            background: #ffffff !important;
            color: #334155 !important;
            border: 1px solid rgba(244, 43, 85, 0.28) !important;
            border-radius: 8px !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            padding: 0.35rem 0.65rem !important;
            min-height: 34px !important;
            height: 34px !important;
            white-space: nowrap !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        div[class*="st-key-top_refresh"] button:hover {
            background: #fff5f7 !important;
            color: #f42b55 !important;
            border-color: #f42b55 !important;
            box-shadow: 0 4px 14px rgba(244, 43, 85, 0.16) !important;
            transform: translateY(-1px) !important;
        }

        div[class*="st-key-top_logout"] button:hover {
            background: #fff0f3 !important;
            color: #ef4444 !important;
            border-color: #ef4444 !important;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.16) !important;
            transform: translateY(-1px) !important;
        }


        /* ==================================================
           RESPONSIVE PRODUCTION LOGIN EXPERIENCE (FactoryOps)
           ================================================== */

        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        #MainMenu,
        footer {
            display: none !important;
            visibility: hidden !important;
        }

        .stApp {
            overflow-x: visible !important;
        }

        .login-backdrop-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #f42b55 0%, #ff4d6d 25%, #ffffff 80%, #fff0f3 100%);
            z-index: 9990;
            pointer-events: none;
        }

        [class*="st-key-login_frame"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            transform: none !important;
            z-index: 9999 !important;
            width: 100vw !important;
            height: 100vh !important;
            min-height: 100vh !important;
            margin: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            overflow: hidden !important;
            background: #ffffff !important;
            padding: 0 !important;
        }

        [class*="st-key-login_frame"] [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            width: 100vw !important;
            height: 100vh !important;
            min-height: 100vh !important;
            gap: 0 !important;
            margin: 0 !important;
            align-items: stretch !important;
        }

        [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(1) {
            padding: 0 !important;
            height: 100vh !important;
            min-height: 100vh !important;
            flex: 1 1 50% !important;
            width: 50vw !important;
            min-width: 50vw !important;
            max-width: 50vw !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .login-hero-container {
            width: 100%;
            height: 100% !important;
            min-height: 100vh !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-end !important;
            padding: clamp(2rem, 4.5vw, 4.5rem) !important;
            box-sizing: border-box !important;
            position: relative;
        }

        .login-hero-container::before {
            display: none !important;
        }

        .login-hero-content-box {
            position: relative;
            z-index: 2;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1.5px solid rgba(244, 43, 85, 0.28);
            border-radius: 20px;
            padding: 2rem 2.4rem;
            box-shadow: 0 20px 45px rgba(225, 29, 72, 0.12), 0 4px 14px rgba(0, 0, 0, 0.04);
        }

        .hero-title-brand {
            color: #0f172a;
            font-size: clamp(2.2rem, 3.2vw, 3.4rem);
            font-weight: 850;
            letter-spacing: -0.04em;
            line-height: 1.08;
            margin-bottom: 0.4rem;
        }

        .hero-title-brand span {
            color: #f42b55;
        }

        .hero-divider-bar {
            width: 48px;
            height: 4px;
            background: linear-gradient(90deg, #f42b55 0%, #fb7185 100%);
            margin-bottom: 0.75rem;
            border-radius: 2px;
            box-shadow: 0 2px 8px rgba(244, 43, 85, 0.4);
        }

        .hero-tagline-text {
            color: #334155;
            font-size: clamp(0.95rem, 1.1vw, 1.15rem);
            font-weight: 600;
            margin-bottom: 0;
            line-height: 1.4;
            letter-spacing: -0.01em;
        }

        [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(2) {
            padding: 0 !important;
            height: 100vh !important;
            min-height: 100vh !important;
            flex: 1 1 50% !important;
            width: 50vw !important;
            min-width: 50vw !important;
            max-width: 50vw !important;
            background: linear-gradient(180deg, #ffffff 0%, #fff5f7 100%) !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }

        [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(2) > div[data-testid="stVerticalBlock"] {
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 2rem !important;
            box-sizing: border-box !important;
            margin: 0 !important;
        }

        [class*="st-key-login_form_side"] {
            width: 100% !important;
            max-width: 440px !important;
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            box-shadow: none !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            box-sizing: border-box !important;
            margin: auto !important;
        }

        .login-form-eyebrow {
            color: #f42b55;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.35rem;
            text-align: left !important;
            width: 100% !important;
        }

        .login-form-heading {
            color: #0f172a;
            font-size: 2.6rem;
            font-weight: 750;
            letter-spacing: -0.03em;
            margin-bottom: 0.4rem;
            line-height: 1.1;
            text-align: left !important;
            width: 100% !important;
        }

        .login-form-subtitle {
            color: #64748b;
            font-size: 0.98rem;
            margin-bottom: 2rem;
            text-align: left !important;
            width: 100% !important;
        }

        [class*="st-key-login_portal"] {
            margin-bottom: 1.8rem !important;
            width: 100% !important;
            display: flex !important;
            justify-content: flex-start !important;
        }

        [class*="st-key-login_portal"] [data-testid="stRadio"] > label {
            display: none !important;
        }

        [class*="st-key-login_portal"] div[role="radiogroup"] {
            display: flex !important;
            flex-direction: row !important;
            justify-content: flex-start !important;
            gap: 2.5rem !important;
            width: 100% !important;
        }

        [class*="st-key-login_portal"] div[role="radiogroup"] label {
            display: flex !important;
            align-items: center !important;
            gap: 0.65rem !important;
            color: #334155 !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }

        [class*="st-key-login_portal"] div[role="radiogroup"] label p {
            color: #334155 !important;
            font-size: 1rem !important;
        }

        div[data-testid="stRadio"] [role="radiogroup"] label > div > div:nth-child(1),
        div[data-testid="stRadio"] [role="radiogroup"] input:checked ~ div:nth-of-type(1),
        [class*="st-key-login_portal"] div[role="radiogroup"] [data-baseweb="radio"] div {
            border-color: #f42b55 !important;
            background-color: transparent !important;
        }

        div[data-testid="stRadio"] div[class*="etak9228"],
        div[data-testid="stRadio"] [role="radiogroup"] input:checked ~ div:nth-of-type(2),
        div[data-testid="stRadio"] [role="radiogroup"] label > div > div:nth-of-type(2),
        div[data-testid="stRadio"] [role="radiogroup"] div[style*="255, 75, 75"] {
            background-color: #f42b55 !important;
            background: #f42b55 !important;
            border-color: #f42b55 !important;
        }

        div[data-testid="stForm"] {
            border: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            width: 100% !important;
        }

        div[data-testid="stForm"] [data-testid="stTextInput"] {
            margin-bottom: 1.4rem !important;
            width: 100% !important;
        }

        div[data-testid="stForm"] [data-testid="stTextInput"] label,
        div[data-testid="stForm"] [data-testid="stTextInput"] label p {
            color: #334155 !important;
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.45rem !important;
            text-align: left !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
            border: 1.5px solid rgba(244, 43, 85, 0.3) !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
            height: 50px !important;
            min-height: 50px !important;
            box-sizing: border-box !important;
            transition: all 0.2s ease !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"]:hover {
            border-color: #f42b55 !important;
            box-shadow: 0 0 12px rgba(244, 43, 85, 0.2) !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: #f42b55 !important;
            box-shadow: 0 0 14px rgba(244, 43, 85, 0.3) !important;
        }

        div[data-testid="stTextInput"] div[data-baseweb="input"] div,
        div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
            border: none !important;
            border-color: transparent !important;
            background-color: transparent !important;
            background: transparent !important;
            box-shadow: none !important;
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            align-items: center !important;
        }

        div[data-testid="stTextInput"] input,
        .stTextInput input,
        [data-testid="stTextInput"] input,
        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"] input,
        input[type="text"],
        input[type="password"] {
            background-color: transparent !important;
            background: transparent !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            caret-color: #f42b55 !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            font-size: 0.98rem !important;
            height: 48px !important;
            min-height: 48px !important;
            width: 100% !important;
            padding-right: 14px !important;
        }

        div[data-testid="stTextInput"] input:focus,
        .stTextInput input:focus,
        [data-testid="stTextInput"] input:focus,
        div[data-baseweb="input"] input:focus,
        div[data-baseweb="base-input"] input:focus,
        input[type="text"]:focus,
        input[type="password"]:focus {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
            caret-color: #f42b55 !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #94a3b8 !important;
            -webkit-text-fill-color: #94a3b8 !important;
            opacity: 0.9 !important;
        }

        div[data-testid="stTextInput"] input[aria-label="Username"] {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23f42b55' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: 14px center !important;
            padding-left: 44px !important;
        }

        div[data-testid="stTextInput"] input[aria-label="Password"] {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23f42b55' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect width='18' height='11' x='3' y='11' rx='2' ry='2'/%3E%3Cpath d='M7 11V7a5 5 0 0 1 10 0v4'/%3E%3C/svg%3E") !important;
            background-repeat: no-repeat !important;
            background-position: 14px center !important;
            padding-left: 44px !important;
        }

        [data-testid="stTextInput"] button {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: #f42b55 !important;
            background: transparent !important;
            background-color: transparent !important;
            margin-right: 8px !important;
        }

        [data-testid="stTextInput"] button svg,
        [data-testid="stTextInput"] button path {
            fill: none !important;
            stroke: #f42b55 !important;
            color: #f42b55 !important;
        }

        div[data-testid="stFormSubmitButton"] {
            width: 100% !important;
            margin-top: 1rem !important;
        }

        div[data-testid="stFormSubmitButton"] button,
        button[data-testid="stBaseButton-primaryFormSubmit"] {
            width: 100% !important;
            height: 50px !important;
            min-height: 50px !important;
            background: linear-gradient(135deg, #f42b55 0%, #e11d48 100%) !important;
            background-color: #f42b55 !important;
            border: none !important;
            outline: none !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            box-shadow: 0 8px 24px rgba(244, 43, 85, 0.4) !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
            background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
            background-color: #e11d48 !important;
            box-shadow: 0 12px 30px rgba(244, 43, 85, 0.55) !important;
            transform: translateY(-1px) !important;
        }

        div[data-testid="stFormSubmitButton"] button *,
        button[data-testid="stBaseButton-primaryFormSubmit"] * {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            color: #ffffff !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            display: inline-block !important;
            width: auto !important;
            height: auto !important;
            line-height: 1 !important;
        }

        @media (max-width: 900px) {
            [class*="st-key-login_frame"] > [data-testid="stHorizontalBlock"] {
                flex-direction: column !important;
            }
            [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(1) {
                min-height: 280px !important;
                height: 35vh !important;
                flex: none !important;
            }
            .login-hero-container {
                min-height: 280px !important;
                height: 35vh !important;
                padding: 1.5rem !important;
            }
            .login-hero-content-box {
                padding: 1.2rem 1.4rem !important;
            }
            [class*="st-key-login_frame"] [data-testid="stColumn"]:nth-of-type(2) {
                min-height: auto !important;
                padding: 2rem 1.2rem !important;
                flex: none !important;
            }
            [class*="st-key-login_form_side"] {
                width: 100% !important;
                max-width: 100% !important;
                padding: 2rem 1.5rem !important;
            }
        }


        /* ==================================================
           DASHBOARD HERO BANNER (SECTION 01)
           ================================================== */
        .dashboard-hero-banner {
            width: 100%;
            background: linear-gradient(135deg, #f42b55 0%, #e11d48 55%, #be123c 100%);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 20px;
            padding: 1.8rem 2.4rem;
            margin-top: 1rem;
            margin-bottom: 2.2rem;
            box-shadow: 0 16px 40px rgba(244, 43, 85, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            position: relative;
            overflow: hidden;
        }

        .banner-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
            width: 100%;
        }

        .banner-text-side {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .banner-kicker {
            color: #ffe4e8;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            margin-bottom: 0.35rem;
        }

        .banner-main-title {
            color: #ffffff;
            font-size: clamp(2rem, 2.8vw, 2.6rem);
            font-weight: 850;
            letter-spacing: -0.035em;
            line-height: 1.1;
            margin-bottom: 0.65rem;
        }

        .banner-accent-bar {
            width: 44px;
            height: 3px;
            background: #ffffff;
            border-radius: 2px;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.9);
        }

        .banner-subtitle {
            color: #ffe4e8;
            font-size: 0.95rem;
            font-weight: 400;
            line-height: 1.5;
            margin-top: 0.85rem;
            max-width: 460px;
        }

        .banner-graphic-side {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            flex-shrink: 0;
        }

        .banner-factory-img {
            width: clamp(200px, 22vw, 300px);
            height: auto;
            border-radius: 14px;
            border: 2px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            object-fit: cover;
        }

        /* Generic Section wrapper for Sections 02-08 */
        .factory-section {
            position: relative;
            width: 100%;
            background: #ffffff;
            border: 1px solid rgba(244, 43, 85, 0.16);
            border-left: 4px solid #f42b55;
            border-radius: 12px;
            padding: 0.65rem 1.25rem;
            margin-top: 1.6rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 3px 12px rgba(244, 43, 85, 0.05);
            box-sizing: border-box;
            display: flex;
            align-items: center;
        }

        .section-header {
            margin: 0;
            padding: 0;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .section-main-title {
            color: #0f172a;
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            line-height: 1.2;
            margin: 0;
        }

        .section-divider {
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(244, 43, 85, 0.22), transparent);
            margin: 1.8rem 0;
        }


        /* ==================================================
           KPI METRIC CARDS (2 ROWS OF 5 CARDS)
           ================================================== */
        .kpi-card {
            background: #ffffff;
            border: 1px solid rgba(244, 43, 85, 0.16);
            border-radius: 14px;
            padding: 0.9rem 1rem;
            min-height: 92px;
            height: 100%;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 16px rgba(244, 43, 85, 0.06), 0 1px 3px rgba(0, 0, 0, 0.03);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1rem;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: rgba(244, 43, 85, 0.45);
            box-shadow: 0 8px 24px rgba(244, 43, 85, 0.12);
            background: #ffffff;
        }

        .kpi-top-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            width: 100%;
            z-index: 2;
        }

        .kpi-icon-badge {
            width: 36px;
            height: 36px;
            min-width: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .kpi-badge-red {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #ef4444;
        }
        .kpi-badge-blue, .kpi-badge-cognac, .kpi-badge-rose {
            background: rgba(244, 43, 85, 0.12);
            border: 1px solid rgba(244, 43, 85, 0.3);
            color: #f42b55;
        }
        .kpi-badge-green {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #10b981;
        }
        .kpi-badge-orange {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: #f59e0b;
        }
        .kpi-badge-cyan {
            background: rgba(6, 182, 212, 0.12);
            border: 1px solid rgba(6, 182, 212, 0.3);
            color: #06b6d4;
        }
        .kpi-badge-purple {
            background: rgba(168, 85, 247, 0.12);
            border: 1px solid rgba(168, 85, 247, 0.3);
            color: #a855f7;
        }
        .kpi-badge-amber {
            background: rgba(234, 179, 8, 0.12);
            border: 1px solid rgba(234, 179, 8, 0.3);
            color: #eab308;
        }
        .kpi-badge-pink {
            background: rgba(236, 72, 153, 0.12);
            border: 1px solid rgba(236, 72, 153, 0.3);
            color: #ec4899;
        }

        .kpi-info {
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-width: 0;
            flex: 1;
            z-index: 2;
        }

        .kpi-label {
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            line-height: 1.15;
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .kpi-value {
            color: #0f172a !important;
            font-size: 1.28rem;
            font-weight: 850;
            letter-spacing: -0.02em;
            line-height: 1.15;
            margin-top: 1px;
            display: flex;
            align-items: baseline;
            gap: 4px;
            white-space: nowrap;
            overflow: hidden;
        }

        .metric-unit {
            font-size: 0.78rem;
            font-weight: 600;
            color: #f42b55;
            letter-spacing: 0;
        }

        .kpi-bottom-row {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            width: 100%;
            margin-top: 0.45rem;
            z-index: 2;
            position: relative;
        }

        .kpi-delta {
            font-size: 0.78rem;
            font-weight: 600;
            color: #64748b;
            line-height: 1;
        }

        .kpi-red .kpi-value {
            color: #ef4444 !important;
            text-shadow: 0 0 16px rgba(239, 68, 68, 0.25);
        }

        .kpi-sparkline-wrap {
            position: absolute;
            right: -8px;
            bottom: -8px;
            width: 125px;
            height: 40px;
            pointer-events: none;
            opacity: 0.45;
            z-index: 1;
        }


        /* ==================================================
           HEALTH OVERVIEW (DONUT & SUMMARY)
           ================================================== */
        .health-section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 2.2rem 0 1.2rem 0;
            width: 100%;
        }

        .health-header-left {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .health-title-row {
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }

        .health-title-text {
            color: #0f172a;
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.025em;
        }

        .health-subtitle-text {
            color: #64748b;
            font-size: 0.85rem;
            font-weight: 400;
        }

        .health-header-right {
            display: flex;
            align-items: center;
        }

        .health-filter-pill {
            background: #ffffff;
            border: 1px solid rgba(244, 43, 85, 0.2);
            border-radius: 8px;
            color: #475569;
            font-size: 0.82rem;
            font-weight: 500;
            padding: 6px 14px;
            display: flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .health-filter-pill:hover {
            border-color: #f42b55;
            color: #f42b55;
            background: #fff0f3;
        }

        .health-card {
            background: #ffffff;
            border: 1px solid rgba(244, 43, 85, 0.16);
            border-radius: 16px;
            padding: 1.5rem 1.6rem;
            height: 100%;
            box-sizing: border-box;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 24px rgba(244, 43, 85, 0.06);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .health-chart-title {
            color: #0f172a;
            font-size: 1.05rem;
            font-weight: 750;
            letter-spacing: -0.015em;
            margin-bottom: 0.2rem;
        }

        .health-chart-subtitle {
            color: #64748b;
            font-size: 0.82rem;
            font-weight: 400;
            margin-bottom: 0.9rem;
        }

        .health-donut-layout {
            display: flex;
            align-items: center;
            justify-content: space-around;
            gap: 1.5rem;
            padding-top: 0.8rem;
        }

        .health-donut-chart {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .health-donut-legend {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            flex-grow: 1;
        }

        .legend-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.35rem 0;
            border-bottom: 1px solid rgba(244, 43, 85, 0.08);
        }

        .legend-row:last-child {
            border-bottom: none;
        }

        .legend-left {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.85rem;
            font-weight: 550;
            color: #334155;
        }

        .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        .legend-dot.green { background: #10b981; box-shadow: 0 0 8px #10b981; }
        .legend-dot.orange { background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }
        .legend-dot.red { background: #ef4444; box-shadow: 0 0 8px #ef4444; }

        .legend-value {
            color: #0f172a;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .legend-percentage {
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 400;
            margin-left: 2px;
        }

        .health-metric-block {
            display: flex;
            flex-direction: column;
            gap: 0.95rem;
            margin-top: 0.6rem;
        }

        .metric-progress-item {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
        }

        .metric-row-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .metric-row-label {
            color: #334155;
            font-size: 0.84rem;
            font-weight: 600;
        }

        .metric-row-val {
            color: #0f172a;
            font-size: 0.88rem;
            font-weight: 700;
        }

        .metric-row-pct {
            color: #64748b;
            font-size: 0.78rem;
            font-weight: 400;
            margin-left: 3px;
        }

        .progress-track {
            width: 100%;
            height: 6px;
            background: rgba(244, 43, 85, 0.1);
            border-radius: 999px;
            overflow: hidden;
            position: relative;
        }

        .progress-fill {
            height: 100%;
            border-radius: 999px;
            transition: width 0.4s ease;
        }

        .progress-fill.green {
            background: linear-gradient(90deg, #059669, #10b981);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        }
        .progress-fill.orange {
            background: linear-gradient(90deg, #d97706, #f59e0b);
            box-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
        }
        .progress-fill.red {
            background: linear-gradient(90deg, #b91c1c, #ef4444);
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
        }


        /* ==================================================
           TABLES WITH PROPER BORDERS, MARGINS & STYLING
           ================================================== */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(244, 43, 85, 0.16) !important;
            border-radius: 16px !important;
            background: #ffffff !important;
            box-shadow: 0 8px 24px rgba(244, 43, 85, 0.06) !important;
            overflow: hidden !important;
            margin: 1.5rem 0 2rem 0 !important;
        }

        .factory-table-card {
            background: #ffffff;
            border: 1px solid rgba(244, 43, 85, 0.16);
            border-radius: 14px;
            padding: 0;
            overflow: hidden;
            margin: 0.75rem 0 1.5rem 0;
            box-shadow: 0 8px 24px rgba(244, 43, 85, 0.06);
            backdrop-filter: blur(14px);
        }

        .factory-table-scroll {
            max-height: 520px;
            overflow-y: auto;
            overflow-x: auto;
            width: 100%;
        }

        .factory-modern-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-family: inherit;
            font-size: 0.83rem;
            color: #1e293b;
        }

        .factory-modern-table thead {
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .factory-modern-table th {
            background: #fff0f3;
            color: #0f172a;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 9px 12px;
            border-bottom: 2px solid rgba(244, 43, 85, 0.28);
            border-right: 1px solid rgba(244, 43, 85, 0.1);
            white-space: nowrap;
            text-align: left;
        }

        .factory-modern-table th:last-child {
            border-right: none;
        }

        .factory-modern-table tbody tr {
            transition: background 0.15s ease;
        }

        .factory-modern-table tbody tr:nth-child(odd) {
            background: #ffffff;
        }

        .factory-modern-table tbody tr:nth-child(even) {
            background: #fffbfc;
        }

        .factory-modern-table tbody tr:hover {
            background: rgba(244, 43, 85, 0.06) !important;
        }

        .factory-modern-table td {
            padding: 8px 12px;
            border-bottom: 1px solid rgba(244, 43, 85, 0.09);
            border-right: 1px solid rgba(244, 43, 85, 0.06);
            color: #1e293b;
            vertical-align: middle;
            font-size: 0.83rem;
            line-height: 1.35;
        }

        .factory-modern-table td:last-child {
            border-right: none;
        }

        .factory-modern-table tbody tr:last-child td {
            border-bottom: none;
        }

        .tbl-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.15rem 0.55rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            line-height: 1;
        }

        .tbl-badge.badge-green {
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #059669;
        }

        .tbl-badge.badge-amber {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(245, 158, 11, 0.4);
            color: #d97706;
        }

        .tbl-badge.badge-red {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #dc2626;
        }

        .badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            display: inline-block;
        }

        .badge-dot.green { background: #10b981; box-shadow: 0 0 6px #10b981; }
        .badge-dot.amber { background: #f59e0b; box-shadow: 0 0 6px #f59e0b; }
        .badge-dot.red   { background: #ef4444; box-shadow: 0 0 6px #ef4444; }


        /* ==================================================
           GENERAL BUTTONS (Refresh, Logout, Actions)
           ================================================== */

        .stButton > button {
            background: #ffffff !important;
            border: 1px solid rgba(244, 43, 85, 0.32) !important;
            border-radius: 8px !important;
            color: #f42b55 !important;
            height: 35px !important;
            min-height: 35px !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            padding: 0 10px !important;
            white-space: nowrap !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 6px rgba(244, 43, 85, 0.08) !important;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #f42b55 0%, #e11d48 100%) !important;
            border-color: #f42b55 !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(244, 43, 85, 0.35) !important;
            transform: translateY(-1px) !important;
        }

        .quick-action-link {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 44px;
            box-sizing: border-box;
            background: #ffffff;
            border: 1px solid rgba(244, 43, 85, 0.25);
            border-radius: 8px;
            color: #f42b55;
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            box-shadow: 0 2px 6px rgba(244, 43, 85, 0.06);
            transition: all 0.2s ease;
        }

        .quick-action-link:hover {
            background: linear-gradient(135deg, #f42b55 0%, #e11d48 100%);
            border-color: #f42b55;
            color: #ffffff;
            box-shadow: 0 6px 18px rgba(244, 43, 85, 0.35);
            transform: translateY(-1px);
        }

        div[data-testid="stTextInput"] label p {
            color: #0f172a !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.35rem !important;
        }

        div[data-testid="stTextInput"] > div {
            border: 1px solid rgba(244, 43, 85, 0.25) !important;
            background: #ffffff !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stTextInput"] > div:hover {
            border-color: #f42b55 !important;
            box-shadow: 0 0 12px rgba(244, 43, 85, 0.2) !important;
        }

        div[data-testid="stTextInput"] input {
            color: #0f172a !important;
            background-color: transparent !important;
            background: transparent !important;
            font-size: 0.92rem !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #94a3b8 !important;
        }

        .footer-note {
            color: #64748b !important;
            font-size: 0.75rem;
            text-align: center;
            margin-top: 1.5rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        @media (max-width: 768px) {
            .factory-section {
                padding: 1.2rem 1rem 1.5rem 1rem;
                border-radius: 16px;
            }

            .section-main-title {
                font-size: 1.55rem;
            }
        }

    </style>    </style>
    """
)


# ============================================================
# SCROLL-SPY JAVASCRIPT
# ============================================================


def inject_scroll_spy():
    components.html(
        """
        <script>
        (() => {
            const parentDoc = window.parent.document;
            const parentWin = window.parent;

            function attachNavSystem() {
                const links = Array.from(parentDoc.querySelectorAll(".factory-nav-btn"));
                if (!links.length) {
                    setTimeout(attachNavSystem, 150);
                    return;
                }

                links.forEach((link) => {
                    if (link.dataset.hasClickListener) return;
                    link.dataset.hasClickListener = "true";

                    link.addEventListener("click", function(e) {
                        e.preventDefault();
                        e.stopPropagation();

                        // 1. Instantly highlight clicked button
                        links.forEach(l => l.classList.remove("active", "nav-item-active"));
                        this.classList.add("active", "nav-item-active");

                        // 2. Smoothly scroll to target section with offset
                        const targetId = this.getAttribute("data-target") || (this.getAttribute("href") || "").replace("#", "");
                        const targetEl = parentDoc.getElementById(targetId);

                        if (targetEl) {
                            parentWin.isClickScrolling = true;
                            clearTimeout(parentWin.clickScrollTimer);

                            const headerOffset = 120;
                            const scrollContainer = parentDoc.querySelector('section[data-testid="stMain"]') || parentDoc.querySelector('.main');

                            if (scrollContainer) {
                                const cTop = scrollContainer.getBoundingClientRect().top;
                                const elTop = targetEl.getBoundingClientRect().top;
                                const targetY = scrollContainer.scrollTop + (elTop - cTop) - headerOffset;
                                scrollContainer.scrollTo({ top: Math.max(0, targetY), behavior: "smooth" });
                            }
                            const winY = targetEl.getBoundingClientRect().top + parentWin.pageYOffset - headerOffset;
                            parentWin.scrollTo({ top: Math.max(0, winY), behavior: "smooth" });

                            parentWin.clickScrollTimer = setTimeout(() => {
                                parentWin.isClickScrolling = false;
                            }, 1600);
                        }
                    });
                });

                // Scroll-spy: update active nav button when scrolling past sections
                const updateActiveOnScroll = () => {
                    if (parentWin.isClickScrolling) return;

                    const scrollContainer = parentDoc.querySelector('section[data-testid="stMain"]') || parentDoc.querySelector('.main');
                    const scrollTop = scrollContainer ? scrollContainer.scrollTop : (parentWin.pageYOffset || parentDoc.documentElement.scrollTop || 0);
                    const scrollHeight = scrollContainer ? scrollContainer.scrollHeight : parentDoc.documentElement.scrollHeight;
                    const clientHeight = scrollContainer ? scrollContainer.clientHeight : parentWin.innerHeight;
                    const containerTop = scrollContainer ? scrollContainer.getBoundingClientRect().top : 0;

                    const distFromBottom = scrollHeight - (scrollTop + clientHeight);

                    // 1. If at bottom of page (within 85px), Help is the active section
                    if (distFromBottom <= 85) {
                        const lastLink = links[links.length - 1];
                        if (lastLink && !lastLink.classList.contains("nav-item-active")) {
                            links.forEach(l => l.classList.remove("active", "nav-item-active"));
                            lastLink.classList.add("active", "nav-item-active");
                        }
                        return;
                    }

                    // 2. Adaptive threshold for sections:
                    // As the page scrolls down towards the bottom, the detection threshold adapts
                    // so lower sections like Incidents highlight reliably when scrolled into view,
                    // without increasing any section or button width/height.
                    const maxScroll = Math.max(1, scrollHeight - clientHeight);
                    const scrollRatio = Math.min(1, Math.max(0, scrollTop / maxScroll));
                    const triggerThreshold = 155 + (scrollRatio * (clientHeight * 0.44));

                    let activeLink = links[0];
                    links.forEach((link) => {
                        const targetId = link.getAttribute("data-target") || (link.getAttribute("href") || "").replace("#", "");
                        const targetEl = parentDoc.getElementById(targetId);
                        if (targetEl) {
                            const elTop = targetEl.getBoundingClientRect().top - containerTop;
                            if (elTop <= triggerThreshold) {
                                activeLink = link;
                            }
                        }
                    });

                    if (activeLink && !activeLink.classList.contains("nav-item-active")) {
                        links.forEach(l => l.classList.remove("active", "nav-item-active"));
                        activeLink.classList.add("active", "nav-item-active");
                    }
                };

                const scrollContainer = parentDoc.querySelector('section[data-testid="stMain"]') || parentDoc.querySelector('.main');
                if (scrollContainer) {
                    scrollContainer.removeEventListener("scroll", updateActiveOnScroll);
                    scrollContainer.addEventListener("scroll", updateActiveOnScroll, { passive: true });
                }
                parentWin.removeEventListener("scroll", updateActiveOnScroll);
                parentWin.addEventListener("scroll", updateActiveOnScroll, { passive: true });
            }

            attachNavSystem();
            setInterval(attachNavSystem, 600);
        })();
        </script>
        """,
        height=1,
        width=1,
    )


# ============================================================
# API HELPERS
# ============================================================


def api_request(
    method: str,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
) -> Any:

    url = f"{API_BASE_URL}{path}"

    response = requests.request(
        method=method,
        url=url,
        params=params,
        json=json,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    if not response.content:
        return None

    return response.json()


def api_get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
) -> Any:

    return api_request(
        "GET",
        path,
        params=params,
    )


def extract_list(
    payload: Any,
) -> List[Dict[str, Any]]:

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):

        for key in (
            "items",
            "data",
            "results",
            "machines",
            "sensors",
            "predictions",
            "maintenance",
            "incidents",
        ):

            value = payload.get(key)

            if isinstance(value, list):
                return value

    return []


def safe_get(
    path: str,
    params: Optional[Dict[str, Any]] = None,
):

    try:

        return (
            api_get(
                path,
                params=params,
            ),
            None,
        )

    except requests.exceptions.ConnectionError:

        return (
            None,
            f"Cannot connect to backend at {API_BASE_URL}.",
        )

    except requests.exceptions.Timeout:

        return (
            None,
            "Backend request timed out.",
        )

    except requests.exceptions.HTTPError as exc:

        status = exc.response.status_code if exc.response is not None else "unknown"

        detail = ""

        try:
            detail = exc.response.json()
        except Exception:
            pass

        return (
            None,
            f"API returned HTTP {status}: {detail}",
        )

    except Exception as exc:

        return (
            None,
            str(exc),
        )


def fetch_first(
    paths: List[str],
):

    errors = []

    for path in paths:

        data, error = safe_get(path)

        if error is None:
            return data, None

        errors.append(f"{path}: {error}")

    return (
        None,
        " | ".join(errors),
    )


# ============================================================
# FORMATTERS
# ============================================================


def fmt_number(
    value: Any,
    digits: int = 2,
) -> str:

    if value is None or value == "":
        return "—"

    try:
        return f"{float(value):.{digits}f}"

    except Exception:
        return str(value)


def metric_card(
    label: str,
    value: Any,
    note: str = "",
    icon: str = "machines",
    color: str = "blue",
    unit: str = "",
    show_sparkline: bool = True,
):
    stroke_colors = {
        "red": "#ef4444",
        "blue": "#f42b55",
        "green": "#10b981",
        "orange": "#f59e0b",
        "cyan": "#06b6d4",
        "purple": "#a855f7",
        "amber": "#eab308",
        "pink": "#ec4899",
    }
    bg_tints = {
        "red": "rgba(239, 68, 68, 0.16)",
        "blue": "rgba(244, 43, 85, 0.12)",
        "green": "rgba(16, 185, 129, 0.16)",
        "orange": "rgba(245, 158, 11, 0.16)",
        "cyan": "rgba(6, 182, 212, 0.16)",
        "purple": "rgba(168, 85, 247, 0.16)",
        "amber": "rgba(234, 179, 8, 0.16)",
        "pink": "rgba(236, 72, 153, 0.16)",
    }
    border_tints = {
        "red": "rgba(239, 68, 68, 0.35)",
        "blue": "rgba(244, 43, 85, 0.3)",
        "green": "rgba(16, 185, 129, 0.35)",
        "orange": "rgba(245, 158, 11, 0.35)",
        "cyan": "rgba(6, 182, 212, 0.35)",
        "purple": "rgba(168, 85, 247, 0.35)",
        "amber": "rgba(234, 179, 8, 0.35)",
        "pink": "rgba(236, 72, 153, 0.35)",
    }

    stroke = stroke_colors.get(color, "#f42b55")
    bg_tint = bg_tints.get(color, "rgba(244, 43, 85, 0.12)")
    border_tint = border_tints.get(color, "rgba(244, 43, 85, 0.3)")

    raw_icons = {
        "shield": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "machines": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
        "healthy": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
        "warning": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        "critical": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/><line x1="2" y1="2" x2="22" y2="22"/></svg>',
        "health_rate": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "availability": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        "alerts": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
        "maintenance": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        "risk": f'<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    }

    spark_paths = {
        "shield": "M 0 35 Q 25 32, 50 28 T 85 30 T 115 20 T 140 12",
        "machines": "M 0 34 Q 25 30, 50 20 T 85 22 T 115 12 T 140 5",
        "healthy": "M 0 36 Q 30 33, 55 24 T 90 26 T 120 16 T 140 8",
        "warning": "M 0 35 Q 25 32, 55 22 T 85 24 T 115 14 T 140 6",
        "critical": "M 0 36 Q 20 33, 45 28 T 75 30 T 110 18 T 140 10",
        "health_rate": "M 0 35 Q 25 28, 50 18 T 80 22 T 110 12 T 140 6",
        "availability": "M 0 36 Q 30 32, 60 24 T 90 26 T 120 14 T 140 8",
        "alerts": "M 0 35 Q 20 32, 45 26 T 75 28 T 105 18 T 140 12",
        "maintenance": "M 0 36 Q 25 30, 50 20 T 80 24 T 115 12 T 140 6",
        "risk": "M 0 36 Q 20 33, 45 30 T 80 32 T 115 20 T 140 12",
    }

    icon_raw = raw_icons.get(icon, raw_icons["machines"])
    icon_img_html = svg_to_img(icon_raw, 22, 22)

    spark_d = spark_paths.get(icon, "M 0 35 Q 25 30, 50 20 T 85 22 T 115 12 T 140 6")
    spark_raw = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 45" fill="none"><path d="{spark_d}" stroke="{stroke}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    spark_img_html = svg_to_img(spark_raw, 125, 40, f"position:absolute; right:8px; bottom:6px; pointer-events:none; filter:drop-shadow(0 0 6px {stroke});")
    sparkline_html = f'<div class="kpi-sparkline-wrap">{spark_img_html}</div>' if show_sparkline else ""

    val_style = "color: #ef4444;" if color == "red" else "color: #0f172a;"
    unit_html = f'<span class="metric-unit">{unit}</span>' if unit else ""

    render_html(
        f"""
        <div class="kpi-card kpi-{color}">
            <div class="kpi-top-row">
                <div class="kpi-icon-badge" style="background:{bg_tint}; border:1px solid {border_tint}; box-shadow: 0 0 12px {bg_tint};">
                    {icon_img_html}
                </div>
                <div class="kpi-info">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value" style="{val_style}">{value}{unit_html}</div>
                </div>
            </div>
            {f'<div class="kpi-bottom-row"><div class="kpi-delta" style="color:{stroke};">{note}</div>{sparkline_html}</div>' if (note or sparkline_html) else ''}
        </div>
        """
    )


def normalize_dataframe(
    rows: List[Dict[str, Any]],
) -> pd.DataFrame:

    if not rows:
        return pd.DataFrame()

    return pd.json_normalize(rows)


# ============================================================
# TABLE DISPLAY HELPER
# ============================================================


def format_cell_value(col_name: str, val: Any) -> str:
    if pd.isna(val) or val is None or str(val).strip() == "" or str(val).strip() == "—":
        return '<span style="color:#64748b;">—</span>'

    val_str = str(val).strip()
    lower_val = val_str.lower()

    if lower_val in ["healthy", "normal", "low", "optimal", "passed", "resolved", "completed"]:
        return f'<span class="tbl-badge badge-green"><span class="badge-dot green"></span>{val_str}</span>'
    elif lower_val in ["warning", "medium", "moderate", "degraded", "pending", "in_progress"]:
        return f'<span class="tbl-badge badge-amber"><span class="badge-dot amber"></span>{val_str}</span>'
    elif lower_val in ["critical", "high", "failed", "danger", "error", "open"]:
        return f'<span class="tbl-badge badge-red"><span class="badge-dot red"></span>{val_str}</span>'

    if isinstance(val, float):
        if "score" in col_name.lower() or "prob" in col_name.lower() or "percent" in col_name.lower() or "availability" in col_name.lower():
            return f'<span style="font-weight:600; color:#f42b55;">{val:.1f}%</span>'
        return f'{val:.2f}'
    elif isinstance(val, int) and not isinstance(val, bool):
        if "score" in col_name.lower() or "prob" in col_name.lower() or "percent" in col_name.lower():
            return f'<span style="font-weight:600; color:#f42b55;">{val}%</span>'
        return f'{val:,}'

    return val_str


def display_table(
    df: pd.DataFrame,
    units: Optional[Dict[str, str]] = None,
):
    if df.empty:
        st.info("No data available.")
        return

    units = units or {}
    display_df = df.copy()

    for column, unit in units.items():
        if column in display_df.columns:
            display_df[column] = display_df[column].apply(
                lambda value: "—" if pd.isna(value) else f"{value} {unit}"
            )

    headers = list(display_df.columns)
    th_cells = "".join(f'<th>{h.replace("_", " ").title()}</th>' for h in headers)

    rows_markup = []
    for _, row in display_df.iterrows():
        td_cells = []
        for col in headers:
            raw_val = row[col]
            formatted = format_cell_value(col, raw_val)
            td_cells.append(f'<td style="text-align:right;">{formatted}</td>')
        rows_markup.append(f'<tr>{"".join(td_cells)}</tr>')

    table_html = f"""
    <div class="factory-table-card">
        <div class="factory-table-scroll">
            <table class="factory-modern-table">
                <thead>
                    <tr>{th_cells}</tr>
                </thead>
                <tbody>
                    {"".join(rows_markup)}
                </tbody>
            </table>
        </div>
    </div>
    """
    render_html(table_html)


# ============================================================
# SECTION WRAPPERS
# ============================================================


def section_start(
    section_id: str,
    number: str,
    title: str,
    description: str = "",
):
    if section_id == "factory-dashboard":
        banner_b64 = get_banner_img_base64()
        render_html(
            f"""
            <div id="{section_id}" style="width:100%;">
                <div class="dashboard-hero-banner">
                    <div class="banner-content">
                        <div class="banner-text-side">
                            <div class="banner-main-title">{title}</div>
                            <div class="banner-accent-bar"></div>
                            <div class="banner-subtitle">Real-time overview of your factory operations and predictive insights</div>
                        </div>
                        <div class="banner-graphic-side">
                            <img src="data:image/jpeg;base64,{banner_b64}" class="banner-factory-img" alt="Smart Factory Platform" />
                        </div>
                    </div>
                </div>
            </div>
            """
        )
    else:
        render_html(
            f"""
            <div id="{section_id}" class="factory-section">
                <div class="section-header">
                    <div class="section-main-title">{title}</div>
                </div>
            </div>
            """
        )


def section_end():
    render_html(
        """
        </section>
        """
    )


def top_navigation(pages: List[str]):
    username = st.session_state.get("username", "Admin")

    bell_svg = svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>', 18, 18)
    profile_svg = svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f42b55" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>', 18, 18)

    nav_icons = {
        "Dashboard": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>', 16, 16),
        "Machines": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>', 16, 16),
        "Sensors": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 6a6 6 0 0 1 6 6"/><path d="M12 10a2 2 0 0 1 2 2"/><circle cx="12" cy="12" r="1"/></svg>', 16, 16),
        "Predictions": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>', 16, 16),
        "Risk Analysis": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>', 16, 16),
        "Maintenance": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>', 16, 16),
        "Incidents": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>', 16, 16),
        "Help": svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>', 16, 16),
    }

    links_html = []
    for i, page in enumerate(pages):
        slug = f"factory-{page.lower().replace(' ', '-')}"
        active_cls = "nav-item-active" if i == 0 else ""
        icon = nav_icons.get(page, "")
        links_html.append(
            f'<a href="#{slug}" class="factory-nav-btn {active_cls}" data-target="{slug}">'
            f'{icon}<span>{page}</span>'
            f'</a>'
        )
    nav_links_joined = "".join(links_html)

    # Wrap the entire header and nav row in one constant fixed container
    with st.container(key="factory_header_sticky"):
        render_html(
            f"""
            <header class="factory-header-bar">
                <div class="header-left">
                    <span class="header-brand-title">FactoryOps</span>
                    <span class="header-brand-sub">Smart Factory Intelligence</span>
                </div>
                <div class="header-right">
                    <div class="header-icon-btn" title="System Notifications">
                        {bell_svg}
                        <span class="header-badge-dot"></span>
                    </div>
                    <div class="header-profile-badge" title="Logged in as {username}">
                        {profile_svg}
                    </div>
                </div>
            </header>
            """
        )

        nav_col, action_col = st.columns([7.3, 2.7], gap="small")
        with nav_col:
            render_html(f'<div class="factory-nav-container">{nav_links_joined}</div>')
        with action_col:
            if st.button("Logout", use_container_width=True, key="top_logout"):
                st.session_state.clear()
                st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================


def login_page():
    bg_base64 = get_login_bg_base64()

    render_html(
        """
        <style>
        .block-container, [data-testid="stAppViewBlockContainer"], [data-testid="stMainBlockContainer"], .main .block-container {
            max-width: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        </style>
        <div class="login-backdrop-overlay"></div>
        """
    )

    with st.container(key="login_frame"):
        col1, col2 = st.columns([1, 1], gap="small")

        with col1:
            mime = "image/png" if bg_base64.startswith("iVBORw0KGgo") else "image/jpeg"
            render_html(
                f"""
                <div class="login-hero-container" style="background-image: url('data:{mime};base64,{bg_base64}');">
                    <div class="login-hero-content-box">
                        <div class="hero-title-brand">Factory<span>Ops</span></div>
                        <div class="hero-divider-bar"></div>
                        <div class="hero-tagline-text">Smart Operations. Stronger Tomorrow.</div>
                    </div>
                </div>
                """
            )

        with col2:
            render_html(
                """
                <script>
                (() => {
                    function applyMockupTheme() {
                        document.querySelectorAll('[data-testid="stTextInput"] div[data-baseweb="input"]').forEach(el => {
                            el.style.setProperty('background-color', '#ffffff', 'important');
                            el.style.setProperty('border', '1.5px solid rgba(244, 43, 85, 0.35)', 'important');
                            el.style.setProperty('border-radius', '12px', 'important');
                        });
                        document.querySelectorAll('[data-testid="stTextInput"] div[data-baseweb="input"] div, [data-testid="stTextInput"] div[data-baseweb="base-input"]').forEach(el => {
                            el.style.setProperty('background-color', 'transparent', 'important');
                            el.style.setProperty('border', 'none', 'important');
                        });
                        document.querySelectorAll('[data-testid="stTextInput"] input').forEach(el => {
                            el.style.setProperty('background-color', 'transparent', 'important');
                            el.style.setProperty('color', '#0f172a', 'important');
                            el.style.setProperty('-webkit-text-fill-color', '#0f172a', 'important');
                        });
                        document.querySelectorAll('[data-testid="stRadio"] [role="radiogroup"] input:checked').forEach(radio => {
                            const container = radio.closest('label');
                            if (container) {
                                const dots = container.querySelectorAll('div > div');
                                if (dots.length > 1) {
                                    dots[1].style.setProperty('background-color', '#f42b55', 'important');
                                }
                            }
                        });
                    }
                    applyMockupTheme();
                    setInterval(applyMockupTheme, 250);
                })();
                </script>
                """
            )

            with st.container(key="login_form_side"):
                render_html(
                    """
                    <div class="login-form-eyebrow">Login to your account!</div>
                    <div class="login-form-heading">Welcome Back!</div>
                    <div class="login-form-subtitle">Please enter your details to continue</div>
                    """
                )

                portal = st.radio(
                    "Portal",
                    ["User Portal", "Admin Portal"],
                    horizontal=True,
                    label_visibility="collapsed",
                    key="login_portal",
                )

                with st.form("login_form", clear_on_submit=False):
                    username = st.text_input(
                        "Username",
                        placeholder="Enter your username",
                        key="login_username",
                    )
                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter your password",
                        key="login_password",
                    )
                    submitted = st.form_submit_button(
                        "Sign In",
                        use_container_width=True,
                        type="primary",
                    )

    if submitted:
        valid_admin = (
            portal == "Admin Portal"
            and username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        )
        valid_user = (
            portal == "User Portal"
            and username == USER_USERNAME
            and password == USER_PASSWORD
        )

        if valid_admin or valid_user:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = "admin" if valid_admin else "user"
            st.session_state.page = "Dashboard"
            st.rerun()
        else:
            st.error("Invalid username or password for the selected portal.")


# ============================================================
# DASHBOARD
# ============================================================


def dashboard_page():

    section_start(
        "factory-dashboard",
        "01",
        "Factory Dashboard",
    )

    dashboard, error = safe_get("/dashboard/summary")

    if error:

        st.error(error)

        st.info("Start the backend first, then refresh this page.")

        section_end()
        return

    if not isinstance(
        dashboard,
        dict,
    ):

        st.error("Dashboard API returned an unexpected response.")

        section_end()
        return

    cols = st.columns(5, gap="medium")
    with cols[0]:
        metric_card(
            "Factory Status",
            dashboard.get("factory_status", "—"),
            note="↑ 12% from yesterday",
            icon="shield",
            color="red",
        )
    with cols[1]:
        metric_card(
            "Total Machines",
            dashboard.get("total_machines", 0),
            note="↑ 8% from yesterday",
            icon="machines",
            color="blue",
        )
    with cols[2]:
        metric_card(
            "Healthy",
            dashboard.get("healthy_machines", 0),
            note="↑ 5% from yesterday",
            icon="healthy",
            color="green",
        )
    with cols[3]:
        metric_card(
            "Warning",
            dashboard.get("warning_machines", 0),
            note="↓ 3% from yesterday",
            icon="warning",
            color="orange",
        )
    with cols[4]:
        metric_card(
            "Critical",
            dashboard.get("critical_machines", 0),
            note="↑ 15% from yesterday",
            icon="critical",
            color="red",
        )

    cols = st.columns(5, gap="medium")
    with cols[0]:
        metric_card(
            "Average Health",
            f"{fmt_number(dashboard.get('average_health_score'), 1)}%",
            note="↑ 2.3% from yesterday",
            icon="health_rate",
            color="blue",
        )
    with cols[1]:
        metric_card(
            "Availability",
            dashboard.get("machine_availability", "—"),
            note="↑ 1.8% from yesterday",
            icon="availability",
            color="cyan",
        )
    with cols[2]:
        metric_card(
            "Active Alerts",
            dashboard.get("active_alerts", 0),
            note="↑ 10% from yesterday",
            icon="alerts",
            color="purple",
        )
    with cols[3]:
        metric_card(
            "Maintenance Due",
            dashboard.get("maintenance_due", 0),
            note="↓ 6% from yesterday",
            icon="maintenance",
            color="amber",
        )
    with cols[4]:
        metric_card(
            "High Failure Risk",
            dashboard.get("high_failure_risk", 0),
            note="↑ 14% from yesterday",
            icon="risk",
            color="pink",
        )

    pulse_icon = svg_to_img('<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#f42b55" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>', 22, 22)
    render_html(
        f"""
        <div class="health-section-header">
            <div class="health-header-left">
                <div class="health-title-row">
                    {pulse_icon}
                    <span class="health-title-text">Health Overview</span>
                </div>
                <div class="health-subtitle-text">Overall equipment health distribution</div>
            </div>
        </div>
        """
    )

    healthy = int(
        dashboard.get(
            "healthy_machines",
            0,
        )
        or 0
    )

    warning = int(
        dashboard.get(
            "warning_machines",
            0,
        )
        or 0
    )

    critical = int(
        dashboard.get(
            "critical_machines",
            0,
        )
        or 0
    )

    total_health = healthy + warning + critical

    healthy_percent = healthy / total_health * 100 if total_health else 0
    warning_percent = warning / total_health * 100 if total_health else 0
    critical_percent = critical / total_health * 100 if total_health else 0

    if total_health > 0:
        health_data = pd.DataFrame(
            {
                "Status": ["Healthy", "Warning", "Critical"],
                "Machines": [healthy, warning, critical],
            }
        )

        chart_col, summary_col = st.columns([1.15, 1], gap="medium")

        with chart_col:
            circ = 326.73
            r_val = 52
            cx_val = 80
            cy_val = 80

            len_crit = (critical / total_health) * circ if total_health else 0
            len_warn = (warning / total_health) * circ if total_health else 0
            len_hlth = (healthy / total_health) * circ if total_health else 0

            offset_crit = 0.0
            offset_warn = -len_crit
            offset_hlth = -(len_crit + len_warn)

            donut_raw = f"""<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 160 160">
                <circle cx="{cx_val}" cy="{cy_val}" r="{r_val}" fill="none" stroke="#ef4444" stroke-width="26"
                    stroke-dasharray="{len_crit:.2f} {circ:.2f}" stroke-dashoffset="{offset_crit:.2f}" transform="rotate(-90 {cx_val} {cy_val})" />
                <circle cx="{cx_val}" cy="{cy_val}" r="{r_val}" fill="none" stroke="#f59e0b" stroke-width="26"
                    stroke-dasharray="{len_warn:.2f} {circ:.2f}" stroke-dashoffset="{offset_warn:.2f}" transform="rotate(-90 {cx_val} {cy_val})" />
                <circle cx="{cx_val}" cy="{cy_val}" r="{r_val}" fill="none" stroke="#10b981" stroke-width="26"
                    stroke-dasharray="{len_hlth:.2f} {circ:.2f}" stroke-dashoffset="{offset_hlth:.2f}" transform="rotate(-90 {cx_val} {cy_val})" />
                <circle cx="{cx_val}" cy="{cy_val}" r="39" fill="#ffffff" />
            </svg>"""
            donut_img_html = svg_to_img(donut_raw, 160, 160)

            render_html(
                f"""
                <div class="health-card">
                    <div class="health-chart-title">
                        Machine Health Overview
                    </div>
                    <div class="health-chart-subtitle">
                        Distribution of current machine health status
                    </div>
                    <div class="health-donut-layout" style="display:flex; align-items:center; justify-content:space-around; gap:1.5rem; padding-top:0.8rem;">
                        <div class="health-donut-chart">
                            {donut_img_html}
                        </div>
                        <div class="health-donut-legend">
                            <div class="legend-row">
                                <div class="legend-left">
                                    <span class="legend-dot green"></span>
                                    Healthy
                                </div>
                                <div class="legend-value">
                                    {healthy} <span class="legend-percentage">({healthy_percent:.1f}%)</span>
                                </div>
                            </div>
                            <div class="legend-row">
                                <div class="legend-left">
                                    <span class="legend-dot orange"></span>
                                    Warning
                                </div>
                                <div class="legend-value">
                                    {warning} <span class="legend-percentage">({warning_percent:.1f}%)</span>
                                </div>
                            </div>
                            <div class="legend-row">
                                <div class="legend-left">
                                    <span class="legend-dot red"></span>
                                    Critical
                                </div>
                                <div class="legend-value">
                                    {critical} <span class="legend-percentage">({critical_percent:.1f}%)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """
            )

        with summary_col:
            render_html(
                f"""
                <div class="health-card">
                    <div class="health-chart-title">
                        Health Summary
                    </div>
                    <div class="health-progress-summary">
                        <div class="progress-item">
                            <div class="progress-info">
                                <div class="progress-label">
                                    <span class="legend-dot green"></span>
                                    Healthy
                                </div>
                                <div class="progress-count">
                                    {healthy} <span class="progress-pct">({healthy_percent:.1f}%)</span>
                                </div>
                            </div>
                            <div class="progress-track">
                                <div class="progress-fill green" style="width: {max(2.0, healthy_percent):.1f}%;"></div>
                            </div>
                        </div>
                        <div class="progress-item">
                            <div class="progress-info">
                                <div class="progress-label">
                                    <span class="legend-dot orange"></span>
                                    Warning
                                </div>
                                <div class="progress-count">
                                    {warning} <span class="progress-pct">({warning_percent:.1f}%)</span>
                                </div>
                            </div>
                            <div class="progress-track">
                                <div class="progress-fill orange" style="width: {max(2.0, warning_percent):.1f}%;"></div>
                            </div>
                        </div>
                        <div class="progress-item">
                            <div class="progress-info">
                                <div class="progress-label">
                                    <span class="legend-dot red"></span>
                                    Critical
                                </div>
                                <div class="progress-count">
                                    {critical} <span class="progress-pct">({critical_percent:.1f}%)</span>
                                </div>
                            </div>
                            <div class="progress-track">
                                <div class="progress-fill red" style="width: {max(2.0, critical_percent):.1f}%;"></div>
                            </div>
                        </div>
                    </div>
                </div>
                """
            )
    else:
        st.info("No machine health data is currently available.")

    render_html(
        """
        <div class="section-title">
            Quick Actions
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        render_html(
            '<a class="quick-action-link" href="#factory-machines">View Machines</a>'
        )

    with c2:
        render_html(
            '<a class="quick-action-link" href="#factory-predictions">View Predictions</a>'
        )

    with c3:
        render_html(
            '<a class="quick-action-link" href="#factory-incidents">View Incidents</a>'
        )

    section_end()


# ============================================================
# MACHINES
# ============================================================


def machines_page():

    section_start(
        "factory-machines",
        "02",
        "Machines",
    )

    data, error = fetch_first(
        [
            "/machines",
            "/machine",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.warning("No machines returned by the API.")

    else:
        df = normalize_dataframe(rows)

        search = st.text_input(
            "Search machine",
            placeholder="Machine code or name",
            key="machines_search",
        )

        if search:

            mask = (
                df.astype(str)
                .apply(
                    lambda col: col.str.contains(
                        search,
                        case=False,
                        na=False,
                    )
                )
                .any(axis=1)
            )

            df = df[mask]

        display_table(df)

        st.caption(f"{len(df)} machine(s) shown.")

    if st.session_state.get("role") == "admin":
        with st.expander("Admin machine controls"):
            add_col, remove_col = st.columns(2)

            with add_col:
                st.markdown("**Add machine**")
                with st.form("add_machine_form", clear_on_submit=True):
                    machine_code = st.text_input("Machine code")
                    machine_name = st.text_input("Machine name")
                    machine_type = st.text_input("Machine type")
                    department = st.text_input("Department")
                    operating_hours = st.number_input(
                        "Operating hours",
                        min_value=0.0,
                        step=1.0,
                    )
                    add_machine = st.form_submit_button(
                        "Add machine",
                        type="primary",
                    )

                if add_machine:
                    payload = {
                        "machine_code": machine_code.strip(),
                        "machine_name": machine_name.strip(),
                        "machine_type": machine_type.strip(),
                        "department": department.strip(),
                        "operating_hours": operating_hours,
                        "health_status": "Healthy",
                    }
                    if not all(payload[key] for key in (
                        "machine_code",
                        "machine_name",
                        "machine_type",
                        "department",
                    )):
                        st.error("Complete all machine fields before adding it.")
                    else:
                        try:
                            api_request("POST", "/machines/", json=payload)
                            st.success("Machine added.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Could not add machine: {exc}")

            with remove_col:
                st.markdown("**Remove machine**")
                remove_id = st.number_input(
                    "Machine ID to remove",
                    min_value=1,
                    step=1,
                    key="admin_remove_machine_id",
                )
                if st.button("Remove machine", key="admin_remove_machine"):
                    try:
                        api_request("DELETE", f"/machines/{int(remove_id)}")
                        st.success("Machine removed.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not remove machine: {exc}")

    section_end()


# ============================================================
# SENSORS
# ============================================================


def sensors_page():

    section_start(
        "factory-sensors",
        "03",
        "Sensor Monitoring",
    )

    machine_id = st.number_input(
        "Machine ID",
        min_value=1,
        value=100,
        step=1,
        key="sensor_machine_id",
    )

    data, error = fetch_first(
        [
            f"/sensors/machine/{machine_id}",
            f"/sensors?machine_id={machine_id}",
        ]
    )

    if error:

        data, error = fetch_first(
            [
                "/sensors",
                "/sensor",
            ]
        )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.warning("No sensor readings found.")

        section_end()
        return

    df = normalize_dataframe(rows)

    numeric_cols = [
        column
        for column in [
            "temperature",
            "vibration",
            "pressure",
            "humidity",
            "voltage",
            "current",
        ]
        if column in df.columns
    ]

    short_units = {
        "temperature": "°C",
        "vibration": "mm/s",
        "pressure": "bar",
        "humidity": "%",
        "voltage": "V",
        "current": "A",
    }

    sensor_icons = {
        "temperature": "critical",
        "vibration": "health_rate",
        "pressure": "warning",
        "humidity": "availability",
        "voltage": "alerts",
        "current": "risk",
    }

    sensor_colors = {
        "temperature": "red",
        "vibration": "green",
        "pressure": "orange",
        "humidity": "cyan",
        "voltage": "amber",
        "current": "purple",
    }

    table_units = {
        "temperature": "Celsius (°C)",
        "vibration": "millimeters per second (mm/s)",
        "pressure": "bar",
        "humidity": "percent (%)",
        "voltage": "volts (V)",
        "current": "amperes (A)",
    }

    if numeric_cols:

        render_html(
            """
            <div class="section-title" style="color:#0f172a; font-size:1.15rem; font-weight:750; margin:1rem 0 0.6rem 0;">
                Latest Reading
            </div>
            """
        )

        latest = df.iloc[0]

        cols = st.columns(
            min(
                len(numeric_cols),
                6,
            )
        )

        for column, sensor_name in zip(
            cols,
            numeric_cols,
        ):

            with column:
                unit = short_units.get(sensor_name, "")
                raw_val = latest[sensor_name]
                if isinstance(raw_val, float):
                    value = f"{raw_val:.1f}"
                elif isinstance(raw_val, int):
                    value = f"{raw_val:,}"
                else:
                    value = str(raw_val)

                s_icon = sensor_icons.get(sensor_name, "machines")
                s_color = sensor_colors.get(sensor_name, "blue")

                metric_card(
                    sensor_name.replace(
                        "_",
                        " ",
                    ).title(),
                    value,
                    unit=unit,
                    icon=s_icon,
                    color=s_color,
                    show_sparkline=False,
                )

    render_html(
        """
        <div class="section-title" style="color:#0f172a; font-size:1.15rem; font-weight:750; margin:1.5rem 0 0.6rem 0;">
            Sensor Data
        </div>
        """
    )

    display_table(df, units=table_units)

    section_end()


# ============================================================
# PREDICTIONS
# ============================================================


def predictions_page():

    section_start(
        "factory-predictions",
        "04",
        "Failure Predictions",
    )

    data, error = fetch_first(
        [
            "/predictions",
            "/prediction",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.warning("No predictions returned by the API.")

        section_end()
        return

    df = normalize_dataframe(rows)

    if "risk_level" in df.columns:

        risk_filter = st.selectbox(
            "Risk Level",
            options=["High", "Medium", "Low"],
            index=None,
            placeholder="Select risk level",
            key="prediction_risk_filter",
        )

        if risk_filter:
            df = df[df["risk_level"].astype(str).str.lower().eq(risk_filter.lower())]

    if "health_score" in df.columns:

        df["health_score"] = pd.to_numeric(
            df["health_score"],
            errors="coerce",
        )

    if "failure_probability" in df.columns:

        df["failure_probability"] = pd.to_numeric(
            df["failure_probability"],
            errors="coerce",
        )

    c1, c2, c3 = st.columns(3)

    with c1:

        high_count = (
            int((df["risk_level"].astype(str).str.lower() == "high").sum())
            if "risk_level" in df.columns
            else 0
        )

        metric_card(
            "High Risk",
            high_count,
        )

    with c2:

        avg_health = df["health_score"].mean() if "health_score" in df.columns else 0

        metric_card(
            "Average Health",
            f"{avg_health:.1f}%",
        )

    with c3:

        avg_probability = (
            df["failure_probability"].mean()
            if "failure_probability" in df.columns
            else 0
        )

        metric_card(
            "Avg Failure Probability",
            f"{avg_probability:.1f}%",
        )

    preferred = [
        "machine_id",
        "health_score",
        "failure_probability",
        "risk_level",
        "predicted_failure",
        "estimated_failure_days",
        "confidence_score",
    ]

    visible = [column for column in preferred if column in df.columns]

    display_df = df[visible] if visible else df

    display_table(display_df)

    section_end()


# ============================================================
# RISK ANALYSIS
# ============================================================


def risk_page():
    section_start(
        "factory-risk-analysis",
        "05",
        "Risk Analysis",
    )

    data, error = fetch_first(["/predictions", "/prediction"])

    if error:
        st.error(error)
        section_end()
        return

    rows = extract_list(data)
    if not rows:
        st.info("No prediction data is currently available.")
        section_end()
        return

    df = normalize_dataframe(rows)

    if "risk_level" not in df.columns:
        st.info("Risk level is not available in the prediction response.")
        section_end()
        return

    selected = st.selectbox(
        "Risk Level",
        ["High", "Medium", "Low"],
        index=None,
        placeholder="Select risk level",
        key="risk_analysis_filter",
    )

    if selected:
        df = df[df["risk_level"].astype(str).str.lower().eq(selected.lower())]

    display_table(df)
    st.caption(f"{len(df)} risk record(s) shown.")

    section_end()


# ============================================================
# MAINTENANCE
# ============================================================


def maintenance_page():

    section_start(
        "factory-maintenance",
        "06",
        "Maintenance",
    )

    data, error = fetch_first(
        [
            "/maintenance",
            "/maintenances",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if rows:

        df = normalize_dataframe(rows)

        display_table(df)

        st.caption(f"{len(df)} maintenance record(s) shown.")

    else:

        st.info("No maintenance records are currently available.")

    if st.session_state.get("role") == "admin":
        with st.expander("Admin repair controls"):
            st.markdown("**Log a maintenance or repair job**")
            with st.form("add_maintenance_form", clear_on_submit=True):
                repair_machine_id = st.number_input(
                    "Machine ID",
                    min_value=1,
                    step=1,
                    key="admin_repair_machine_id",
                )
                repair_type = st.text_input(
                    "Repair type",
                    value="Corrective repair",
                )
                repair_priority = st.selectbox(
                    "Priority",
                    ["Low", "Medium", "High", "Critical"],
                )
                repair_engineer = st.text_input("Engineer")
                repair_date = st.date_input(
                    "Scheduled date",
                    value=datetime.utcnow().date(),
                )
                repair_status = st.selectbox(
                    "Status",
                    ["Scheduled", "In Progress", "Completed", "Cancelled"],
                )
                repair_remarks = st.text_area("Remarks")
                add_repair = st.form_submit_button(
                    "Save repair job",
                    type="primary",
                )

            if add_repair:
                payload = {
                    "machine_id": int(repair_machine_id),
                    "maintenance_type": repair_type.strip(),
                    "priority": repair_priority,
                    "engineer": repair_engineer.strip(),
                    "scheduled_date": datetime.combine(
                        repair_date,
                        datetime.min.time(),
                    ).isoformat(),
                    "completion_status": repair_status,
                    "remarks": repair_remarks.strip(),
                }
                if not payload["maintenance_type"] or not payload["engineer"]:
                    st.error("Enter a repair type and engineer.")
                else:
                    try:
                        api_request("POST", "/maintenance/", json=payload)
                        st.success("Repair job saved.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not save repair job: {exc}")

    render_html(
        """
        <div class="section-title">
            Maintenance Recommendation
        </div>
        """
    )

    machine_id = st.number_input(
        "Machine ID for recommendation",
        min_value=1,
        value=1,
        step=1,
        key="maintenance_machine_id",
    )

    if st.button(
        "Get Recommendation",
        type="primary",
        key="get_maintenance_recommendation",
    ):

        prediction_data, prediction_error = fetch_first(
            [
                f"/predictions/machine/{machine_id}",
                f"/predictions/{machine_id}",
            ]
        )

        if prediction_error:

            st.error(prediction_error)

            section_end()
            return

        prediction_rows = extract_list(prediction_data)

        prediction = (
            prediction_rows[0]
            if prediction_rows
            else (
                prediction_data
                if isinstance(
                    prediction_data,
                    dict,
                )
                else None
            )
        )

        if not prediction:

            st.warning("No prediction found for this machine.")

            section_end()
            return

        st.json(prediction)

    section_end()


# ============================================================
# INCIDENTS
# ============================================================


def incidents_page():

    section_start(
        "factory-incidents",
        "07",
        "Incidents & Alerts",
    )

    data, error = fetch_first(
        [
            "/incidents",
            "/incident",
        ]
    )

    if error:

        st.error(error)
        section_end()
        return

    rows = extract_list(data)

    if not rows:

        st.info("No incidents returned by the API.")

        section_end()
        return

    df = normalize_dataframe(rows)

    st.metric(
        "Total Incidents",
        len(df),
    )

    if "status" in df.columns:

        statuses = sorted(df["status"].dropna().astype(str).unique())

        selected = st.multiselect(
            "Filter by Status",
            statuses,
            default=statuses,
            key="incident_status_filter",
        )

        df = df[df["status"].astype(str).isin(selected)]

    display_table(df)

    section_end()


# ============================================================
# HELP
# ============================================================


def help_page():

    section_start(
        "factory-help",
        "08",
        "Help & Support",
    )

    render_html(
        """
        <div style="color: #334155; font-size: 1rem; line-height: 1.7; max-width: 860px; margin-bottom: 1.4rem;">
            FactoryOps provides real-time machine telemetry, predictive failure analytics, and automated maintenance scheduling to maximize plant uptime.
            Use the top navigation bar to monitor live equipment status, inspect sensor parameters, or review high-risk operational incidents.
            For platform access, system configuration, or immediate technical assistance, reach out to our operations lead below.
        </div>
        <div class="factory-support-card" style="background: #ffffff; border: 1px solid rgba(244, 43, 85, 0.18); border-radius: 16px; padding: 1.6rem 2rem; box-shadow: 0 10px 30px rgba(244, 43, 85, 0.08); margin-top: 1rem;">
            <div style="color: #f42b55; font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.5rem;">
                Platform Support & Inquiries
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 2rem; align-items: center; justify-content: space-between;">
                <div>
                    <div style="color: #0f172a; font-size: 1.4rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0.25rem;">
                        Kodali Sri Vatsavi 
                    </div>
                    <div style="color: #64748b; font-size: 0.9rem; font-weight: 500;">
                        Factory Operations & Platform Lead
                    </div>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; align-items: center;">
                    <a href="tel:+917729xxxxxx" style="display: inline-flex; align-items: center; gap: 0.5rem; color: #f42b55; text-decoration: none; background: #fff0f3; border: 1px solid rgba(244, 43, 85, 0.3); padding: 0.6rem 1.15rem; border-radius: 10px; font-size: 0.9rem; font-weight: 600; transition: all 0.2s ease;">
                        <span>📞</span> +91 7729xxxxxx
                    </a>
                    <a href="mailto:srivatsavikodali@gmail.com" style="display: inline-flex; align-items: center; gap: 0.5rem; color: #f42b55; text-decoration: none; background: #fff0f3; border: 1px solid rgba(244, 43, 85, 0.3); padding: 0.6rem 1.15rem; border-radius: 10px; font-size: 0.9rem; font-weight: 600; transition: all 0.2s ease;">
                        <span>✉️</span> srivatsavi@gmail.com
                    </a>
                </div>
            </div>
        </div>
        """
    )

    section_end()


# ============================================================
# MAIN APPLICATION
# ============================================================


def main():

    if not st.session_state.authenticated:
        login_page()
        return

    pages = [
        "Dashboard",
        "Machines",
        "Sensors",
        "Predictions",
        "Risk Analysis",
        "Maintenance",
        "Incidents",
        "Help",
    ]

    top_navigation(pages)

    # ========================================================
    # CONTINUOUS SCROLLING WORKSPACE
    # ========================================================

    dashboard_page()

    machines_page()

    sensors_page()

    predictions_page()

    risk_page()

    maintenance_page()

    incidents_page()

    help_page()

    # ========================================================
    # SCROLL SPY
    # ========================================================

    inject_scroll_spy()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
