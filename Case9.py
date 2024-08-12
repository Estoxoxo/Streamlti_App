#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:46:29 2024

@author: esteban.jimenez
"""

import streamlit as st
from utils import save_dataframe, add_special_characters


def case9():
    st.title("Caso 9")
    st.write("Has seleccionado: Caso 9")
    
    # Verificar si 'df_filtered' está en session_state y no es None
    if "df_filtered" in st.session_state and st.session_state.df_filtered is not None:
        
        # Guardar el DataFrame filtrado original si aún no se ha guardado
        if "df_original" not in st.session_state:
            st.session_state.df_original = st.session_state.df_filtered.copy()
        
        # Seleccionar las columnas donde agregar caracteres especiales
        selected_columns = st.multiselect(
            "Selecciona las columnas donde agregar caracteres especiales:", 
            options=st.session_state.df_filtered.columns.tolist(), 
            key="case9_columns_unique"
        )
        
        if selected_columns:
            # Agregar caracteres especiales a las columnas seleccionadas
            st.session_state.df_special = add_special_characters(st.session_state.df_filtered, selected_columns)
            st.write(f"DataFrame con caracteres especiales añadidos a las columnas seleccionadas:")
            st.dataframe(st.session_state.df_special)
        
        # Botón para restaurar el DataFrame original
        if st.button("Restaurar DataFrame original",key="restore_case9_button_unique"):
            st.session_state.df_filtered = st.session_state.df_original.copy()
            st.success("DataFrame restaurado al estado original.")
            st.dataframe(st.session_state.df_filtered)

        # Opciones para guardar el DataFrame actual (ya sea modificado o restaurado)
        file_name = st.text_input("Ingresa el nombre del archivo para guardar (sin extensión):", key="case9_filename_unique")
        file_format = st.selectbox("Selecciona el formato para guardar el archivo:", 
                                    options=['csv', 'parquet', 'xlsx', 'json'], key="case9_format_unique")

        if file_name and file_format:
            if st.button("Guardar archivo", key="save_case9_button_unique"):
                # Guardar el DataFrame con caracteres especiales si existe, de lo contrario guardar el original
                if "df_special" in st.session_state and st.session_state.df_special is not None:
                    save_dataframe(st.session_state.df_special, file_name, file_format)
                    st.success(f"Archivo modificado guardado como {file_name}.{file_format}")
                else:
                    save_dataframe(st.session_state.df_filtered, file_name, file_format)
                    st.success(f"Archivo original guardado como {file_name}.{file_format}")

    else:
        st.error("No se ha cargado o filtrado ningún DataFrame. Por favor, regresa a la página de inicio para cargar y filtrar los datos.")

# Llamar la función `case9`
case9()
