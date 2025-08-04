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

def calcular_edad(fecha):
    return (datetime.now().date() - fecha.date()).days // 365

def cargar_datos():
    # Reemplaza esto con la conexión real a SQL Server
    # Aquí va una carga simulada de ejemplo:
    data = {
        'FechaNacimiento': ['1980-05-20', '2000-01-15', '1995-07-30', '1975-03-10', '1988-11-22', '2002-09-01'],
        'Valor_Prestacion': [150000, 320000, 47000, 141000, 42100, 250000],
        'Sucursal_Ppto': ['ROMA', 'KENNEDY', 'ROMA', 'SUBA', 'SUBA', 'KENNEDY'],
        'Especialidad': ['ODONTOLOGÍA GENERAL', 'ORTODONCIA', 'ORTODONCIA', 'REHABILITACIÓN', 'ORTODONCIA', 'ORTODONCIA'],
        'Prestacion': ['Ortodoncia', 'Ortodoncia', 'Limpieza Dental', 'Endodoncia', 'Limpieza Dental', 'Ortodoncia']
    }
    df = pd.DataFrame(data)
    df['FechaNacimiento'] = pd.to_datetime(df['FechaNacimiento'], errors='coerce')
    df['Edad'] = df['FechaNacimiento'].apply(calcular_edad)
    return df

def clustering_prestaciones(df):
    st.subheader("🔍 Clustering de pacientes (Edad + Valor + Categóricos)")

    features = ['Edad', 'Valor_Prestacion', 'Sucursal_Ppto', 'Especialidad']
    numeric_features = ['Edad', 'Valor_Prestacion']
    categorical_features = ['Sucursal_Ppto', 'Especialidad']

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('pca', PCA(n_components=2)),
        ('kmeans', KMeans(n_clusters=3, random_state=42))
    ])

    X_transformed = pipeline.fit_transform(df[features])
    df['Cluster'] = pipeline.named_steps['kmeans'].labels_
    df['PCA1'] = X_transformed[:, 0]
    df['PCA2'] = X_transformed[:, 1]

    fig = px.scatter(df, x='PCA1', y='PCA2', color='Cluster',
                     hover_data=['Edad', 'Valor_Prestacion', 'Sucursal_Ppto', 'Especialidad'],
                     title='Clusters identificados en las prestaciones')
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df[['Edad', 'Valor_Prestacion', 'Sucursal_Ppto', 'Especialidad', 'Cluster']])

def ranking_tratamientos(df):
    st.subheader("🏆 Ranking de tratamientos por sede")

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

    fig = px.box(df, x='Prestacion', y='Edad', points='all', title='Edad vs Prestación')
    st.plotly_chart(fig, use_container_width=True)

    resumen = df.groupby('Prestacion').agg(
        Edad_Promedio=('Edad', 'mean'),
        Total_Prestaciones=('Prestacion', 'count')
    ).reset_index()
    st.dataframe(resumen)

def main():
    st.title("🧠 Gari Second Brain Analytics – Versión 3")

    df = cargar_datos()
    st.success("Datos cargados correctamente.")

    clustering_prestaciones(df)
    ranking_tratamientos(df)
    edad_vs_prestacion(df)

if __name__ == "__main__":
    main()
