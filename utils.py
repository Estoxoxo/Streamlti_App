#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 19:00:51 2024

@author: esteban.jimenez
"""

import pandas as pd
import streamlit as st
from datetime import datetime

def uppercase_column_names(df):
    df.columns = [col.upper() for col in df.columns]
    return df



def add_timestamp_column(df, column_name='TIMESTAMP'):
    current_timestamp = datetime.now()
    df[column_name] = current_timestamp
    return df

def drop_columns(df, cols):
    df_remove = df.drop(columns=cols, errors='ignore')
    return df_remove

def add_special_characters(df, column_names):
    for column_name in column_names:
        df[column_name] = df[column_name].astype(str) + ' Ñ@#~'
    return df

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

def insert_new_value(df, column_names, value):
    for column_name in column_names:
        # Establecer los valores en nulos
        df[column_name] = df[column_name].apply(lambda x: None)
        # Reemplazar los valores nulos por el valor especificado
        df[column_name] = df[column_name].fillna(value)
    return df


def render_navbar():
    menu = st.selectbox("Selecciona una página", ["Home", "BigQuery", "CloudStorage"])
    st.session_state["menu"] = menu
    return menu
