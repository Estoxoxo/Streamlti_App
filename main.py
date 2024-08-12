import streamlit as st
from cloud_storage_page import cloud_storage
from BigQuery import BigQuery
from Jira import Jira
import pandas as pd
import os
from PIL import Image, ImageOps

# Definir primero la función show_home
def show_home():
    st.subheader("SBO CASES:")

    # Adding CSS styles
    st.markdown(
        """
        <style>
        .image-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            background-color: #e0e0e0;
            padding: 20px;
            border-radius: 10px;
        }
        .image-container img {
            width: 250px;
            height: 250px;
            object-fit: cover;
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #d3d3d3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Define the path to the images
    bigquery_image_path = '/Users/esteban.jimenez/Streamlti_App/Images/BigQuery_icon.png'
    cloudstorage_image_path = '/Users/esteban.jimenez/Streamlti_App/Images/GCP_ICON.png'
    
    # Load and resize images to ensure they have the same dimensions
    try:
        bigquery_image = Image.open(bigquery_image_path)
        cloudstorage_image = Image.open(cloudstorage_image_path)
        
        # Resize images to the same size using LANCZOS filter
        bigquery_image = ImageOps.fit(bigquery_image, (250, 250), Image.Resampling.LANCZOS)
        cloudstorage_image = ImageOps.fit(cloudstorage_image, (250, 250), Image.Resampling.LANCZOS)
   
    except FileNotFoundError:
        st.error("Error: No se encontraron las imágenes. Verifica las rutas y la ubicación de las imágenes.")
        return

    # Create a container for the images and buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(bigquery_image, use_column_width=False)
        if st.button("Ir a BigQuery Cases"):
            st.session_state.page = "BigQuery Cases"
    
    with col2:
        st.image(cloudstorage_image, use_column_width=False)
        if st.button("Ir a Cloud Storage Cases"):
            st.session_state.page = "Cloud Storage Cases"
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    st.title("Manejo de Archivos y Datos")
   
    # Inicialmente mostrar la pantalla principal
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    
    if st.session_state.page == "Home":
        show_home()
    elif st.session_state.page == "BigQuery Cases":
        BigQuery()
    elif st.session_state.page == "Cloud Storage Cases":
        cloud_storage()

# Ejecutar la función principal
if __name__ == "__main__":
    main()
