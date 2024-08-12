#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:44:23 2024

@author: esteban.jimenez
"""

import streamlit as st
from utils import save_dataframe


def case2():
    st.title("Caso 2")
    st.write("Has seleccionado: Caso 2")
    
    # Verificar si 'df_filtered' está en session_state y no es None
    if "df_filtered" in st.session_state and st.session_state.df_filtered is not None:
        
        # Guardar el DataFrame filtrado original si aún no se ha guardado
        if "df_original" not in st.session_state:
            st.session_state.df_original = st.session_state.df_filtered.copy()
        
        st.write("DataFrame original:")
        st.dataframe(st.session_state.df_filtered)
        
        # Botón para restaurar el DataFrame original
        if st.button("Restaurar DataFrame original",key="restore_case2_button_unique"):
            st.session_state.df_filtered = st.session_state.df_original.copy()
            st.success("DataFrame restaurado al estado original.")
            st.dataframe(st.session_state.df_filtered)

        # Opciones para guardar el DataFrame actual (ya sea modificado o restaurado)
        file_name = st.text_input("Ingresa el nombre del archivo para guardar (sin extensión):", key="case2_filename_unique")
        file_format = st.selectbox("Selecciona el formato para guardar el archivo:", 
                                    options=['csv', 'parquet', 'xlsx', 'json'], key="case2_format_unique")

        if file_name and file_format:
            if st.button("Guardar archivo", key="save_case2_button_unique"):
                save_dataframe(st.session_state.df_filtered, file_name, file_format)
                st.success(f"Archivo guardado como {file_name}.{file_format}")

    else:
        st.error("No se ha cargado o filtrado ningún DataFrame. Por favor, regresa a la página de inicio para cargar y filtrar los datos.")

# Llamar la función `case2`
case2()
