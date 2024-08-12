#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:45:47 2024

@author: esteban.jimenez
"""

import streamlit as st
from utils import save_dataframe

def case7():
    st.title("Caso 7")
    st.write("Has seleccionado: Caso 7")
    if "df_load" in st.session_state:
        st.write("Copiando DataFrame:")
        st.dataframe(st.session_state.df_filtered )

        file_name = st.text_input("Ingresa el nombre del archivo para guardar la copia del DataFrame (sin extensión):", key="case7_filename_unique")
        file_format = st.selectbox("Selecciona el formato para guardar el archivo:", 
                                    options=['csv', 'parquet', 'xlsx', 'json'], key="case7_format_unique")
        if file_name and file_format:
            if st.button("Guardar archivo", key="save_case7_button_unique"):
                save_dataframe(st.session_state.df_filtered , file_name, file_format)
                st.success("Copia del DataFrame guardada.")


