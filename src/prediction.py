import pandas as pd
import streamlit as st
from kedro.framework.session import KedroSession


def predict():
    st.title("Insurance Premium Prediction")
    age = st.sidebar.slider("Age", min_value=18, max_value=100)
    sex = st.sidebar.radio("Sex", ["male", "female"])
    bmi = st.sidebar.slider("BMI", min_value=14, max_value=54)
    children = st.sidebar.slider("Children", min_value=0, max_value=10)
    smoker = st.sidebar.radio("Smoker", ["yes", "no"])
    region = st.sidebar.radio(
        "Region", ["northwest", "northeast", "southeast", "southwest"]
    )
    if st.button("Predict"):
        predict_features = pd.DataFrame(
            data=[[age, sex, bmi, children, smoker, region]],
            columns=["age", "sex", "bmi", "children", "smoker", "region"],
        )
        predict_features.to_csv("./data/05_model_input/pred_features.csv")
        with KedroSession.create("km_insurance") as session:
            context = session.load_context()
            context.run(pipeline_name="pred")
            pred_results = context.catalog.load("pred_results")
            st.success(f"The result is {pred_results.values}")


if __name__ == "__main__":
    predict()
