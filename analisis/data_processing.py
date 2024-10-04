import pandas as pd
from datetime import timedelta

# Info del Cliente (página=0)
# +----------------------------------------------------------------------------------------------------------

def customer_info(df):

    df_c_info = df.loc[:0,['CUPS', 'Titular', 'CIF', 'Distribuidora',
       'Localidad del suministro', 'Cod. Postal del suministro', 'Tarifa', 'Ultima lectura', 'CNAE',
       'Fecha cambio última comercializadora', 'Potencia BIE']]
    df_c_info.rename(columns={'Fecha cambio última comercializadora':'Último cambio comerc', 'Localidad del suministro':'Localidad','Cod. Postal del suministro':'CP'}, inplace=True)

    pot_index = df[df['Direccion del suministro'] == 'Potencia'].index[0] +1
    print(pot_index)
    df_pot = df.iloc[pot_index:pot_index+6, df.columns.get_loc('Direccion del suministro')].reset_index().drop('index',axis=1)
    df_pot['Pot'] = [f'P{i+1}' for i in range(len(df_pot))]
    df_pot = df_pot[['Pot','Direccion del suministro']]
    df_pot.rename(columns={'Direccion del suministro': 'Potencia_kW'}, inplace=True)

    return df_c_info, df_pot


# Consumo Activo (página=1)
# +----------------------------------------------------------------------------------------------------------
def dates_fix(df):
    df_copy = df.copy()

    # Limpiamos espacios en blanco
    df_copy['Fecha lectura anterior'] = df_copy['Fecha lectura anterior'].str.strip()
    df_copy['Fecha lectura'] = df_copy['Fecha lectura'].str.strip()

    # Convertimos las columnas de fecha a datetime de pandas
    df_copy['Fecha lectura anterior'] = pd.to_datetime(df_copy['Fecha lectura anterior'], format='%d/%m/%Y')
    df_copy['Fecha lectura'] = pd.to_datetime(df_copy['Fecha lectura'], format='%d/%m/%Y')

    # Calculamos la duración del intervalo
    df_copy['Duración días'] = (df_copy['Fecha lectura'] - df_copy['Fecha lectura anterior']).dt.days

    
    return df_copy


def distrib_1day_rows(df):
    for i, row in df.iterrows():        

        # Verificamos si el intervalo de la fila es de solo 1 día
        if row['Duración días'] == 1:
            # Sacamos el mes de la fecha
            actual_month = row['Fecha lectura'].month

            # Comparamos con la fila anterior para ver si tienen el mismo mes
            if i > 0 and df.loc[i-1, 'Fecha lectura'].month == actual_month:
                # ¿Es el mismo mes que la fila anterior? --> sumamos el consumo por cada periodo
                for p in range(1, 7):  # P1 a P6
                    column = f'Consumo P{p}'
                    if column in df.columns:
                        df.loc[i-1, column] += row.get(column, 0)
            # Si la fila anterior no es del mismo mes, revisamos la siguiente
            elif i < len(df) - 1 and df.loc[i+1, 'Fecha lectura'].month == actual_month:
                # ¿Es el mismo mes que la fila siguiente? --> sumamos el consumo por cada periodo
                for p in range(1, 7):  # P1 a P6
                    column = f'Consumo P{p}'
                    if column in df.columns:
                        df.loc[i+1, column] += row.get(column, 0)
    
    # Eliminamos filas de 1 día que sobran después de repartir el consumo
    no_1dayrows_df = df[df['Duración días'] != 1].copy().reset_index(drop=True)
    return no_1dayrows_df



periodict = {1: ['P1', 'P2', 'P6'],
 2: ['P1', 'P2', 'P6'],
 3: ['P2', 'P3', 'P6'],
 4: ['P4', 'P5', 'P6'],
 5: ['P4', 'P5', 'P6'],
 6: ['P3', 'P4', 'P6'],
 7: ['P1', 'P2', 'P6'],
 8: ['P3', 'P4', 'P6'],
 9: ['P3', 'P4', 'P6'],
 10: ['P4', 'P5', 'P6'],
 11: ['P2', 'P3', 'P6'],
 12: ['P1', 'P2', 'P6']}


def div_rows(df):
    splited_rows = []
    work_df = df.copy()
    
    # Iterar sobre cada fila del DataFrame
    for _, row in work_df.iterrows():
        start_date = row['Fecha lectura anterior']
        end_date = row['Fecha lectura']
        consumption_per_period = {f'Consumo P{i}': row[f'Consumo P{i}'] for i in range(1, 7)}  # Consumo de P1 a P6
        total_days = row['Duración días']

        # Dividir si las fechas abarcan meses diferentes
        if start_date.month != end_date.month or start_date.year != end_date.year:
            # Obtener periodos de cada mes
            periods_part1 = periodict[start_date.month]
            periods_part2 = periodict[end_date.month]
            
            # Encontrar periodos compartidos
            shared_periods = set(periods_part1).intersection(periods_part2)
            unique_periods_part1 = set(periods_part1) - shared_periods
            unique_periods_part2 = set(periods_part2) - shared_periods

            # Parte 1: desde start_date hasta el último día del mes de inicio
            last_day_of_start_month = pd.Timestamp(start_date.year, start_date.month, 
                                                   pd.Timestamp(start_date.year, start_date.month, 1).days_in_month)
            days_part1 = (last_day_of_start_month - start_date).days + 1
            prop_days1 = days_part1 / total_days

            # Distribuir consumo proporcionalmente para periodos compartidos
            consumptions_part1 = {
                f'Consumo P{p[-1]}': round(prop_days1 * consumption_per_period[f'Consumo P{p[-1]}'], 0)
                for p in shared_periods
            }
            # Asignar consumo completo para periodos únicos del primer mes
            consumptions_part1.update({
                f'Consumo P{p[-1]}': consumption_per_period[f'Consumo P{p[-1]}']
                for p in unique_periods_part1
            })

            splited_rows.append({
                'Fecha lectura anterior': start_date, 
                'Fecha lectura': last_day_of_start_month,
                'Duración días': days_part1,
                'Proporción días': prop_days1,
                **consumptions_part1
            })

            # Parte 2: desde el primer día del siguiente mes hasta end_date
            first_day_of_next_month = last_day_of_start_month + timedelta(days=1)
            days_part2 = (end_date - first_day_of_next_month).days + 1
            prop_days2 = days_part2 / total_days

            # Distribuir consumo proporcionalmente para periodos compartidos en el segundo mes
            consumptions_part2 = {
                f'Consumo P{p[-1]}': consumption_per_period[f'Consumo P{p[-1]}'] - consumptions_part1.get(f'Consumo P{p[-1]}', 0)
                for p in shared_periods
            }
            # Asignar consumo completo para periodos únicos del segundo mes
            consumptions_part2.update({
                f'Consumo P{p[-1]}': consumption_per_period[f'Consumo P{p[-1]}']
                for p in unique_periods_part2
            })

            splited_rows.append({
                'Fecha lectura anterior': first_day_of_next_month, 
                'Fecha lectura': end_date,
                'Duración días': days_part2,
                'Proporción días': prop_days2,
                **consumptions_part2
            })

        else:
            # Si las fechas están en el mismo mes, mantener la fila con todo su consumo
            month_periods = periodict[start_date.month]
            month_consumptions = {
                f'Consumo P{p[-1]}': consumption_per_period[f'Consumo P{p[-1]}'] for p in month_periods
            }
            
            splited_rows.append({
                'Fecha lectura anterior': start_date, 
                'Fecha lectura': end_date,
                'Duración días': total_days,
                'Proporción días': 1,
                **month_consumptions
            })

    # Crear DataFrame con filas divididas y redistribuir filas de 1 día
    pre_df = pd.DataFrame(splited_rows)
    pre_df['Mes'] = pre_df['Fecha lectura anterior'].dt.strftime('%B')
    final_df = distrib_1day_rows(pre_df)

    # Reordenar columnas
    orden_columnas = ['Fecha lectura anterior', 'Fecha lectura', 'Duración días', 'Proporción días', 
                  'Consumo P1', 'Consumo P2', 'Consumo P3', 'Consumo P4', 'Consumo P5', 'Consumo P6', 'Mes']
    final_df = final_df[orden_columnas].fillna(0)

    return final_df



def join_per_month(df):
    work_df = df.copy()  # Hacemos una copia del DataFrame para no modificar el original
    i = 0  # Inicializamos el índice para recorrer el DataFrame

    while i < len(work_df) - 1:  # Recorremos hasta la penúltima fila
        # Obtenemos el mes actual y el de la siguiente fila
        actual_month = work_df.loc[i, 'Mes']
        next_row_month = work_df.loc[i + 1, 'Mes']

        # Si los meses coinciden
        if actual_month == next_row_month:
            # Actualizamos la fecha de fin al de la siguiente fila
            work_df.loc[i, 'Fecha lectura'] = work_df.loc[i + 1, 'Fecha lectura']

            # Sumamos los consumos de P1 a P6
            for p in range(1, 7):
                if f'Consumo P{p}' in work_df.columns:
                    work_df.loc[i, f'Consumo P{p}'] += work_df.loc[i + 1, f'Consumo P{p}']

            # Eliminamos la siguiente fila porque la hemos fusionado
            work_df = work_df.drop(i + 1).reset_index(drop=True)
        else:
            i += 1  # Si son meses diferentes, pasamos a la siguiente fila

    return work_df

def select_last_year(df):

    last_date = df['Fecha lectura'].max()
    actual_year = last_date.year
    prev_year = actual_year - 1
    last_year_df = df[df['Fecha lectura'].dt.year == actual_year]
    prev_year_df = df[df['Fecha lectura'].dt.year == prev_year]

    # Si faltan meses del año actual, añadimos de los del año anterior
    if len(last_year_df) < 12:
        n_missing = 12 - len(last_year_df)
        m_to_add = prev_year_df.loc[-n_missing:,:]
        last_year_df = pd.concat([last_year_df, m_to_add], axis=0)

    order = ['Mes', 'Consumo P1', 'Consumo P2', 'Consumo P3',
       'Consumo P4', 'Consumo P5', 'Consumo P6']

    final_df = last_year_df[order]

    return final_df

def consump_by_month(df):
    work_df = df.copy()

    for i, row in df.iterrows():
        work_df.loc[i,'Month Total'] = row[['Consumo P1', 'Consumo P2', 'Consumo P3', 'Consumo P4',
       'Consumo P5', 'Consumo P6']].sum()
    
    return work_df

def process_active(df):

    raw = df.copy()
    fixed_dates = dates_fix(raw)
    div_rows_df = div_rows(fixed_dates)
    full_months_df = join_per_month(div_rows_df)
    last_year_df = select_last_year(full_months_df)
    months_totals = consump_by_month(last_year_df)

    return months_totals

