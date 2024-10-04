import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def total_consumption_per_period(df):
    # Calcula el consumo total por periodo y retorna un diccionario con los totales
    totals = {f'P{p}': df[f'Consumo P{p}'].sum() for p in range(1, 7)}
    return totals

def generate_month_graph(df):
    # Definir el color de fondo de la app y el color de texto
    background_color = '#1a1a1a'
    text_color = 'white'  

    # Convertir los nombres de los meses a números y ordenar
    df['Mes_num'] = pd.to_datetime(df['Mes'], format='%B').dt.month
    df = df.sort_values('Mes_num')

    # Configurar el estilo de Seaborn
    sns.set_style("whitegrid", {'axes.facecolor': background_color})
    sns.set_context("notebook", font_scale=1.2)

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
    fig.patch.set_facecolor(background_color)  # Fondo de la figura
    ax.set_facecolor(background_color)  # Fondo de los ejes

    # Crear el gráfico de barras
    sns.barplot(x='Mes', y='Month Total', data=df, palette='Blues_d', ax=ax)

    # Ajustar textos y etiquetas
    ax.set_xlabel('Mes', fontsize=18, color=text_color, fontweight='bold')
    ax.set_ylabel('Consumo (kWh)', fontsize=18, color=text_color, fontweight='bold')

    # Ajustar los ticks de ambos ejes
    ax.tick_params(axis='x', colors=text_color, labelsize=14, rotation=45)
    ax.tick_params(axis='y', colors=text_color, labelsize=14)

    # Poner en negrita las etiquetas de los ticks del eje x
    for tick in ax.get_xticklabels():
        tick.set_fontweight('bold')

    # Poner en negrita las etiquetas de los ticks del eje y
    for tick in ax.get_yticklabels():
        tick.set_fontweight('bold')

    # Eliminar los bordes del gráfico
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Eliminar el título si existe
    ax.set_title('')

    plt.tight_layout()

    # Guardar la figura en el buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, facecolor=background_color)
    plt.close(fig)
    buf.seek(0)

    # Convertir la imagen a base64 para mostrar en la app
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64


def generate_period_graph(df):
    # Definir el color de fondo de la app y el color de texto
    background_color = '#1a1a1a'  # Color de fondo de la app
    text_color = 'white'  # Color de los textos y etiquetas

    # Obtener los totales de consumo por periodo
    totals = total_consumption_per_period(df)
    periods = list(totals.keys())
    consumption = list(totals.values())

    # Crear un DataFrame para facilitar el uso con Seaborn
    data = pd.DataFrame({
        'Periodo': periods,
        'Total Consumo': consumption
    })

    # Configurar el estilo de Seaborn
    sns.set_style("whitegrid", {'axes.facecolor': background_color})
    sns.set_context("notebook", font_scale=1.2)

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Crear el gráfico de barras
    sns.barplot(x='Periodo', y='Total Consumo', data=data, palette='Reds_d', ax=ax)

    # Ajustar textos y etiquetas
    ax.set_xlabel('Periodo', fontsize=14, color=text_color, fontweight='bold')
    ax.set_ylabel('Consumo (kWh)', fontsize=14, color=text_color, fontweight='bold')

    # Ajustar los ticks de ambos ejes
    ax.tick_params(axis='x', colors=text_color, labelsize=14)
    ax.tick_params(axis='y', colors=text_color, labelsize=14)

    # Poner en negrita las etiquetas de los ticks del eje x
    for tick in ax.get_xticklabels():
        tick.set_fontweight('bold')

    # Poner en negrita las etiquetas de los ticks del eje y
    for tick in ax.get_yticklabels():
        tick.set_fontweight('bold')

    # Eliminar los bordes del gráfico
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Eliminar el título si existe
    ax.set_title('')

    plt.tight_layout()

    # Guardar la figura en el buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, facecolor=background_color)
    plt.close(fig)
    buf.seek(0)

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64
