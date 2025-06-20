import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib

MODEL_FILENAME = "./../../behaviourModel.pkl"

def train_and_save_model(dataset_path= "../../dataset.csv", model_path=MODEL_FILENAME):
    # 1. Caricamento dataset
    df = pd.read_csv(dataset_path)

    # 2. Separazione feature e target
    X = df.drop(columns=["socialita"])
    y = df["socialita"]

    print("Distribuzione classi nel dataset:")
    print(y.value_counts(normalize=True))

    # 3. Train/test split (test_size 20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Distribuzione classi train:")
    print(y_train.value_counts(normalize=True))
    print("Distribuzione classi test:")
    print(y_test.value_counts(normalize=True))

    # 4. Addestramento modello
    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # 5. Salvataggio modello
    joblib.dump(model, model_path)
    print(f"Modello salvato in '{model_path}'")

    return model


def load_model(model_path=MODEL_FILENAME):
    return joblib.load(model_path)



def predict(model, input_df):
    """
    input_df: pandas DataFrame con colonne coerenti con quelle del training, senza la colonna target.
    """

    probs = model.predict_proba(input_df)
    preds = model.predict(input_df)
    return preds, probs
