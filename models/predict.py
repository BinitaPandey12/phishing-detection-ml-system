import json
from pathlib import Path

from xgboost import XGBClassifier
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

model = XGBClassifier()
model.load_model(BASE_DIR / "models" / "url" / "xgb_model.ubj")

with open(BASE_DIR / "notebooks" / "model_metadata.json") as f:
    metadata = json.load(f)

FEATURE_ORDER = metadata["feature_order"]


def predict_url(features):

    df = pd.DataFrame([features])

    df = df[FEATURE_ORDER]

    prediction = model.predict(df)

    return prediction[0]
