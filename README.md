# 🏠 House Price Prediction Web App

A complete AI web application that predicts California house prices using machine learning, built with **FastAPI** and **Gradio**.

## 🌟 Features

- ✅ **FastAPI Backend** - RESTful API with automatic documentation
- ✅ **Interactive Gradio UI** - User-friendly web interface  
- ✅ **Machine Learning Model** - Trained on California housing dataset
- ✅ **Docker Ready** - Easy deployment to any cloud platform
- ✅ **Free Deployment** - Deploy to Render.com at no cost

## 🚀 Live Demo

- **API Documentation**: http://localhost:10000/docs
- **Interactive UI**: http://localhost:10000/gradio
- **API Endpoint**: http://localhost:10000/predict

## 📁 Project Structure

```
house-price-app/
├── main.py              # FastAPI + Gradio application
├── requirements.txt     # Python dependencies
├── house_model.pkl      # Trained ML model
├── create_model.py      # Script to generate the model
├── test_api.py          # API testing script
└── README.md           # This file
```

## 🛠️ Local Setup

### 1. Clone or Download

```bash
cd C:\house-price-app
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python main.py
```

### 4. Access the Application

- **Main Page**: http://localhost:10000
- **API Docs**: http://localhost:10000/docs  
- **Gradio UI**: http://localhost:10000/gradio

## 📊 API Usage

### Prediction Endpoint

**POST** `/predict`

```json
{
  "data": [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
}
```

**Response:**
```json
{
  "prediction": 4.526,
  "prediction_formatted": "$452,600.00"
}
```

### Features Explanation

The model expects 8 features (California Housing Dataset):

1. **MedInc**: Median income in block group (in tens of thousands)
2. **HouseAge**: Median house age in block group 
3. **AveRooms**: Average number of rooms per household
4. **AveBedrms**: Average number of bedrooms per household  
5. **Population**: Block group population
6. **AveOccup**: Average number of household members
7. **Latitude**: Latitude coordinate
8. **Longitude**: Longitude coordinate

## 🌐 Deploy to Render.com

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - House Price Prediction API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/house-price-api.git
git push -u origin main
```

### 2. Deploy on Render

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `house-price-predictor`
   - **Runtime**: `Python 3`
   - **Build Command**: (leave blank)
   - **Start Command**: `uvicorn main:app --host=0.0.0.0 --port=10000`
   - **Instance Type**: Free
5. Click **"Deploy"**

### 3. Your App Will Be Live At:
```
https://house-price-predictor.onrender.com
```

## 🧪 Testing

Run the test script to verify everything works:

```bash
python test_api.py
```

## 📦 Model Information

- **Algorithm**: Linear Regression
- **Dataset**: California Housing (sklearn)
- **Features**: 8 numerical features
- **Target**: House prices in hundreds of thousands
- **Performance**: ~57% R² score on test data

## 🔧 Customization

### Change the Model

Replace `house_model.pkl` with your own trained model:

```python
import joblib
# Train your model
model = YourModel()
# Save it
joblib.dump(model, "house_model.pkl")
```

### Modify Features

Update the input schema in `main.py`:

```python
class HousePredictionInput(BaseModel):
    data: Optional[List[float]] = [your_default_values]
```

### Update UI

Customize the Gradio interface by modifying the `inputs` parameter in `main.py`.

## 🤝 Contributing

Feel free to submit issues and pull requests!

## 📄 License

MIT License - feel free to use for any project.

---

**Built with ❤️ using FastAPI, Gradio, and scikit-learn**