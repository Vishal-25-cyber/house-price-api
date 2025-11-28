# Script to create the trained house price prediction model
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

# Load the California housing dataset
print("Loading California housing dataset...")
X, y = fetch_california_housing(return_X_y=True)

# Display dataset info
print(f"Dataset shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Features: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
print("Training Linear Regression model...")
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"Training R² score: {train_score:.4f}")
print(f"Testing R² score: {test_score:.4f}")

# Make a sample prediction
sample_data = [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
sample_prediction = model.predict([sample_data])
print(f"Sample prediction for {sample_data}: ${sample_prediction[0]*100000:.2f}")

# Save the trained model
print("Saving model to house_model.pkl...")
joblib.dump(model, "house_model.pkl")
print("Model saved successfully!")