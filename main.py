from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import joblib
import gradio as gr
import threading
import uvicorn
import numpy as np
import os

# Initialize FastAPI app
app = FastAPI(title="House Price Prediction API", version="1.0.0")

# Load the trained model
model = joblib.load("house_model.pkl")

class HousePredictionInput(BaseModel):
    data: Optional[List[float]] = [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]

class PredictionResponse(BaseModel):
    prediction: float
    prediction_formatted: str

@app.get("/", response_class=HTMLResponse)
def root():
    """Root endpoint with basic info"""
    return """
    <html>
        <head>
            <title>House Price Prediction API</title>
        </head>
        <body>
            <h1>🏠 House Price Prediction API</h1>
            <h2>Available Endpoints:</h2>
            <ul>
                <li><a href="/docs">📚 API Documentation (Swagger)</a></li>
                <li><a href="/predict">/predict</a> - POST endpoint for predictions</li>
                <li><a href="/gradio">🎯 Interactive Gradio UI</a></li>
            </ul>
            <h3>Sample Input Features (California Housing Dataset):</h3>
            <ol>
                <li>MedInc - Median income in block group</li>
                <li>HouseAge - Median house age in block group</li>
                <li>AveRooms - Average number of rooms per household</li>
                <li>AveBedrms - Average number of bedrooms per household</li>
                <li>Population - Block group population</li>
                <li>AveOccup - Average number of household members</li>
                <li>Latitude - Latitude</li>
                <li>Longitude - Longitude</li>
            </ol>
        </body>
    </html>
    """

@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: HousePredictionInput = HousePredictionInput()):
    """Make a house price prediction based on input features"""
    try:
        # Make prediction (model output is in hundreds of thousands)
        pred = model.predict([input_data.data])
        prediction_value = float(pred[0])
        
        # Convert to actual dollar amount (multiply by 100,000)
        actual_price = prediction_value * 100000
        
        return PredictionResponse(
            prediction=prediction_value,
            prediction_formatted=f"${actual_price:,.2f}"
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": True}

# Gradio interface function
def predict_house_price(med_inc, house_age, ave_rooms, ave_bedrms, population, ave_occup, latitude, longitude):
    """Function for Gradio interface"""
    try:
        # Prepare input data
        input_features = [med_inc, house_age, ave_rooms, ave_bedrms, population, ave_occup, latitude, longitude]
        
        # Make prediction
        pred = model.predict([input_features])
        prediction_value = float(pred[0])
        
        # Convert to actual dollar amount
        actual_price = prediction_value * 100000
        
        return f"${actual_price:,.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=predict_house_price,
    inputs=[
        gr.Number(label="Median Income (in tens of thousands)", value=8.3252, precision=4),
        gr.Number(label="House Age (years)", value=41.0, precision=1),
        gr.Number(label="Average Rooms per Household", value=6.98, precision=2),
        gr.Number(label="Average Bedrooms per Household", value=1.02, precision=2),
        gr.Number(label="Population", value=322.0, precision=0),
        gr.Number(label="Average Occupancy", value=2.55, precision=2),
        gr.Number(label="Latitude", value=37.88, precision=2),
        gr.Number(label="Longitude", value=-122.23, precision=2),
    ],
    outputs=gr.Textbox(label="Predicted House Price"),
    title="🏠 California House Price Predictor",
    description="""
    This app predicts house prices based on California housing data features.
    
    **Features:**
    - **Median Income**: Median income in block group (in tens of thousands)
    - **House Age**: Median house age in block group 
    - **Ave Rooms**: Average number of rooms per household
    - **Ave Bedrooms**: Average number of bedrooms per household
    - **Population**: Block group population
    - **Ave Occupancy**: Average number of household members
    - **Latitude**: Latitude coordinate
    - **Longitude**: Longitude coordinate
    
    *Try the default values or modify them to see different predictions!*
    """,
    examples=[
        [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23],
        [5.6431, 9.0, 7.85, 1.13, 485.0, 2.16, 33.60, -117.88],
        [3.2317, 34.0, 5.82, 1.06, 1977.0, 3.44, 36.06, -119.01],
    ]
)

# Mount Gradio app
app = gr.mount_gradio_app(app, iface, path="/gradio")

if __name__ == "__main__":
    print("🏠 Starting House Price Prediction API...")
    print("📊 Model loaded successfully!")
    
    # Get port from environment variable (Render sets this automatically)
    port = int(os.getenv("PORT", 10000))
    
    print(f"🌐 FastAPI docs will be at: /docs")
    print(f"🎯 Gradio UI will be at: /gradio")
    
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=port)