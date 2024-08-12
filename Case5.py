import streamlit as st
from utils import save_dataframe, insert_new_value



def case5():
    st.title("Caso 5")
    st.write("Has seleccionado: Caso 5")
    
    # Verificar si 'df_filtered' está en session_state y no es None
    if "df_filtered" in st.session_state and st.session_state.df_filtered is not None:
        
        # Guardar el DataFrame filtrado original si aún no se ha guardado
        if "df_original" not in st.session_state:
            st.session_state.df_original = st.session_state.df_filtered.copy()
        
        # Seleccionar las columnas donde se eliminarán los valores existentes y se reemplazarán por espacios en blanco
        selected_columns = st.multiselect(
            "Selecciona las columnas donde eliminar valores y dejarlas en blanco:", 
            options=st.session_state.df_filtered.columns.tolist(), 
            key="case5_columns_unique"
        )
        
        if selected_columns:
            # Eliminar valores existentes y reemplazarlos por espacios en blanco en las columnas seleccionadas
            st.session_state.df_new = insert_new_value(st.session_state.df_filtered, selected_columns, '')
            st.write(f"DataFrame con columnas seleccionadas modificadas:")
            st.dataframe(st.session_state.df_new)
        
        # Botón para restaurar el DataFrame original
        if st.button("Restaurar DataFrame original",key="restore_case5_button_unique"):
            st.session_state.df_filtered = st.session_state.df_original.copy()
            st.success("DataFrame restaurado al estado original.")
            st.dataframe(st.session_state.df_filtered)

        # Opciones para guardar el DataFrame actual (ya sea modificado o restaurado)
        file_name = st.text_input("Ingresa el nombre del archivo para guardar (sin extensión):", key="case5_filename_unique")
        file_format = st.selectbox("Selecciona el formato para guardar el archivo:", 
                                    options=['csv', 'parquet', 'xlsx', 'json'], key="case5_format_unique")

        if file_name and file_format:
            if st.button("Guardar archivo", key="save_case5_button_unique"):
                # Guardar el DataFrame modificado si existe, de lo contrario guardar el original
                if "df_new" in st.session_state and st.session_state.df_new is not None:
                    save_dataframe(st.session_state.df_new, file_name, file_format)
                    st.success(f"Archivo modificado guardado como {file_name}.{file_format}")
                else:
                    save_dataframe(st.session_state.df_filtered, file_name, file_format)
                    st.success(f"Archivo original guardado como {file_name}.{file_format}")

    else:
        st.error("No se ha cargado o filtrado ningún DataFrame. Por favor, regresa a la página de inicio para cargar y filtrar los datos.")

# Llamar la función `case5`
case5()
