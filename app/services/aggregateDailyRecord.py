def aggregate_daily_record(df):
    #prendiamo heartRate non nulli e maggiori di 0 e ne facciamo la media
    heart_rate_vals = df['HeartRate'][(df['HeartRate'] > 0) & (df['HeartRate'].notna())]
    heart_rate_mean = heart_rate_vals.mean() if not heart_rate_vals.empty else 0.0

    #prendiamo le durate non nulle e maggiori di 0 e prendiamo l'ultima, che rappresenta i minuti di chiamata totali fino a quell'ora
    call_duration_vals = df['CallDuration'][(df['CallDuration'] > 0) & (df['CallDuration'].notna())]
    call_duration_last = call_duration_vals.iloc[-1] if not call_duration_vals.empty else 0.0

    #prendiamo le sleepDuration non nulle e maggiori di 0 e prendiamo l'ultimo
    sleep_duration_vals = df['SleepDuration'][(df['SleepDuration'] > 0) & (df['SleepDuration'].notna())]
    sleep_duration_last = sleep_duration_vals.iloc[-1] if not sleep_duration_vals.empty else 0.0

    #prendiamo posFlag non nulli
    posflag_series = df['PosFlag'].dropna()
    #sommiamo quanti flag abbiamo a 0
    ore_fuori = (posflag_series == 0).sum()
    minuti_fuori = ore_fuori * 60

    record = {
        'HeartRate_mean': float(heart_rate_mean),
        'CallDuration_last': float(call_duration_last),
        'SleepDuration_last': float(sleep_duration_last),
        'Minuti_fuori_casa': float(minuti_fuori),
    }

    return record
