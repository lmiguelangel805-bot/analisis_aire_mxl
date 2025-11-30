import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURACIÓN GLOBAL ---
FILE_PATH = 'data/palacio-municipal, municipio de mexicali, baja california - municipal-air-quality.csv'  # Ajusta la ruta si es necesario
LIMIT_NOM = 45  # Límite NOM-025-SSA1-2014
LIMIT_WHO = 12  # Límite OMS
WATERMARK_TEXT = '© Análisis por [TU NOMBRE] - Datos AQICN'

def load_data(filepath):
    """
    Carga el dataset de calidad del aire y estandariza nombres de columnas.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no fue encontrado.")
    
    try:
        df = pd.read_csv(filepath)
        # Limpieza de espacios en nombres de columnas
        df.columns = df.columns.str.strip()
        print(f"[INFO] Dataset cargado exitosamente: {len(df)} registros.")
        return df
    except Exception as e:
        print(f"[ERROR] Fallo al leer el archivo: {e}")
        return None

def clean_data(df):
    """
    Realiza la limpieza de datos: conversión de fechas y tipos numéricos.
    """
    # Conversión de fecha
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    else:
        raise ValueError("La columna 'date' no existe en el dataset.")

    # Conversión de columnas numéricas
    cols_to_numeric = ['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']
    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Eliminación de filas sin datos de fecha o PM2.5
    df = df.dropna(subset=['date', 'pm25'])
    
    # Feature Engineering
    df['month'] = df['date'].dt.month_name()
    df['weekday'] = df['date'].dt.day_name()
    
    print("[INFO] Limpieza de datos completada.")
    return df

def add_watermark(ax):
    """
    Agrega una marca de agua anti-plagio a la gráfica actual.
    """
    ax.text(0.5, 0.5, WATERMARK_TEXT,
            transform=ax.transAxes,
            fontsize=20,
            color='gray',
            alpha=0.2,
            ha='center',
            va='center',
            rotation=20,
            weight='bold')

def plot_monthly_trend(df):
    """
    Genera y guarda el diagrama de caja mensual.
    """
    order = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
    
    plt.figure(figsize=(14, 8))
    ax = sns.boxplot(data=df, x='month', y='pm25', order=order, palette="coolwarm")
    
    # Referencias
    plt.axhline(y=LIMIT_NOM, color='red', linestyle='--', label=f'Límite NOM ({LIMIT_NOM})')
    plt.axhline(y=LIMIT_WHO, color='green', linestyle='--', label=f'Meta OMS ({LIMIT_WHO})')
    
    plt.title('Distribución Mensual de Contaminación PM2.5 en Mexicali', fontsize=14, weight='bold')
    plt.ylabel('Concentración PM2.5 (µg/m³)')
    plt.xlabel('Mes')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    add_watermark(ax)
    plt.tight_layout()
    plt.savefig('images/monthly_trend.png', dpi=300)
    print("[INFO] Gráfica mensual guardada en 'images/monthly_trend.png'")
    plt.close()

def plot_weekly_trend(df):
    """
    Genera y guarda el diagrama de caja semanal.
    """
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(data=df, x='weekday', y='pm25', order=order, palette="viridis")
    
    plt.axhline(y=LIMIT_NOM, color='red', linestyle='--', label=f'Límite NOM ({LIMIT_NOM})')
    
    plt.title('Distribución Semanal de Contaminación PM2.5', fontsize=14, weight='bold')
    plt.ylabel('Concentración PM2.5 (µg/m³)')
    plt.xlabel('Día de la Semana')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    add_watermark(ax)
    plt.tight_layout()
    plt.savefig('images/weekly_trend.png', dpi=300)
    print("[INFO] Gráfica semanal guardada en 'images/weekly_trend.png'")
    plt.close()

if __name__ == "__main__":
    # Creación de carpeta para imágenes si no existe
    if not os.path.exists('images'):
        os.makedirs('images')

    # Flujo de ejecución principal
    df_raw = load_data(FILE_PATH)
    
    if df_raw is not None:
        df_clean = clean_data(df_raw)
        
        # Generación de reportes visuales
        plot_monthly_trend(df_clean)
        plot_weekly_trend(df_clean)
        
        print("[SUCCESS] Análisis finalizado correctamente.")