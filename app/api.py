# app/api.py
from http.client import HTTPException

from fastapi import *
import pandas as pd
from starlette.responses import JSONResponse

from .auth import verify_jwt
from .models.schemas import *
from .services.aggregateDailyRecord import aggregate_daily_record
from .services.buildFinalDataset import build_final_dataset
from .services.convertNumpyToPython import convert_numpy_to_python
from .services.geocoding import geocode_address
from .services.inference import *
from .services.processPositions import *


router = APIRouter()


@router.post("/model", response_model=PredictionSupervisedForData)
def ai_model_endpoint(
    data: PositionAndData,
    token_payload=Depends(verify_jwt)
):

    #1) dobbiamo estrarre la lista delle posizioni e indirzzo da data.
    positionList=[p.dict() for p in data.positions]

    #2) dobbiamo trasformare l'indirizzo in coordinate geografiche
    address=data.address
    homeLatitude, homeLongitude = geocode_address(address)
    if homeLatitude is None  or homeLongitude is None:
        raise HTTPException(status_code=400, detail="Invalide address")

    print(f"Indirizzo geocodificato per '{address}': Latitudine={homeLatitude}, Longitudine={homeLongitude}")

    #3) dobbiamo applicare modello unsupervised alla lista di posizioni

    flagPerHour=process_positions(positionList,homeLatitude, homeLongitude)

    #4) costruire il FinalDataset

    patient_id = data.data[0].patientId
    #current_date = data.data[0].date if data.data else (data.positions[0].date if data.positions else "default_date")
    current_date = data.data[0].date if data.data else data.positions[0].date

    final_dataset: FinalDataset = build_final_dataset(
        flag_per_hour=flagPerHour,
        original_data=data.data,
        patient_id=patient_id,
        current_date=current_date
    )

    print("Final Dataset costruito:")
    for record in final_dataset.records:
        print(
            f"  Ora: {record.time}, HeartRate: {record.heartRate}, CallDuration: {record.callDuration}, SleepDuration: {record.sleepDuration}, PosFlag: {record.posPredictions}")

    records_list = []
    for record in final_dataset.records:
        records_list.append({
            'Ora': record.time,
            'HeartRate': record.heartRate,
            'CallDuration': record.callDuration,
            'SleepDuration': record.sleepDuration,
            'PosFlag': record.posPredictions
        })
    df = pd.DataFrame(records_list)


    # aggrega in un unico record giornaliero
    aggregated_record = aggregate_daily_record(df)


    clean_aggregated = convert_numpy_to_python(aggregated_record)


    #sistemo formato del punto di test da dare al modello


    input_dict = {
        "HeartRate_mean": float(clean_aggregated.get("HeartRate_mean", 0)),
        "CallDuration_last": float(clean_aggregated.get("CallDuration_last", 0)),
        "SleepDuration_last": float(clean_aggregated.get("SleepDuration_last", 0)),
        "Minuti_fuori_casa": float(clean_aggregated.get("Minuti_fuori_casa", 0)),
    }

    input_df = pd.DataFrame([input_dict])


    # 5) applicare modello supervised

    model=load_model("behaviourModel.pkl")


    # 6) restituire il behaviour

    preds, probs = predict(model, input_df)
    predicted_label = int(preds[0])

    result={
        "patientId": patient_id,
        "behaviour": predicted_label
    }

    print("probabilità:", probs)

    return JSONResponse(content=result, status_code=200)
