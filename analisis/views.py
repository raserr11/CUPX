from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return HttpResponse('No file selected')
        
        file = request.FILES['file']

        # Leer el archivo Excel con pandas
        try:
            df = pd.read_excel(file)
            # Procesar el DataFrame (esto es solo una muestra de cómo empezar)
            num_filas = df.shape[0]
            num_columnas = df.shape[1]
            return HttpResponse(f'Archivo subido con éxito. Número de filas: {num_filas}, Número de columnas: {num_columnas}')
        
        except Exception as e:
            return HttpResponse(f'Error procesando el archivo: {str(e)}')
        
    return render(request, 'analisis/upload.html')