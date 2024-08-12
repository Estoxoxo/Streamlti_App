# -*- coding: utf-8 -*-

import streamlit as st

def case1():
    st.title("Caso 1")
    st.write("Has seleccionado: Caso 1")
    if "df_filtered" in st.session_state:
        st.write("DataFrame filtrado:")
        st.dataframe(st.session_state.df_filtered)

    file_name = st.text_input("Ingresa el nombre del archivo para guardar (sin extensión):", key="case1_filename_unique")
    file_format = st.selectbox("Selecciona el formato para guardar el archivo:", 
                                options=['csv', 'parquet', 'xlsx', 'json'], key="case1_format_unique")
    if file_name and file_format:
        if st.button("Guardar archivo", key="save_case1_button_unique"):
            save_dataframe(st.session_state.df_filtered, file_name, file_format)

def save_dataframe(df, file_name, file_format):
    file_path = file_name + f'.{file_format}'
    if file_format == 'csv':
        df.to_csv(file_path, index=False)
    elif file_format == 'parquet':
        df.to_parquet(file_path, index=False)
    elif file_format == 'xlsx':
        df.to_excel(file_path, index=False, engine='openpyxl')
    elif file_format == 'json':
        df.to_json(file_path, orient='records', lines=True)
    st.success(f"Archivo guardado en: {file_path}")
    return file_path
