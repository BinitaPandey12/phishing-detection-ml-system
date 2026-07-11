import json
import pandas as pd
import shap
from models.predict import predict_url
from src.utils.feature_description import feature_descriptions

from xgboost import XGBClassifier

model = XGBClassifier()
model.load_model("notebooks/xgb_model.ubj")

with open("notebooks/model_metadata.json") as f:
    metadata = json.load(f)

FEATURE_ORDER = metadata["feature_order"]

explainer = shap.TreeExplainer(model)


def explain_prediction(features):

    df = pd.DataFrame([features])

    df = df[FEATURE_ORDER]

    shap_values = explainer.shap_values(df)

    feature_contributions = pd.DataFrame(
        {
            "Feature": df.columns,
            "Feature_Value": df.iloc[0].values,
            "SHAP_Value": shap_values[0],
        }
    )

    feature_contributions["Abs_SHAP"] = (
        feature_contributions["SHAP_Value"].abs()
    )

    phishing_push = (
        feature_contributions[
            feature_contributions["SHAP_Value"] > 0
        ]
        .sort_values(
            by="SHAP_Value",
            ascending=False,
        )
    )

    legitimate_push = (
        feature_contributions[
            feature_contributions["SHAP_Value"] < 0
        ]
        .sort_values(
            by="SHAP_Value"
        )
    )

    phishing_total = phishing_push["SHAP_Value"].sum()

    legitimate_total = legitimate_push["SHAP_Value"].sum()

    return {
        "all_features": feature_contributions,
        "phishing_push": phishing_push,
        "legitimate_push": legitimate_push,
        "phishing_total": phishing_total,
        "legitimate_total": legitimate_total,
    }


def generate_explanation(features):

    result = explain_prediction(features)

    phishing_push = result["phishing_push"]
    legitimate_push = result["legitimate_push"]

    phishing_total = result["phishing_total"]
    legitimate_total = result["legitimate_total"]

    top_phishing = phishing_push.head(5)
    top_legitimate = legitimate_push.head(5)

    prediction = predict_url(features)

    if prediction == 1:
        prediction_label = "PHISHING"
    else:
        prediction_label = "LEGITIMATE"

    phishing_reasons = []

    for _, row in top_phishing.iterrows():

        feature = row["Feature"]

        reason = (
            feature_descriptions
            .get(feature, {})
            .get("positive", feature)
        )

        phishing_reasons.append(reason)

    legitimate_reasons = []

    for _, row in top_legitimate.iterrows():

        feature = row["Feature"]

        reason = (
            feature_descriptions
            .get(feature, {})
            .get("negative", feature)
        )

        legitimate_reasons.append(reason)

    if abs(legitimate_total) > phishing_total:

        final_explanation = (
            f"Although several phishing indicators were detected, "
            f"the legitimate-oriented features exerted a stronger "
            f"overall influence ({abs(legitimate_total):.2f}) "
            f"than the phishing-oriented features "
            f"({phishing_total:.2f})."
        )

    else:

        final_explanation = (
            f"The phishing-oriented features exerted a stronger "
            f"overall influence ({phishing_total:.2f}) than the "
            f"legitimate-oriented features "
            f"({abs(legitimate_total):.2f})."
        )

    formatted_explanation = (
        "Factors increasing phishing suspicion:\n"
        + "\n".join(f"• {reason}" for reason in phishing_reasons)
        + "\n\nFactors supporting legitimacy:\n"
        + "\n".join(f"• {reason}" for reason in legitimate_reasons)
        + f"\n\nFinal Prediction: {prediction_label}"
        + f"\n\nConclusion:\n{final_explanation}"
    )

    return {
        "prediction": prediction_label,
        "phishing_reasons": phishing_reasons,
        "legitimate_reasons": legitimate_reasons,
        "conclusion": final_explanation,
        "formatted_explanation": formatted_explanation
    }
