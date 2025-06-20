from pydantic import BaseModel
from typing import List, Optional


class Positions(BaseModel):
    latitude: float
    longitude: float
    time: str
    date: str
    patientId: str

class Data(BaseModel):
    patientId: str
    date: str
    time: str
    heartRate: Optional[int]
    callDuration: Optional[int]
    sleepDuration: int

class PositionAndData(BaseModel):
    positions: List[Positions]      #lista delle psizioni
    data: List[Data]                #lista dei dati
    address: str

class PredictionUnSupervisedForPositions(BaseModel):
    predictions: List[int]      #restituisce 24 flag binarie da 00:00 a 23:00 (1 casa, 0 uscito)


class FinalRecord(BaseModel):
    patientId: str
    date: str
    time: str
    heartRate: Optional[int]
    callDuration: Optional[int]
    sleepDuration: Optional[int]
    posPredictions: Optional[int]

class FinalDataset(BaseModel):
    records: List[FinalRecord] #deve contenere tutti i 24 record con il flag ottenuto dall'unsupervised per le posizioni e i dati presi da positionanddate

class PredictionSupervisedForData(BaseModel):
    behaviour: int