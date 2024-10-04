import streamlit as st
import pandas as pd
from datetime import datetime
import re
from io import StringIO, BytesIO
import time




# Funciones para extraer prefijo, sufijo y fecha
def extraer_prefijo(nombre_archivo):
    return re.split(r'[-_]', nombre_archivo)[0]

def extraer_sufijo(nombre_archivo):
    partes = re.split(r'[-_]', nombre_archivo)
    if len(partes) > 2:
        return partes[-2]
    else:
        st.error("El archivo no tiene suficiente información para extraer el sufijo.")
        return None

def extraer_fecha(nombre_archivo):
    match = re.search(r'(\d{2}-\d{2}-\d{4})|(\d{8})', nombre_archivo)
    if match:
        return match.group(0)
    else:
        st.error(f"El archivo '{nombre_archivo}' no contiene una fecha válida.")
        return None

# Función para validar archivo
def validar_archivo_nombre(archivo):
    nombre_archivo = archivo.name
    prefijo = extraer_prefijo(nombre_archivo)
    sufijo = extraer_sufijo(nombre_archivo)
    fecha = extraer_fecha(nombre_archivo)
    
    if prefijo and sufijo and fecha:
        st.success(f"Archivo cargado correctamente.\nPrefijo: {prefijo}\nSufijo: {sufijo}\nFecha: {fecha}")
    else:
        st.error(f"El archivo '{nombre_archivo}' no cumple con el formato esperado.")
    
    return prefijo, sufijo, fecha

# Función para mostrar el número de registros y columnas
def mostrar_info_dataframe(df, nombre_archivo):
    num_filas = df.shape[0]
    num_columnas = df.shape[1]
    st.write(f"Archivo: {nombre_archivo} | Registros: {num_filas} | Columnas: {num_columnas}")
    return num_filas, num_columnas

# Inicialización del estado del DataFrame
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'final_df' not in st.session_state:
    st.session_state.final_df = None
if 'df_seleccionado' not in st.session_state:
    st.session_state.df_seleccionado = None


if 'guardar_csv' not in st.session_state:
    st.session_state.guardar_csv = False
if 'guardar_excel' not in st.session_state:
    st.session_state.guardar_excel = False
if 'guardar_json' not in st.session_state:
    st.session_state.guardar_json = False
if 'guardar_parquet' not in st.session_state:
    st.session_state.guardar_parquet = False
    
if 'ingresar_mayusculas' not in st.session_state:
    st.session_state.ingresar_mayusculas = False
if 'datos_parceados' not in st.session_state:
    st.session_state.datos_parceados = False
if 'valores_nulos' not in st.session_state:
    st.session_state.valores_nulos = False
if 'caracteres_especiales' not in st.session_state:
    st.session_state.caracteres_especiales = False
if 'borrar_columna' not in st.session_state:
    st.session_state.borrar_columna = False
if 'validar_esquema' not in st.session_state:
    st.session_state.validar_esquema = False
if 'cantidad_datos' not in st.session_state:
    st.session_state.cantidad_datos = False
if 'validacion_data' not in st.session_state:
    st.session_state.validacion_data = False
    
    
if 'montos_negativos' not in st.session_state:
    st.session_state.montos_negativos = False
    
if 'montos_en_cero' not in st.session_state:
    st.session_state.montos_en_cero = False
    
if 'fecha_usuario' not in st.session_state:
    st.session_state.fecha_usuario = False

# Configuración de la página de Streamlit
st.set_page_config(page_title="TestDataLab", layout="wide")

# Subida de archivos y creación de DataFrame
st.header("TestDataLab")
archivos_subidos = st.file_uploader("Sube uno o varios archivos de datos (CSV, Parquet, JSON, Excel):", type=["csv", "parquet", "json", "xlsx"], accept_multiple_files=True)

# Validación y carga de archivos subidos
if archivos_subidos:
    formatos_aceptados = ['csv', 'parquet', 'json', 'xlsx']
    nombres_archivos = [archivo.name for archivo in archivos_subidos]
    
    # Mostrar la lista de archivos subidos y permitir seleccionar uno para trabajar
    archivo_seleccionado = st.selectbox("Selecciona el archivo con el que deseas trabajar", nombres_archivos)
    
    if archivo_seleccionado:
        archivo = next(archivo for archivo in archivos_subidos if archivo.name == archivo_seleccionado)
        
        prefijo, sufijo, fecha = validar_archivo_nombre(archivo)
        file_type = archivo.name.split('.')[-1]

        # Cargar el archivo seleccionado en un DataFrame
        if file_type == 'csv':
            st.session_state.original_df = pd.read_csv(archivo, low_memory=False)
        elif file_type == 'xlsx':
            st.session_state.original_df = pd.read_excel(archivo)
        elif file_type == 'json':
            st.session_state.original_df = pd.read_json(archivo)
        elif file_type == 'parquet':
            st.session_state.original_df = pd.read_parquet(archivo)

        # Inicializar el DataFrame final si aún no está definido
        if st.session_state.final_df is None or st.session_state.final_df.empty:
            st.session_state.final_df = st.session_state.original_df.copy()
            st.session_state.final_df2 = st.session_state.original_df.copy()
        # Mostrar información del DataFrame
            with st.spinner('Se esta Cargando el Archivo'):
             time.sleep(5)
             mostrar_info_dataframe(st.session_state.original_df, archivo_seleccionado)
             st.success('Puedes ver el archivo en Tabla Original')
             with st.expander("Tabla Orginal"):
              st.dataframe(st.session_state.final_df2)
            
        #st.dataframe(st.session_state.final_df)

# Sidebar con opciones de transformación y validaciones de archivo
with st.sidebar:
    st.title("Casos de prueba")
    
    st.header("Modificación de Datos:")
    uppercase_option = st.checkbox("Ingresar Mayúsculas")
    parse_data_option = st.checkbox("Datos Parceados",value=st.session_state.datos_parceados)
    null_values_option = st.checkbox("Valores Nulos")
    special_characters_option = st.checkbox("Agregar Caracteres especiales")
    montos_negativos = st.checkbox("Procesar Montos Negativos", value=st.session_state.montos_negativos)
    montos_en_cero = st.checkbox("Procesar Montos en Cero", value=st.session_state.montos_en_cero)
    fecha_usuario = st.checkbox("Ingresa una Fecha", value=st.session_state.fecha_usuario)
    
    st.header("Eliminación de Datos:")
    delete_column_option = st.checkbox("Borrar columna")
    
    st.header("Validación de Esquema:")
    validate_schema_option = st.checkbox("Validar el Esquema")
    data_quantity_option = st.checkbox("Cantidad de Datos")
    data_validation_option = st.checkbox("Validación de la Data")
    Nombre_Columnas = st.checkbox("Nombre de las Columnas")
    Orden_Columnas = st.checkbox("Orden de las Columnas")
    Tipo_Dato =  st.checkbox("Validación tipo de Datos en la Tabla")
    Valores_Permitidos =  st.checkbox("Valores Permitidos (Nulos, Caracteres especiales, Duplicados)") 
    
    st.title("Opciones de Guardado")
    guardar_csv = st.checkbox("Guardar como CSV")
    guardar_excel = st.checkbox("Guardar como Excel")
    guardar_json = st.checkbox("Guardar como JSON")
    guardar_parquet = st.checkbox("Guardar como Parquet")
    nombre_archivo = st.text_input("Nombre del archivo:", value="datos_modificados")
    



# Funciones de transformación


def procesar_montos_negativos(df, column_name):
    df[column_name] = df[column_name].apply(lambda x: -abs(x))
    return df.head(10)

def procesar_montos_en_cero(df, column_name):
    df[column_name] = 0
    return df.head(10)

def aplicar_fecha_usuario(df, column_name, fecha):
    df[column_name] = fecha
    return df.head(10)

def add_timestamp_column(df, column_name='TIMESTAMP'):
    df[column_name] = datetime.now()
    return df.head(10)

def uppercase_column_names(df):
    df.columns = [col.upper() for col in df.columns]
    return df.head(10)

def valores_nulos(df, column_name):
    if column_name not in df.columns:
        st.error(f"La columna '{column_name}' no existe en el DataFrame.")
        return df
    new_value = ' '
    df[column_name] = new_value
    return df.head(10)

def agregar_caracteres_especiales(df, column_name):
    if column_name not in df.columns:
        st.error(f"La columna '{column_name}' no existe en el DataFrame.")
        return df
    df[column_name] = df[column_name].astype(str) + " @!"
    return df.head(10)

def borrar_columna(df, column_name):
    if column_name not in df.columns:
        st.error(f"La columna '{column_name}' no existe en el DataFrame.")
        return df
    X = df.drop(columns=[column_name],inplace=True)
    return X

# Aplicación de transformaciones inmediatas
if st.session_state.df_seleccionado is not None:
    
    # Procesar Mayúsculas
    if uppercase_option:
        temp_df = uppercase_column_names(st.session_state.df_seleccionado)
        st.write("Vista previa de cambio: Mayúsculas")
        st.dataframe(temp_df)
        if st.button("Mantener Cambios (Mayúsculas)"):
            st.session_state.final_df = temp_df.copy()

    # Procesar Datos Parceados
    if parse_data_option:
        temp_df = add_timestamp_column(st.session_state.df_seleccionado)
        st.write("Vista previa de cambio: Marca de Tiempo")
        temp_df
        if st.button("Mantener Cambios (Marca de Tiempo)"):
           st.session_state.final_df = temp_df

    # Procesar Valores Nulos
    if null_values_option:
        columna_nulos = st.text_input("Escribe el nombre de la columna para reemplazar valores nulos:")
        if columna_nulos:
            temp_df = valores_nulos(st.session_state.df_seleccionado, columna_nulos)
            st.write(f"Vista previa de cambio: Valores Nulos en {columna_nulos}")
            st.dataframe(temp_df)
            if st.button("Mantener Cambios (Valores Nulos)"):
                st.session_state.final_df = temp_df.copy()

    # Procesar Caracteres Especiales
    if special_characters_option:
        columna_caracteres = st.text_input("Escribe el nombre de la columna para agregar caracteres especiales:")
        if columna_caracteres:
            temp_df = agregar_caracteres_especiales(st.session_state.df_seleccionado, columna_caracteres)
            st.write(f"Vista previa de cambio: Caracteres Especiales en {columna_caracteres}")
            st.dataframe(temp_df)
            if st.button("Mantener Cambios (Caracteres Especiales)"):
                 st.session_state.final_df = temp_df.copy()

    # Borrar columna
    if delete_column_option:
        columna_borrar = st.text_input("Escribe el nombre de la columna para borrar:")
        if columna_borrar:
            temp_df = borrar_columna(st.session_state.df_seleccionado, columna_borrar)
            st.write(f"Vista previa de cambio: Borrar columna {columna_borrar}")
            st.dataframe(temp_df)
            if st.button("Mantener Cambios (Borrar columna)"): 
                st.session_state.final_df = temp_df.copy()
    
    
    if montos_negativos:
        datosnegativos = st.text_input("Escribe el nombre de la columna para ingresar datos negativos:")
        if datosnegativos:
            temp_df = procesar_montos_negativos(st.session_state.df_seleccionado, datosnegativos)
            st.write(f"Vista previa de cambio: Datos Negativos {datosnegativos}")
            st.dataframe(temp_df)
            if st.button("Mantener Cambios (datosnegativos )"): 
                st.session_state.final_df = temp_df.copy()
                
    
    
    if montos_en_cero:
        montosencero = st.text_input("Escribe el nombre de la columna para ingresar datos negativos:")
        if montosencero :
            temp_df = procesar_montos_en_cero(st.session_state.df_seleccionado, montosencero )
            st.write(f"Vista previa de cambio: Datos Negativos {montosencero}")
            st.dataframe(temp_df)
            if st.button("Mantener Cambios (montosencero)"): 
                st.session_state.final_df = temp_df.copy()
    
    
    
    if fecha_usuario:
        fechausuario = st.text_input("Escribe el nombre de la columna para ingresar datos negativos:")
        fecha = st.date_input("Selecciona una Fecha")
        if fechausuario :
            temp_df = aplicar_fecha_usuario(st.session_state.df_seleccionado, fechausuario,fecha )
            st.write(f"Vista previa de cambio: Datos Negativos {fechausuario}")
            st.dataframe(temp_df)
            if st.button("Mantener Cambios (fechausuario)"): 
                st.session_state.final_df = temp_df.copy()
    
    
   
# Si el usuario selecciona columnas, las almacenamos en session_state
with st.expander("Seleccionar columnas"):
 
 lista_columnas = st.text_input("Introduce una lista de columnas separadas por comas (ejemplo: columna1, columna2, columna3):")
 if lista_columnas:
     columnas = [col.strip() for col in lista_columnas.split(',')]
     columnas_validas = [col for col in columnas if col in st.session_state.final_df.columns]
     columnas_invalidas = [col for col in columnas if col not in st.session_state.final_df.columns]

     if columnas_invalidas:
         st.error(f"Las siguientes columnas no existen en el DataFrame: {', '.join(columnas_invalidas)}")
    
     if columnas_validas:
         df_seleccionado = st.session_state.final_df[columnas_validas]
         st.write(f"Columnas seleccionadas: {', '.join(columnas_validas)}")
         st.session_state.df_seleccionado = df_seleccionado  # Guardar en session_state
         st.session_state.lista_columnas = " " 
         st.session_state.final_df2 = False
        
        

# Mostrar DataFrame final si está disponible
if st.session_state.df_seleccionado is not None:
    st.write("### DataFrame final después de la selección:")
    st.dataframe(st.session_state.df_seleccionado)
    
    if guardar_excel:
        excel = BytesIO()
        with pd.ExcelWriter(excel, engine='xlsxwriter') as writer:
            st.session_state.df_seleccionado.to_excel(writer, index=False)
            excel.seek(0)
            st.download_button("Descargar Excel", excel.getvalue(), f"{nombre_archivo}.xlsx")
            
    if guardar_csv:
        csv = StringIO()
        st.session_state.df_seleccionado.to_csv(csv, index=False)
        csv.seek(0)
        st.download_button("Descargar CSV", csv.getvalue(), f"{nombre_archivo}.csv")

    
if st.button("Finalizar y Limpiar"):
        st.session_state.final_df = None
        st.session_state.original_df = None
        st.session_state.df_seleccionado = None
        st.session_state.ingresar_mayusculas = False
        st.session_state.datos_parceados = False
        st.session_state.valores_nulos = False
        st.session_state.caracteres_especiales = False
        st.session_state.borrar_columna = False
        st.session_state.validar_esquema = False
        st.session_state.cantidad_datos = False
        st.session_state.validacion_data = False
        st.session_state.guardar_csv = False
        st.session_state.guardar_excel = False
        st.session_state.guardar_json = False
        st.session_state.guardar_parquet = False
        st.session_state.lista_columnas = " "  # Restablecer el filtro de columnas
        st.success("Sesión finalizada.")
        st.rerun()
