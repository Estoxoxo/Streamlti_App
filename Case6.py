#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:45:36 2024

@author: esteban.jimenez
"""

import streamlit as st
from utils import save_dataframe, drop_columns



def case6():
    st.title("Caso 6")
    st.write("Has seleccionado: Caso 6")
    
    # Verificar si 'df_filtered' está en session_state y no es None
    if "df_filtered" in st.session_state and st.session_state.df_filtered is not None:
        
        # Guardar el DataFrame filtrado original si aún no se ha guardado
        if "df_original" not in st.session_state:
            st.session_state.df_original = st.session_state.df_filtered.copy()
        
        # Mostrar la opción de borrar columnas
        selected_columns = st.multiselect("Selecciona las columnas a borrar:", 
                                          options=st.session_state.df_filtered.columns.tolist(), 
                                          key="case6_colnames_unique")
        
        if selected_columns:
            # Eliminar las columnas seleccionadas del DataFrame
            df_temp = st.session_state.df_filtered.copy()
            st.session_state.df_modified = drop_columns(df_temp, selected_columns)
            st.write("DataFrame después de eliminar las columnas:")
            st.dataframe(st.session_state.df_modified)

        # Botón para restaurar el DataFrame original
        if st.button("Restaurar DataFrame original",key="restore_case6_button_unique"):
            st.session_state.df_filtered = st.session_state.df_original.copy()
            st.success("DataFrame restaurado al estado original.")
            st.dataframe(st.session_state.df_filtered)

        # Guardar el DataFrame actual (ya sea modificado o restaurado)
        file_name = st.text_input("Ingresa el nombre del archivo para guardar (sin extensión):", key="case6_filename_unique")
        file_format = st.selectbox("Selecciona el formato para guardar el archivo:", 
                                    options=['csv', 'parquet', 'xlsx', 'json'], key="case6_format_unique")

        if file_name and file_format:
            if st.button("Guardar archivo", key="save_case6_button_unique"):
                # Guardar el DataFrame modificado si existe, de lo contrario guardar el original
                if "df_modified" in st.session_state and st.session_state.df_modified is not None:
                    save_dataframe(st.session_state.df_modified, file_name, file_format)
                    st.success(f"Archivo modificado guardado como {file_name}.{file_format}")
                else:
                    save_dataframe(st.session_state.df_filtered, file_name, file_format)
                    st.success(f"Archivo original guardado como {file_name}.{file_format}")

    else:
        st.error("No se ha cargado o filtrado ningún DataFrame. Por favor, regresa a la página de inicio para cargar y filtrar los datos.")

# Llamar la función `case6`
case6()
