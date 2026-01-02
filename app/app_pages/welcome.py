# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import logging
import os

logger = logging.getLogger(__name__)


def display_logo(logo_path: str):
    """Displays the logo in the sidebar or a placeholder if the logo is not found.

    Args:
        logo_path (str): The file path for the logo image.
    """
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        logger.info("Logo displayed.")
    else:
        st.sidebar.markdown("### Logo Placeholder")
        logger.warning("Logo not found, displaying placeholder.")

# Function to display main content
def display_main_content():
    """Displays the main welcome content on the page."""
    st.title("Risk Assessment of Safety-Related Digital Instrumentation and Control Systems 📄")
    st.markdown(
        """
        Welcome to the Digital I&C Risk Assessment Platform 👋

        This app allows you to perform the following analyses.

        **Features:**
        - **Preliminary Assessment**: which enables efficient estimation of software failure probability using stage-level evaluations of SDLC activities to support early design decisions.
        - **Comprehensive  Assessment**: which provides more detailed and refined failure probability estimates based on in-depth evaluations of development activities.
        - **Common Cause Analysis**: which identifies potential software-related CCFs through the determination of common cause component groups (CCCGs) based on software-specific coupling factors
        - **Software quality assessment survey**: offering a structured, survey-based approach to assess software reliability attributes;
        - **CCCG evaluation**: which assesses the vulnerability of each CCCG to CCF using both qualitative and quantitative measures.

        **Choose a page from the sidebar to begin!**
        """
    )
    logger.info("Displayed main welcome content.")

# Function to display sidebar content
def display_sidebar_content() -> None:
    """Displays headers and footer content in the sidebar."""
    st.sidebar.markdown(
        "<h2 style='text-align: center;'>Digital I&C Risk Assessment</h2>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h4 style='text-align: center;'>Software Common Cause Failure Analysis</h4>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="footer-text">
            © 2025 BAHAMAS
        </div>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Displayed sidebar content.")


def app():
    display_logo("../docs/pics/bahamas_structure.png")
    display_sidebar_content()
    display_main_content()
