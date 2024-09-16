import pandas as pd

def dates_fix(df):
    df_copy = df.copy()

    # Delete blank spaces
    df_copy['Fecha lectura anterior'] = df_copy['Fecha lectura anterior'].str.strip()
    df_copy['Fecha lectura'] = df_copy['Fecha lectura'].str.strip()

    # Convert date columns to pandas datetime
    df_copy['Fecha lectura anterior'] = pd.to_datetime(df_copy['Fecha lectura anterior'], format='%d/%m/%Y')
    df_copy['Fecha lectura'] = pd.to_datetime(df_copy['Fecha lectura'], format='%d/%m/%Y')

    # Calculating interval length
    df_copy['Duración días'] = (df_copy['Fecha lectura'] - df_copy['Fecha lectura anterior']).dt.days

    return df_copy

def distrib_1day_rows(df):
    for i, row in df.iterrows():        

        # Check if row interval is just 1 day
        if row['Duración días'] == 1:
            # We extract the date's month
            actual_month = row['Fecha lectura'].month

            # Check previous row to si if they have the same month
            if i > 0 and df.loc[i-1, 'Fecha lectura'].month == actual_month:
                # Has the same month as previous row? --> sum the consumption for every period
                for p in range(1, 7):  # P1 a P6
                    column = f'Consumo P{p}'
                    if column in df.columns:
                        df.loc[i-1, column] += row.get(column, 0)
            # Previous row hasn't the same month, check next row
            elif i < len(df) - 1 and df.loc[i+1, 'Fecha lectura'].month == actual_month:
                # Has the same month as next row? --> sum the consumption for every period
                for p in range(1, 7):  # P1 a P6
                    column = f'Consumo P{p}'
                    if column in df.columns:
                        df.loc[i+1, column] += row.get(column, 0)
    
    # Delete 1 day rows after distributing consumption
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

def div_rows(df, periodict):
    splited_rows = []
    work_df = dates_fix(df)
    
    # Loop through each row in the original DataFrame
    for _, row in work_df.iterrows():
        start_date = row['Fecha lectura anterior']
        end_date = row['Fecha lectura']
        consumption_per_period = {f'Consumo P{i}': row[f'Consumo P{i}'] for i in range(1, 7)}  # Get consumption for P1 to P6
        total_days = row['Duración días']

        # If dates span over different months, split the row
        if start_date.month != end_date.month or start_date.year != end_date.year:
            # Get periods for each month
            periods_part1 = periodict[start_date.month]  # First month periods
            periods_part2 = periodict[end_date.month]  # Second month periods
            
            # Find the shared periods between both months
            shared_periods = set(periods_part1).intersection(periods_part2)
            
            # Get the periods that are unique to each month
            unique_periods_part1 = set(periods_part1) - shared_periods
            unique_periods_part2 = set(periods_part2) - shared_periods

            # First part: from start_date to the last day of start month
            last_day_of_start_month = pd.Timestamp(start_date.year, start_date.month, 
                                                   pd.Timestamp(start_date.year, start_date.month, 1).days_in_month)
            days_part1 = (last_day_of_start_month - start_date).days + 1
            prop_days1 = days_part1 / total_days

            # Distribute consumption proportionally for shared periods
            consumptions_part1 = {
                f'Consumo P{p[-1]}': round(prop_days1 * consumption_per_period[f'Consumo P{p[-1]}'], 0)
                for p in shared_periods
            }
            # Assign full consumption for unique periods in the first month
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

            # Second part: from the first day of the next month to end_date
            first_day_of_next_month = last_day_of_start_month + timedelta(days=1)
            days_part2 = (end_date - first_day_of_next_month).days + 1
            prop_days2 = days_part2 / total_days

            # Distribute consumption proportionally for shared periods in the second month
            consumptions_part2 = {
                f'Consumo P{p[-1]}': consumption_per_period[f'Consumo P{p[-1]}'] - consumptions_part1.get(f'Consumo P{p[-1]}', 0)
                for p in shared_periods
            }
            # Assign full consumption for unique periods in the second month
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
            # If the dates are within the same month, keep the row as is with all its consumption
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

    # Create DataFrame with the split rows and redistribute any 1-day rows
    final_df = pd.DataFrame(splited_rows)
    final_df = distrib_1day_rows(final_df)

    # Reorder the columns to keep things consistent
    orden_columnas = ['Fecha lectura anterior', 'Fecha lectura', 'Duración días', 'Proporción días', 
                  'Consumo P1', 'Consumo P2', 'Consumo P3', 'Consumo P4', 'Consumo P5', 'Consumo P6']
    final_df = final_df[orden_columnas].fillna(0)

    return final_df, splited_rows

# Apply the function to split rows and display the result
df_dividido, filas_dic = div_rows(df, periodict)

# Show the resulting DataFrame
df_dividido.head(35)
