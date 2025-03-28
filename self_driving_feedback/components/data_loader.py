import pandas as pd


def load_analysis_stats():
    data = pd.read_csv("./data/survey_results.csv")
    drive_mean = data[["q1", "q2", "q3", "q4", "q5"]].mean().mean()
    emergency_mean = data[["q6", "q7", "q8", "q9", "q10"]].mean().mean()
    parking_mean = data[["q11", "q12", "q13"]].mean().mean()
    overall_mean = data[["q14", "q15", "q16"]].mean().mean()
    return {
        "driving_comfort": drive_mean,
        "emergency_response": emergency_mean,
        "parking_function": parking_mean,
        "overall_satisfaction": overall_mean,
    }
