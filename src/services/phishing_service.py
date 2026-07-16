from src.preprocessing.feature_extraction import extract_url_features
from src.utils.explanation import generate_explanation


def analyze_url(url):

    features = extract_url_features(url)

    # print("Extracted Features:")
    # for key, value in features.items():
    #     print(f"{key}: {value}")

    result = generate_explanation(features)

    # print("\nPrediction Result:")
    # print(result)

    return result
