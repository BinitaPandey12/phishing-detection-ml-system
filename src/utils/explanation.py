def explain_prediction(index_label):
    
    idx = X_test.index.get_loc(index_label)

    feature_contributions = pd.DataFrame({
        "Feature": X_test.columns,
        "SHAP_Value": shap_values[idx]
    })

    feature_contributions["Abs_SHAP"] = (
        feature_contributions["SHAP_Value"].abs()
    )

    phishing_push = (
        feature_contributions[
            feature_contributions["SHAP_Value"] > 0
        ]
        .sort_values(by="SHAP_Value", ascending=False)
    )

    legitimate_push = (
        feature_contributions[
            feature_contributions["SHAP_Value"] < 0
        ]
        .sort_values(by="SHAP_Value")
    )

    phishing_total = phishing_push["SHAP_Value"].sum()
    legitimate_total = legitimate_push["SHAP_Value"].sum()

    return (
        phishing_push,
        legitimate_push,
        phishing_total,
        legitimate_total
    )
    
    
    
    
    
    
    def generate_explanation(index_label):

        phishing_push, legitimate_push, phishing_total, legitimate_total = (
        explain_prediction(index_label)
    )

    top_legitimate = legitimate_push.head(5)
    top_phishing = phishing_push.head(5)

    legitimate_reasons = []

    for _, row in top_legitimate.iterrows():

        feature = row["Feature"]

        reason = (
            feature_descriptions
            .get(feature, {})
            .get("negative", feature)
        )

        legitimate_reasons.append(reason)

    phishing_reasons = []

    for _, row in top_phishing.iterrows():

        feature = row["Feature"]

        reason = (
            feature_descriptions
            .get(feature, {})
            .get("positive", feature)
        )

        phishing_reasons.append(reason)

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

   
    url_position = X_test.index.get_loc(index_label)

    prediction = y_pred[url_position]

    if prediction == 1:
        prediction_label = "Phishing"
    else:
        prediction_label = "Legitimate"

   
    print("\nFactors increasing phishing suspicion:")

    for reason in phishing_reasons:
        print("•", reason)

    print("\nFactors supporting legitimacy:")

    for reason in legitimate_reasons:
        print("•", reason)

    print(f"\nFinal Prediction: {prediction_label}")

    print("\nConclusion:")
    print(final_explanation)
    
    
    