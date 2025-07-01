import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib

MODEL_FILENAME = "./../../behaviourModel.pkl"


def plot_class_distribution(series, title="Distribuzione classi"):
    plt.figure(figsize=(6, 4))
    sns.countplot(x=series, palette="viridis")
    plt.title(title)
    plt.xlabel("Classe")
    plt.ylabel("Frequenza")
    plt.tight_layout()
    plt.savefig("./class_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_confusion_matrix(cm, labels):
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.title("Matrice di Confusione")
    plt.xlabel("Predetto")
    plt.ylabel("Reale")
    plt.tight_layout()
    plt.savefig("./confusion_matrix.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_classification_metrics(report_dict):
    df = pd.DataFrame(report_dict).transpose().drop("accuracy", errors="ignore")
    df = df[["precision", "recall", "f1-score"]].iloc[:-3]

    df.plot(kind="bar", figsize=(8, 5), colormap="tab10")
    plt.title("Metriche per Classe")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("./classification_metrics.png", dpi=300, bbox_inches="tight")
    plt.close()


def train_and_save_model(dataset_path="../../dataset.csv", model_path=MODEL_FILENAME):
    # 1. Caricamento dataset
    df = pd.read_csv(dataset_path)

    # 2. Separazione feature e target
    X = df.drop(columns=["socialita"])
    y = df["socialita"]

    print("Distribuzione classi nel dataset:")
    print(y.value_counts(normalize=True))

    plot_class_distribution(y, title="Distribuzione classi nel dataset")

    # 3. Train/test split (test_size 20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Distribuzione classi train:")
    print(y_train.value_counts(normalize=True))
    print("Distribuzione classi test:")
    print(y_test.value_counts(normalize=True))

    # 4. Addestramento modello
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)

    print(classification_report(y_test, y_pred))
    print(cm)

    # 5. Salvataggio modello
    joblib.dump(model, model_path)
    print(f"Modello salvato in '{model_path}'")

    # 6. Grafici
    plot_confusion_matrix(cm, labels=model.classes_)
    plot_classification_metrics(report)

    return model


def load_model(model_path=MODEL_FILENAME):
    return joblib.load(model_path)


def predict(model, input_df):

    probs = model.predict_proba(input_df)
    preds = model.predict(input_df)
    return preds, probs


if __name__ == "__main__":
    train_and_save_model()
