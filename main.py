from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import joblib
from rules import generate_recommendations

app = FastAPI()

# Load AI model
model = joblib.load("model/ads_model.pkl")

# Homepage with file upload form
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>AI Ads Analyzer</h1>
    <form action="/analyze" method="post" enctype="multipart/form-data">
        <input name="file" type="file" accept=".csv">
        <button type="submit">Analyze Ads</button>
    </form>
    <p>Upload a CSV with columns: spend, impressions, clicks, ctr, cpc, conversions, cpa, roas</p>
    """

# Analyze uploaded CSV and show results
@app.post("/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):
    try:
        # Read CSV
        df = pd.read_csv(file.file)

        # Features for prediction (make sure your model was trained on these)
        features = ["spend","ctr","cpc","conversions","cpa"]

        # Make predictions
        df["prediction"] = model.predict(df[features])
        label_map = {0:"Loser", 1:"Average", 2:"Winner"}
        df["prediction_label"] = df["prediction"].map(label_map)

        # Generate recommendations
        df["recommendations"] = df.apply(generate_recommendations, axis=1)

        # Color coding for prediction
        def color_prediction(pred):
            if pred == "Winner":
                return 'style="background-color:lightgreen"'
            elif pred == "Average":
                return 'style="background-color:orange"'
            else:
                return 'style="background-color:red;color:white"'

        # Convert dataframe to HTML table with color
        table_html = '<table border="1" cellpadding="5">'
        # Header
        table_html += '<tr>' + ''.join([f"<th>{col}</th>" for col in df.columns]) + '</tr>'
        # Rows
        for _, row in df.iterrows():
            table_html += '<tr>'
            for col in df.columns:
                if col == "prediction_label":
                    table_html += f"<td {color_prediction(row[col])}>{row[col]}</td>"
                else:
                    table_html += f"<td>{row[col]}</td>"
            table_html += '</tr>'
        table_html += '</table>'

        return f"""
        <h1>AI Ads Analysis Results</h1>
        {table_html}
        <br>
        <a href="/">⬅️ Back to upload page</a>
        """

    except Exception as e:
        return f"<p style='color:red'>Error processing file: {e}</p><a href='/'>⬅️ Back</a>"
