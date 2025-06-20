from typing import List
from collections import defaultdict
from app.models.schemas import *


def build_final_dataset(flag_per_hour: List[dict], original_data: List[Data], patient_id: str,
                        current_date: str) -> FinalDataset:

    print(f"original_data ({len(original_data)} record):")
    for r in original_data:
        print(f" time: {r.time}, HR: {r.heartRate}, Call: {r.callDuration}, Sleep: {r.sleepDuration}")

    print(f"flag_per_hour ({len(flag_per_hour)} record):")
    for f in flag_per_hour:
        print(f" time: {f['time']}, flag: {f['flag']}")


    # Mappa i dati originali per ora per un accesso rapido
    data_by_hour = {}  # Non usiamo defaultdict qui per distinguere tra ora assente e ora con dati nulli
    max_hour_data = -1
    for record in original_data:
        hour_str = record.time.split(":")[0]
        hour_int = int(hour_str)
        data_by_hour[f"{hour_int:02d}:00"] = record
        if hour_int > max_hour_data:
            max_hour_data = hour_int

    # Mappa i flag di posizione per ora
    flags_by_hour = {}  # Similmente, non defaultdict
    max_hour_flags = -1

    for flag_item in flag_per_hour:
        hour_part = flag_item['time'].split(":")[0]
        hour_int = int(hour_part)
        normalized_time = f"{hour_int:02d}:00"
        flags_by_hour[normalized_time] = flag_item['flag']
        if hour_int > max_hour_flags:
            max_hour_flags = hour_int


    # Determina l'ultima ora effettiva per cui elaborare i dati
    # Prendiamo il massimo tra l'ultima ora con dati e l'ultima ora con flag
    # Nel tuo caso, dovrebbero coincidere o essere molto vicine
    last_actual_hour = max(max_hour_data, max_hour_flags)

    final_records: List[FinalRecord] = []

    # Itera solo sulle ore per cui ci sono dati disponibili (da 00 a last_actual_hour)
    for h in range(last_actual_hour + 1):
        time_str = f"{h:02d}:00"  # Formato HH:00

        # Ottieni il flag di posizione per l'ora corrente (default 0 se non presente)
        pos_prediction_flag = flags_by_hour.get(time_str, None)

        # Ottieni i dati originali per l'ora corrente (default None se non presente)
        hourly_data = data_by_hour.get(time_str)

        # Inizializza i valori con default se non ci sono dati per quell'ora o se il campo è Optional
        heart_rate = None
        call_duration = None
        sleep_duration = None  # Valore di default se l'ora è presente ma il campo è assente o nullo

        if hourly_data:
            if hourly_data.heartRate is not None:
                heart_rate = hourly_data.heartRate
            if hourly_data.callDuration is not None:
                call_duration = hourly_data.callDuration
            if hourly_data.sleepDuration is not None:
                sleep_duration = hourly_data.sleepDuration

        # Crea l'oggetto FinalRecord per l'ora corrente
        record = FinalRecord(
            patientId=patient_id,
            date=current_date,
            time=time_str,
            heartRate=heart_rate,
            callDuration=call_duration,
            sleepDuration=sleep_duration,
            posPredictions=pos_prediction_flag
        )
        final_records.append(record)

    return FinalDataset(records=final_records)

