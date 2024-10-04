from django.shortcuts import render, redirect
from django.http import HttpResponse
import pandas as pd
from .data_processing import process_active, customer_info
from .data_analysis import generate_period_graph, generate_month_graph

def upload_file(request):
    # Verificamos si el método de la solicitud es POST
    if request.method == 'POST':
        # Comprobamos si hay un archivo en la solicitud
        if 'file' not in request.FILES:
            return HttpResponse('No file selected')  # Mensaje si no se seleccionó ningún archivo

        file = request.FILES['file']  # Obtenemos el archivo subido
        
        try:
            # Leer el archivo Excel en memoria
            df_customer = pd.read_excel(file, sheet_name=0)  # Hoja de información del cliente
            df_active = pd.read_excel(file, sheet_name=1)  # Hoja de consumo activo
            
            # Procesar los datos de los DataFrames
            custom_info, pot = customer_info(df_customer)  # Obtener información del cliente y potencias
            processed_df = process_active(df_active)  # Procesar datos de consumo activo

            # Guardar los datos procesados en la sesión como JSON
            request.session['custom_info'] = custom_info.to_json()
            request.session['pot'] = pot.to_json()
            request.session['processed_df'] = processed_df.to_json()
        
        except Exception as e:
            return HttpResponse(f'Error procesando el archivo: {str(e)}')  # Mensaje de error si algo sale mal
        
        # Redirigir a la vista de análisis
        return redirect('data_preview')

    return render(request, 'upload.html')  # Renderizar la plantilla de subida de archivos


def data_preview(request):
    # Comprobar si hay datos procesados en la sesión
    if 'processed_df' not in request.session:
        return HttpResponse('No data to process.')  # Mensaje si no hay datos para procesar

    try:
        # Reconstruir los DataFrames desde JSON guardado en la sesión
        processed_df = pd.read_json(request.session['processed_df'])
        custom_info = pd.read_json(request.session['custom_info'])
        pot = pd.read_json(request.session['pot'])

        # Generar gráficos y obtener imágenes en base64
        period_graph_base64 = generate_period_graph(processed_df)  # Gráfico por periodos
        month_graph_base64 = generate_month_graph(processed_df)    # Gráfico por meses

        # Convertir custom_info y pot a formatos adecuados para la plantilla
        custom_info_dict = custom_info.to_dict(orient='records')[0]  # Suponemos que solo hay una fila
        pot_list = pot.to_dict(orient='records')  # Lista de diccionarios para cada potencia

    except Exception as e:
        return HttpResponse(f'Error generando gráficos: {str(e)}')  # Mensaje de error si algo sale mal

    # Preparar la información para mostrar
    custom_info_display = {}
    for key, value in custom_info.items():
        key_display = key.replace('_', ' ')  # Reemplazar guiones bajos por espacios
        custom_info_display[key_display] = value

    # Contexto para la plantilla
    context = {
        'period_graph': period_graph_base64,
        'month_graph': month_graph_base64,
        'custom_info': custom_info_dict,
        'pot': pot_list,
    }

    return render(request, 'preview.html', context)  # Renderizar la plantilla de vista previa

