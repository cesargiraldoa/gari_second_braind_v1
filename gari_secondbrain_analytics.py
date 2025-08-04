# gari_secondbrain_analytics.py

import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import plotly.express as px
import streamlit as st

# 🔁 Usa la función de conexión segura a SQL desde tu módulo actual
from db_connection import consultar_ventas  # Asegúrate que existe y se importa correctamente

def calcular_edad(fecha):
    if pd.isnull(fecha):
        return None
    return (datetime.now().date() - fecha.date()).days // 365

def cargar_datos_reales():
    try:
        df = consultar_ventas("[Prestaciones_Temporal]", 10000)
        df['FechaNacimiento'] = pd.to_datetime(df['FechaNacimiento'], errors='coerce')
        df['Edad'] = df['FechaNacimiento'].apply(calcular_edad)
        return df
    except Exception as e:
        st.error(f"⚠️ Error al cargar datos desde SQL Server: {e}")
        return pd.DataFrame()

def clustering_prestaciones(df):
    st.subheader("🔍 Clustering de pacientes (Edad + Valor + Categóricos)")

    if df.empty:
        st.warning("No hay datos disponibles para clustering.")
        return

    # Validación de columnas necesarias
    columnas = ['Edad', 'Valor_Prestacion', 'Sucursal_Ppto', 'Especialidad']
    if not all(col in df.columns for col in columnas):
        st.warning("Faltan columnas necesarias para clustering.")
        return

    df_filtrado = df.dropna(subset=columnas)
    features = columnas

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), ['Edad', 'Valor_Prestacion']),
        ('cat', OneHotEncoder(), ['Sucursal_Ppto', 'Especialidad'])
    ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('pca', PCA(n_components=2)),
        ('kmeans', KMeans(n_clusters=3, random_state=42))
    ])

    X_transformed = pipeline.fit_transform(df_filtrado[features])
    df_filtrado['Cluster'] = pipeline.named_steps['kmeans'].labels_
    df_filtrado['PCA1'] = X_transformed[:, 0]
    df_filtrado['PCA2'] = X_transformed[:, 1]

    fig = px.scatter(df_filtrado, x='PCA1', y='PCA2', color='Cluster',
                     hover_data=['Edad', 'Valor_Prestacion', 'Sucursal_Ppto', 'Especialidad'],
                     title='Clusters identificados en las prestaciones')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_filtrado[['Edad', 'Valor_Prestacion', 'Sucursal_Ppto', 'Especialidad', 'Cluster']])

def ranking_tratamientos(df):
    st.subheader("🏆 Ranking de tratamientos por sede")

    if df.empty or 'Prestacion' not in df.columns or 'Sucursal_Ppto' not in df.columns:
        st.warning("No hay datos suficientes para el ranking.")
        return

    ranking = df.groupby(['Sucursal_Ppto', 'Prestacion']).agg(
        Total_Ventas=('Valor_Prestacion', 'sum'),
        Frecuencia=('Prestacion', 'count')
    ).reset_index()

    ranking_sorted = ranking.sort_values(['Sucursal_Ppto', 'Total_Ventas'], ascending=[True, False])
    st.dataframe(ranking_sorted)

    fig = px.bar(ranking_sorted, x='Prestacion', y='Total_Ventas', color='Sucursal_Ppto',
                 barmode='group', title='Top tratamientos por sede')
    st.plotly_chart(fig, use_container_width=True)

def edad_vs_prestacion(df):
    st.subheader("📊 Distribución de edad por prestación")

    if df.empty or 'Edad' not in df.columns or 'Prestacion' not in df.columns:
        st.warning("No hay datos para analizar edad vs prestación.")
        return

    fig = px.box(df, x='Prestacion', y='Edad', points='all', title='Edad vs Prestación')
    st.plotly_chart(fig, use_container_width=True)

    resumen = df.groupby('Prestacion').agg(
        Edad_Promedio=('Edad', 'mean'),
        Total_Prestaciones=('Prestacion', 'count')
    ).reset_index()
    st.dataframe(resumen)

def main():
    st.title("🧠 Gari Second Brain Analytics – V3 (SQL LIVE)")

    df = cargar_datos_reales()

    if not df.empty:
        st.success("✅ Datos reales cargados exitosamente desde SQL Server.")

    clustering_prestaciones(df)
    ranking_tratamientos(df)
    edad_vs_prestacion(df)

if __name__ == "__main__":
    main()
