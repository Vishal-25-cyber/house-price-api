# Script to create a simple house price prediction model without scikit-learn
import joblib
import numpy as np

class SimpleHousePriceModel:
    """Simple linear regression model without scikit-learn dependency"""
    
    def __init__(self):
        # Pre-trained coefficients based on California housing data analysis
        # Features: MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
        self.coefficients = np.array([
            0.4379,   # MedInc - most important
            0.0094,   # HouseAge  
            -0.1073,  # AveRooms
            0.6451,   # AveBedrms
            -0.0000042,  # Population (very small effect)
            -0.0377,  # AveOccup
            -0.4213,  # Latitude
            -0.4345   # Longitude
        ])
        self.intercept = 1.8856  # Adjusted for proper scale
        
    def predict(self, X):
        """Make predictions using linear combination"""
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        predictions = np.dot(X, self.coefficients) + self.intercept
        return predictions
    
    def score(self, X, y):
        """Calculate R² score"""
        predictions = self.predict(X)
        ss_res = np.sum((y - predictions) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot)

# Create and save the model
print("Creating simple house price prediction model...")
model = SimpleHousePriceModel()

# Test with sample data
sample_data = [8.3252, 41.0, 6.98, 1.02, 322.0, 2.55, 37.88, -122.23]
sample_prediction = model.predict([sample_data])
print(f"Sample prediction for {sample_data}: ${sample_prediction[0]*100000:.2f}")

# Save the model
print("Saving model to house_model.pkl...")
joblib.dump(model, "house_model.pkl")
print("Model saved successfully!")
print("✅ No scikit-learn dependency required!")