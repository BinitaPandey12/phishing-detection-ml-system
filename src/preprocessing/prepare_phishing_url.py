import pandas as pd
from scipy.io import arff

def load_and_clean_phishing_url_dataset(arff_path, output_path):
    # Load arff file
    data, meta = arff.loadarff(arff_path)
    df = pd.DataFrame(data)

    # Convert byte strings to integers
    df = df.map(lambda x: int(x.decode('utf-8')))

    # Remove duplicates
    df = df.drop_duplicates()

    # Save cleaned dataset
    df.to_csv(output_path, index=False)

    print("Dataset cleaned and saved successfully!")
    print("Final shape:", df.shape)
    print("Target distribution:")
    print(df['Result'].value_counts())

    return df

if __name__ == "__main__":
    arff_path = "data/Training Dataset.arff"
    output_path = "data/phishing_urls_cleaned.csv"
    load_and_clean_phishing_url_dataset(arff_path, output_path)