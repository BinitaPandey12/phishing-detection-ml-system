import joblib
from pathlib import Path

from src.preprocessing.sms_cleaner import clean_message


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "message" / "message_svm_final.joblib"

pipeline = joblib.load(MODEL_PATH)


def predict_message(message: str):

    cleaned_message = clean_message(message)

    prediction = pipeline.predict([cleaned_message])[0]

    if prediction == 0:
        label = "Phishing"
    else:
        label = "Legitimate"

    return {
        "prediction": label,
        "prediction_value": int(prediction)
    }
