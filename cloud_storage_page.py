import pandas as pd
import streamlit as st
import os
from datetime import datetime
from PIL import ImageGrab
import streamlit as st
from utils import *
from Case1 import case1
from Case2 import case2
from Case3 import case3
from Case4 import case4
from Case5 import case5
from Case6 import case6
from Case7 import case7
from Case8 import case8
from Case9 import case9
from Case10 import case10
from Case11 import case11
from Case12 import case12
from Case13 import case13
from utils import *

# Importa los demás casos según sea necesario


# Función para manejar el refresco de la aplicación
def finalize_app():
    # Limpiar todos los elementos en session_state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Limpiar caché de Streamlit
    st.cache_data.clear()
    st.cache_resource.clear()

def cloud_storage():
    
     # Llamada a la página de CloudStorage
    # Configuración inicial
    #st.set_page_config(page_title="DataFrame Operations", layout="wide")

    # Sistema de navegación
    menu = st.sidebar.selectbox("Selecciona una opción", ["Inicio", "Caso 1", "Caso 2", "Caso 3", "Caso 4", "Caso 5", "Caso 6", "Caso 7", "Caso 8", "Caso 9", "Caso 10", "Caso 11", "Caso 12"])
    
    if st.sidebar.button("Finalizar Aplicación"):
        finalize_app()

    # Página de inicio: Cargar archivo y filtrar columnas
    if menu == "Inicio":
        st.title("Bienvenido a la aplicación de operaciones con DataFrames")

        st.session_state.file_uploader = st.file_uploader("Sube un archivo de datos (CSV, Parquet, JSON, Excel):")

        if st.session_state.file_uploader is not None:
            st.session_state.df_load = load_file_to_dataframe(st.session_state.file_uploader)
            
            if st.session_state.df_load is not None:
                st.write("DataFrame cargado:")
                st.dataframe(st.session_state.df_load)

                st.text_area("Ingresa los nombres de las columnas a conservar, separadas por comas:", key="column_list_input")
                if st.session_state.column_list_input:
                    selected_columns = [col.strip() for col in st.session_state.column_list_input.split(",")]
                    st.session_state.df_filtered = st.session_state.df_load[selected_columns]
                    st.write("DataFrame después de filtrar columnas:")
                    st.dataframe(st.session_state.df_filtered)

    # Navegación a los casos
    elif menu == "Caso 1":
        case1()

    elif menu == "Caso 2":
        case2()

    elif menu == "Caso 3":
        case3()
    
    elif menu == "Caso 4":
        case4()
    
    elif menu == "Caso 5":
        case5()
    
    elif menu == "Caso 6":
        case6()
    
    
    elif menu == "Caso 7":
        case7()

    elif menu == "Caso 8":
        case8()
        
    elif menu == "Caso 9":
       case9()
       
    elif menu == "Caso 10":
        case10()
    
    elif menu == "Caso 11":
        case11()
    
    elif menu == "Caso 12":
        case12()
    
    elif menu == "Caso 13":
        case13()
    # Continúa con el resto de los casos
    # ...

# Función para cargar archivo
def load_file_to_dataframe(file):
    extension = file.name.split('.')[-1].lower()
    if extension == 'csv':
        return pd.read_csv(file)
    elif extension == 'parquet':
        return pd.read_parquet(file)
    elif extension == 'xlsx' or extension == 'xls':
        return pd.read_excel(file)
    elif extension == 'json':
        return pd.read_json(file)
    else:
        st.error("Formato de archivo no soportado.")
        return None

# Llamada a la función principal
if __name__ == "__main__":
    cloud_storage()
