# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import pandas as pd
import io


def app():
    st.title("Analysis")

    st.sidebar.selectbox("Results", ["UCA", "ODC"])

    # Session state initialization
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame({
            "Key": ["D1", "D2", "C", "O", "OC", "D1C", "D1O", "D1OC", "D2C", "D2O", "D2OC"],
            "Description": ["Diagnosis error (Diagnosis-1)", "Simple diagnosis error (Diagnosis-2)", "Omission error2", "Commission error", "Omission and Commission errors", "Diagnosis-1 and Omission", "Diagnosis-1 and Commission", "Diagnosis-1, Omission and Commission", "Diagnosis-2 and Omission", "Diagnosis-2 and Commission", "Diagnosis-2, Omission and Commission"],
            "mu": ["", "", "", "", "", "", "", "", "", "", ""],
            "sigma":["", "", "", "", "", "", "", "", "", "", ""]
        })

    # Function to add a new row
    def add_row():
        new_row = pd.DataFrame([{col: "" for col in st.session_state.df.columns}])
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

    # Function to add a new column
    def add_column():
        new_col_name = f"Column{len(st.session_state.df.columns) + 1}"
        st.session_state.df[new_col_name] = ""

    # Add buttons for adding rows and columns
    st.sidebar.button("Add Row", on_click=add_row)
    st.sidebar.button("Add Column", on_click=add_column)

    # Configure the grid options
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df)
    gb.configure_default_column(editable=True)
    grid_options = gb.build()

    # Display the table with editable cells
    grid_response = AgGrid(
        st.session_state.df,
        gridOptions=grid_options,
        editable=True,
        fit_columns_on_grid_load=True,
    )

    # Update the DataFrame in session state with the edited data
    st.session_state.df = grid_response['data']

    # Display the edited DataFrame
    st.write("Edited Table:")
    st.dataframe(st.session_state.df)

    # Optionally, allow the user to download the edited DataFrame as a CSV
    csv = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='edited_table.csv',
        mime='text/csv',
    )

    # Text area for user input
    csv_input = st.text_area("CSV Input", "Column1,Column2,Column3\nValue1,Value2,Value3")

    # Convert the CSV input to a DataFrame
    if csv_input:
        try:
            df = pd.read_csv(io.StringIO(csv_input))
            st.write("Here is your table:")
            st.dataframe(df)
        except Exception as e:
            st.write(f"Error: {e}")
