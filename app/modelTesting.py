import pandas as pd

from app.services.inference import *

import hashlib

def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


# Simula un record aggregato
test_input_dict = {
    "HeartRate_mean": 70.4,
    "CallDuration_last": 100.0,
    "SleepDuration_last": 600.0,
    "Minuti_fuori_casa": 0.0
}

# Fai un DataFrame esattamente come fa l'API
test_input_df = pd.DataFrame([test_input_dict])

# Carica il modello (ricorda: DEVE essere quello corretto e aggiornato)
model = load_model("../behaviourModel.pkl")



# Fai inferenza
preds, probs = predict(model, test_input_df)


print(f"Input di test: {test_input_dict}")
print("Ordine colonne API:", list(test_input_df.columns))
print(f"Predizione: {preds[0]}")
print(f"Probabilità: {probs}")

print(model)