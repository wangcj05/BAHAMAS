# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import pandas as pd
import io
import os, sys

# Bahamas Module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from bahamas.utils import SDLC_stages, UCA_types
from bahamas.software_total_failure_probability_bbn import BBN


# streamlit and extra
# create badge for github etc.
from streamlit_extras.badges import badge
# container always at the bottom
from streamlit_extras.bottom_container import bottom
# chart container allows to explore data and download data
from streamlit_extras.chart_container import chart_container
# customize the running widget
from streamlit_extras.customize_running import center_running
# allow users to explore dataframe data: ranges, variables etc.
from streamlit_extras.dataframe_explorer import dataframe_explorer
# Good way to design multi-row, multi-column
from streamlit_extras.grid import grid
# similar to grid
from streamlit_extras.row import row
# similar to badge
from streamlit_extras.mention import mention
# This can be used to report calculation results
from streamlit_extras.metric_cards import style_metric_cards
#
from streamlit_extras.vertical_slider import vertical_slider


# Data:

workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', '..', 'data', 'Defect_Data.xlsx')
# task_data = os.path.join(workdir, '..', '..', 'data', 'Task_List.xlsx')


# Functions for configure
def configure_sidebar() -> None:
    """
    Setup and display the sidebar elements.

    This function configures the sidebar of the Streamlit application,
    including the form for user inputs and the resources section.
    """
    with st.sidebar:
        with st.form("my_form"):
            st.info("**Assessment! Start here ↓**", icon="👋🏾")
            # with st.expander(":orange[**Refine Calculation**]"):
            # Advanced Settings (for the curious minds!)
            defects = None
            mode = None
            tasks = st.file_uploader('Upload your data', type=['xlsx'])
            defects = st.file_uploader('Upload defect data (optional)', type=['xlsx'])
            # mode = st.selectbox("Calculation mode", ('Stochastic', 'Deterministic'))
            num_samples = st.number_input("Number of samples", value=10000)
            plot_failure = st.checkbox('visualize')

            # The Big Red "Submit" Button!
            submitted = st.form_submit_button(
                "Calculate", type="primary", use_container_width=True)
        return submitted, mode, num_samples, plot_failure, tasks, defects


def app():
    # configure the sidebar
    submitted, mode, num_samples, plot_failure, tasks, defects = configure_sidebar()

    st.set_page_config(page_title="BAHAMAS",
                    # page_icon=":bridge_at_night:",
                    page_icon="../docs/pics/bahamas_structure.png",
                    layout="wide",
                    initial_sidebar_state="auto")
    # st.logo("./docs/pics/bahamas_structure.png")
    st.image("../docs/pics/bahamas_structure.png", width=200)

    st.header("""BAHAMAS: Software Reliability Assessment""")

    if submitted:
        output = {}
        style = {}
        if defects is not None:
            software_BBN = BBN(defects, tasks, num_samples)
        else:
            software_BBN = BBN(defect_data, tasks, num_samples)
        software_BBN.calculate()
        total_failure_mean, total_failure_sigma, _ = software_BBN.get_total_failure_probability()

        output['Total Failure Prob.'] = [total_failure_mean, total_failure_sigma]
        style['Total Failure Prob.'] = "{:.2e}"
        # st.write('Software total failure:', total_failure_mean, 'with std:', total_failure_sigma)
        for uca in UCA_types:
            mean, sigma, _ = software_BBN.get_uca(uca)
            output[uca] = [mean, sigma]
            style[uca] = "{:.2e}"

        df = pd.DataFrame(output, index=['mean', 'std'])
        styled_df = df.style.format(style)
        st.subheader("""Calculation Results""")
        st.info("**Assessment Result ↓**", icon="👋🏾")

        st.dataframe(styled_df)
        # visualize data
        if plot_failure:
            fig = software_BBN.plot(save=False, show=False)
            if isinstance(fig, list):
                for f in fig:
                    st.plotly_chart(f)

    else:
        pass



    with bottom():
        st.markdown("#### Bayesian and Human Reliability Analysis-Aided Method for the Reliability Analysis of Software (BAHAMAS)")
        st.markdown('''For help or feedback, contact congjian.wang@inl.gov.
                For more options and information, check out the
                [GitHub repository](https://github.inl.gov/congjian-wang/BAHAMAS) or
                [Report](https://lwrs.inl.gov/content/uploads/11/2024/11/2448420.pdf)
                ''')

