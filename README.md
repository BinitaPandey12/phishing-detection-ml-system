# Phishing URL Detection and Explainability System

## Project Overview

This project aims to detect phishing websites using machine learning and provide human-readable explanations for each prediction using SHAP (SHapley Additive Explanations).

The system analyzes URL-based features, predicts whether a website is phishing or legitimate, and explains which features influenced the prediction.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd phishing-detection-ml-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment:

**macOS/Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

```bash
jupyter notebook
```

Open the notebooks folder and run the notebooks.

## Current Status

* Model training completed
* Model comparison completed
* Model selection completed
* Evaluation completed
* False Positive and False Negative analysis completed
* SHAP integration completed
* Human-readable explanation generation completed
* URL feature extraction in progress

## Future Improvements

* Real-time URL feature extraction
* Web interface for predictions
* Browser extension integration
* Mobile application integration
* Enhanced explainability visualizations
