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
        #TODO: Generalize both tabs to consume from the same routine
        analysis_type = st.segmented_control("Select analysis type", options=['Line Chart', "Histogram", "Boxplot"], default="Line Chart", key="tab1_analysis_type")
        analysis_level = st.radio("Select analysis level", options=["Entire Fleet", "By Equipment"], horizontal=True, key="tab1_analysis_level")
        component = st.selectbox("Select a component", options=file_1['comp_desc'].drop_duplicates() if 'comp_desc' in file_1.columns else [], key="tab1_selectbox_component")
        file = file_1[file_1['comp_desc'] == component].sort_values(by=['sample_dt'])        
        slider = st.slider('Select a threshold limit', min_value=0.5, max_value=1.0, value=0.95, step=0.05, key="tab1_slider_threshold")
        util.handle_tab(file = file, file_basename=file_1_basename, col_target=col_target, analysis_type=analysis_type, analysis_level=analysis_level, component=component, threshold=slider)


    with tab_file_2:
        #TODO: Generalize both tabs to consume from the same routine
        analysis_type = st.segmented_control("Select analysis type", options=['Line Chart', "Histogram", "Boxplot"], default="Line Chart", key="tab2_analysis_type")
        analysis_level = st.radio("Select analysis level", options=["Entire Fleet", "By Equipment"], horizontal=True, key="tab2_analysis_level")
        component = st.selectbox("Select a component", options=file_2['comp_desc'].drop_duplicates() if 'comp_desc' in file_2.columns else [], key="tab2_selectbox_component")
        file = file_2[file_2['comp_desc'] == component].sort_values(by=['sample_dt'])        
        slider = st.slider('Select a threshold limit', min_value=0.5, max_value=1.0, value=0.95, step=0.05, key="tab2_slider_threshold")
        util.handle_tab(file = file, file_basename=file_2_basename, col_target=col_target, analysis_type=analysis_type, analysis_level=analysis_level, component=component, threshold=slider)

    with tab_comparison:
        #TODO: Generalize this
        analysis_type = st.segmented_control("Select analysis type", options=['Line Chart', "Histogram", "Boxplot"], default="Line Chart", key="tab3_analysis_type")
        component = st.selectbox("Select a component", options=file_1['comp_desc'].drop_duplicates() if 'comp_desc' in file_1.columns else [], key="tab3_selectbox_component")
        file = pd.concat([file_1, file_2], ignore_index=True)
        file = file[file['comp_desc'] == component].sort_values(by=['sample_dt'])
        slider = st.slider('Select a threshold limit', min_value=0.5, max_value=1.0, value=0.95, step=0.05, key="tab3_slider_threshold")
        util.handle_comparison(file = file, col_target=col_target, analysis_type=analysis_type, component=component, threshold=slider)
