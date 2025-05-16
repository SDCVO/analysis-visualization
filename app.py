# app.py

import streamlit as st
import pandas as pd
import util


st.set_page_config(page_title="Analysis Dashboard", page_icon=":smiley:", layout="centered")
st.title('Anaysis Dashboard')

col_1, col_2 = st.columns(2)

file_1 = col_1.file_uploader("Upload File 1", type=["csv"])
file_2 = col_2.file_uploader("Upload File 2", type=["csv"])

if file_1 or file_2:
    file_1_basename = file_1.name.split('.')[0] if file_1 else None
    file_2_basename = file_2.name.split('.')[0] if file_2 else None
    
    file_1 = pd.read_csv(file_1) if file_1 else None
    file_2 = pd.read_csv(file_2) if file_2 else None

    file_1_columns = list(file_1.columns) if file_1 is not None else []
    file_2_columns = list(file_2.columns) if file_2 is not None else []
    total_columns = list(set(file_1_columns + file_2_columns))

    #TODO: Generalize this
    col_identifiers_default = ['equip_number', 'fleet', 'mine', 'sample_dt', 'comp_desc']
    col_target_default = list(set(total_columns) - set(col_identifiers_default)) if col_identifiers_default else total_columns
    
    st.subheader('Classify columns')
    col_identifiers = st.multiselect('Select identification columns', options=total_columns, default=col_identifiers_default)
    col_target = st.multiselect('Select target columns', options=list(set(total_columns) - set(col_identifiers)), default=list(set(total_columns) - set(col_identifiers)))

    
    
    tab_file_1, tab_file_2, tab_comparison = st.tabs([f"{file_1_basename}", f"{file_2_basename}", "Comparison"])
    
    with tab_file_1:
        #TODO: Generalize this
        analysis_type = st.segmented_control("Select analysis type", options=['Line Chart', "Histogram", "Boxplot"], default="Line Chart")
        analysis_level = st.radio("Select analysis level", options=["Entire Fleet", "By Equipment"], horizontal=True)
        component = st.selectbox("Select a component", options=file_1['comp_desc'].drop_duplicates() if 'comp_desc' in file_1.columns else [])
        file = file_1[file_1['comp_desc'] == component]
        file = file.sort_values(by='sample_dt', ascending=False)
        util.handle_tab(file = file, col_target=col_target, analysis_type=analysis_type, analysis_level=analysis_level, component=component)

    with tab_file_2:
        #TODO: Generalize this
        analysis_type = st.segmented_control("Select analysis type", options=['Line Chart', "Histogram", "Boxplot"], default="Line Chart", key='unique_dadas')
        analysis_level = st.radio("Select analysis level", options=["Entire Fleet", "By Equipment"], horizontal=True, key='unique_radio')
        component = st.selectbox("Select a component", options=file_2['comp_desc'].drop_duplicates() if 'comp_desc' in file_2.columns else [], key='unique_select')
        file = file_2[file_2['comp_desc'] == component]
        file = file.sort_values(by='sample_dt', ascending=False)
        util.handle_tab(file = file, col_target=col_target, analysis_type=analysis_type, analysis_level=analysis_level, component=component)

    with tab_comparison:
        #TODO: Create comparissons
        pass
        