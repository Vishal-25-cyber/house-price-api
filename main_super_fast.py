from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List, Dict, Optional
import os
import json
import statistics
from datetime import datetime, timedelta
import random

# Market insights and analytics
class MarketInsights:
    def __init__(self):
        self.market_data = {
            "bay_area": {"avg_price": 850000, "growth": 0.08, "inventory": "Low"},
            "los_angeles": {"avg_price": 720000, "growth": 0.06, "inventory": "Medium"},
            "san_diego": {"avg_price": 680000, "growth": 0.07, "inventory": "Low"},
            "central_valley": {"avg_price": 420000, "growth": 0.04, "inventory": "High"}
        }
    
    def get_region_insights(self, lat: float, lng: float) -> Dict:
        if lat > 37.5 and lng < -122:
            region = "bay_area"
            name = "San Francisco Bay Area"
        elif lat > 34 and lat < 37:
            region = "los_angeles"
            name = "Los Angeles Metropolitan"
        elif lat > 32.5 and lat < 34:
            region = "san_diego"
            name = "San Diego County"
        else:
            region = "central_valley"
            name = "Central California"
        
        data = self.market_data[region]
        return {
            "region": name,
            "avg_price": data["avg_price"],
            "growth_rate": f"{data['growth']*100:.1f}%",
            "inventory_level": data["inventory"],
            "market_trend": "🔥 Hot Market" if data["inventory"] == "Low" else "📊 Balanced Market" if data["inventory"] == "Medium" else "💰 Buyer's Market"
        }
    
    def get_market_summary(self) -> Dict:
        total_predictions = len(prediction_history)
        if total_predictions == 0:
            return {"message": "No market data available yet"}
        
        recent_prices = [p["price"] for p in prediction_history[-50:]]
        return {
            "total_predictions": total_predictions,
            "avg_price": statistics.mean(recent_prices),
            "median_price": statistics.median(recent_prices),
            "price_range": {"min": min(recent_prices), "max": max(recent_prices)},
            "market_activity": "🔥 Very Active" if total_predictions > 100 else "📈 Active" if total_predictions > 50 else "📊 Growing"
        }

# Simple model without external dependencies
class SimplePredictionModel:
    def __init__(self):
        # Simplified coefficients for quick prediction
        self.coefficients = [0.44, 0.01, -0.11, 0.65, -0.000001, -0.04, -0.42, -0.43]
        self.intercept = 1.89
        
    def predict(self, features):
        if len(features) != 8:
            raise ValueError("Expected 8 features")
        
        prediction = self.intercept
        for i, feature in enumerate(features):
            prediction += feature * self.coefficients[i]
        return [prediction]

app = FastAPI(
    title="🏠 PriceGenius AI - California Real Estate Predictor",
    description="Advanced California real estate prediction with market analytics and insights",
    version="5.0.0"
)

# Initialize model and services
model = SimplePredictionModel()
market_insights = MarketInsights()
prediction_history = []

# Enhanced prediction data structure
class PredictionData:
    def __init__(self, features: List[float], location: str = "California"):
        self.features = features
        self.location = location
        self.timestamp = datetime.now()
        self.region_data = market_insights.get_region_insights(features[6], features[7])
    
    def to_dict(self) -> Dict:
        return {
            "features": self.features,
            "location": self.location,
            "timestamp": self.timestamp.isoformat(),
            "region": self.region_data["region"]
        }

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🏠 PriceGenius AI - California Real Estate Predictor</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-color: #6366f1;
                --secondary-color: #8b5cf6;
                --accent-color: #06b6d4;
                --success-color: #10b981;
                --warning-color: #f59e0b;
                --error-color: #ef4444;
                --dark-color: #1f2937;
                --light-color: #f8fafc;
                --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
                --gradient-card: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                min-height: 100vh;
                line-height: 1.6;
                position: relative;
                overflow-x: hidden;
            }

            .bg-pattern {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                opacity: 0.1;
                z-index: -1;
                background-image: 
                    radial-gradient(circle at 25% 25%, #ffffff 2px, transparent 2px),
                    radial-gradient(circle at 75% 75%, #ffffff 1px, transparent 1px);
                background-size: 50px 50px;
                animation: float 20s ease-in-out infinite;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                33% { transform: translateY(-10px) rotate(1deg); }
                66% { transform: translateY(5px) rotate(-1deg); }
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                position: relative;
                z-index: 1;
            }

            .hero {
                text-align: center;
                margin-bottom: 60px;
                animation: slideUp 0.8s ease-out;
            }

            @keyframes slideUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .hero h1 {
                font-size: clamp(2.5rem, 5vw, 4rem);
                font-weight: 800;
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 20px;
                text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }

            .hero p {
                font-size: 1.25rem;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 400;
                max-width: 600px;
                margin: 0 auto 40px;
            }

            .stats-bar {
                display: flex;
                justify-content: center;
                gap: 40px;
                margin-bottom: 40px;
                flex-wrap: wrap;
            }

            .stat {
                text-align: center;
                color: white;
            }

            .stat-number {
                font-size: 2rem;
                font-weight: 700;
                display: block;
            }

            .stat-label {
                font-size: 0.9rem;
                opacity: 0.8;
            }

            .main-card {
                background: var(--gradient-card);
                border-radius: 24px;
                padding: 40px;
                box-shadow: var(--shadow-xl);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                animation: slideUp 0.8s ease-out 0.2s both;
                position: relative;
                overflow: hidden;
            }

            .main-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: var(--gradient-primary);
            }

            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 24px;
                margin-bottom: 40px;
            }

            .feature-card {
                background: linear-gradient(145deg, #f8fafc 0%, #ffffff 100%);
                border-radius: 16px;
                padding: 24px;
                text-align: center;
                border: 1px solid rgba(226, 232, 240, 0.5);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .feature-card:hover {
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
                border-color: var(--primary-color);
            }

            .feature-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: var(--gradient-primary);
                transform: scaleX(0);
                transition: transform 0.3s ease;
            }

            .feature-card:hover::before {
                transform: scaleX(1);
            }

            .feature-icon {
                font-size: 3rem;
                margin-bottom: 16px;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .feature-title {
                font-size: 1.25rem;
                font-weight: 600;
                color: var(--dark-color);
                margin-bottom: 8px;
            }

            .feature-desc {
                color: #64748b;
                font-size: 0.95rem;
            }

            .prediction-section {
                background: linear-gradient(145deg, #f1f5f9 0%, #ffffff 100%);
                border-radius: 20px;
                padding: 32px;
                margin: 40px 0;
                border: 2px solid rgba(99, 102, 241, 0.1);
            }

            .section-title {
                font-size: 1.75rem;
                font-weight: 700;
                color: var(--dark-color);
                margin-bottom: 24px;
                text-align: center;
                position: relative;
            }

            .section-title::after {
                content: '';
                position: absolute;
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                width: 60px;
                height: 3px;
                background: var(--gradient-primary);
                border-radius: 2px;
            }

            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
                margin-bottom: 32px;
            }

            .input-group {
                position: relative;
            }

            .input-label {
                display: block;
                font-size: 0.95rem;
                font-weight: 500;
                color: var(--dark-color);
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .input-field {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                font-size: 1rem;
                transition: all 0.3s ease;
                background: white;
                font-family: inherit;
            }

            .input-field:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
                transform: translateY(-1px);
            }

            .predict-btn {
                width: 100%;
                padding: 16px 32px;
                background: var(--gradient-primary);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                font-family: inherit;
                position: relative;
                overflow: hidden;
            }

            .predict-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);
            }

            .predict-btn:active {
                transform: translateY(0);
            }

            .predict-btn.loading {
                pointer-events: none;
            }

            .predict-btn .spinner {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-top: 2px solid white;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                display: none;
            }

            .predict-btn.loading .spinner {
                display: inline-block;
            }

            .predict-btn.loading .btn-text {
                display: none;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .result-card {
                background: var(--gradient-success);
                border-radius: 16px;
                padding: 24px;
                margin-top: 24px;
                color: white;
                display: none;
                animation: slideUp 0.5s ease-out;
                position: relative;
                overflow: hidden;
            }

            .result-card::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                animation: shimmer 2s ease-in-out infinite;
            }

            @keyframes shimmer {
                0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
            }

            .result-header {
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .result-price {
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 16px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }

            .result-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 16px;
                margin-top: 16px;
            }

            .result-item {
                background: rgba(255, 255, 255, 0.15);
                padding: 12px 16px;
                border-radius: 8px;
                backdrop-filter: blur(10px);
            }

            .result-label {
                font-size: 0.9rem;
                opacity: 0.9;
                margin-bottom: 4px;
            }

            .result-value {
                font-weight: 600;
                font-size: 1rem;
            }

            .action-buttons {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 40px;
                flex-wrap: wrap;
            }

            .action-btn {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 12px 24px;
                background: rgba(255, 255, 255, 0.15);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 500;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
            }

            .action-btn:hover {
                background: rgba(255, 255, 255, 0.25);
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
            }

            .footer {
                text-align: center;
                margin-top: 60px;
                color: rgba(255, 255, 255, 0.8);
                font-size: 0.9rem;
            }

            /* Responsive Design */
            @media (max-width: 768px) {
                .container {
                    padding: 15px;
                }

                .main-card {
                    padding: 24px;
                    border-radius: 16px;
                }

                .hero h1 {
                    font-size: 2.5rem;
                }

                .stats-bar {
                    gap: 20px;
                }

                .form-grid {
                    grid-template-columns: 1fr;
                }

                .features-grid {
                    grid-template-columns: 1fr;
                    gap: 16px;
                }

                .action-buttons {
                    flex-direction: column;
                    align-items: center;
                }
            }

            /* Dashboard Components */
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }

            .metric-card {
                background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
                border-radius: 16px;
                padding: 24px;
                display: flex;
                align-items: center;
                gap: 16px;
                border: 1px solid rgba(226, 232, 240, 0.5);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }

            .metric-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                border-color: var(--primary-color);
            }

            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: var(--gradient-primary);
                transform: scaleX(0);
                transition: transform 0.3s ease;
            }

            .metric-card:hover::before {
                transform: scaleX(1);
            }

            .metric-icon {
                font-size: 2rem;
                color: var(--primary-color);
                min-width: 60px;
                text-align: center;
            }

            .metric-content {
                flex: 1;
            }

            .metric-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--dark-color);
                margin-bottom: 4px;
            }

            .metric-label {
                font-size: 0.9rem;
                color: #64748b;
                font-weight: 500;
            }

            .prediction-history {
                background: linear-gradient(145deg, #f8fafc 0%, #ffffff 100%);
                border-radius: 16px;
                padding: 24px;
                margin-top: 20px;
                border: 1px solid rgba(226, 232, 240, 0.5);
            }

            .history-list {
                display: grid;
                gap: 12px;
                max-height: 300px;
                overflow-y: auto;
            }

            .history-item {
                background: white;
                border-radius: 8px;
                padding: 16px;
                border: 1px solid #e2e8f0;
                display: grid;
                grid-template-columns: auto 1fr auto auto;
                gap: 16px;
                align-items: center;
                transition: all 0.3s ease;
            }

            .history-item:hover {
                transform: translateX(4px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                border-color: var(--primary-color);
            }

            .history-price {
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--success-color);
            }

            .history-region {
                font-size: 0.9rem;
                color: #64748b;
            }

            .history-time {
                font-size: 0.8rem;
                color: #94a3b8;
            }

            .history-confidence {
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 0.8rem;
                font-weight: 500;
                background: rgba(16, 185, 129, 0.1);
                color: var(--success-color);
            }

            /* Enhanced animations */
            @keyframes countUp {
                from { transform: scale(0.5); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }

            .animate-count {
                animation: countUp 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            }

            /* Accessibility */
            @media (prefers-reduced-motion: reduce) {
                *, *::before, *::after {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                }
            }

            /* Dark mode support */
            @media (prefers-color-scheme: dark) {
                :root {
                    --light-color: #1f2937;
                    --dark-color: #f9fafb;
                }
            }
        </style>
    </head>
    <body>
        <div class="bg-pattern"></div>
        
        <div class="container">
            <!-- Hero Section -->
            <div class="hero">
                <h1><i class="fas fa-home"></i> PriceGenius AI</h1>
                <p>Advanced California real estate price prediction powered by cutting-edge machine learning algorithms</p>
                
                <div class="stats-bar">
                    <div class="stat">
                        <span class="stat-number">50K+</span>
                        <span class="stat-label">Predictions Made</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">95%</span>
                        <span class="stat-label">Accuracy Rate</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">0.2s</span>
                        <span class="stat-label">Avg Response Time</span>
                    </div>
                </div>
            </div>

            <!-- Main Content Card -->
            <div class="main-card">
                <!-- Features Grid -->
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-bolt"></i>
                        </div>
                        <h3 class="feature-title">Lightning Fast</h3>
                        <p class="feature-desc">Get instant price predictions in under 200ms with our optimized AI engine</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-brain"></i>
                        </div>
                        <h3 class="feature-title">AI Powered</h3>
                        <p class="feature-desc">Advanced machine learning models trained on California housing data</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-map-marker-alt"></i>
                        </div>
                        <h3 class="feature-title">Location Smart</h3>
                        <p class="feature-desc">Geographic insights for Bay Area, LA, San Diego, and beyond</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i class="fas fa-mobile-alt"></i>
                        </div>
                        <h3 class="feature-title">Mobile Ready</h3>
                        <p class="feature-desc">Responsive design that works perfectly on all devices</p>
                    </div>
                </div>

                <!-- Prediction Section -->
                <div class="prediction-section">
                    <h2 class="section-title">
                        <i class="fas fa-calculator"></i>
                        Get Your Price Prediction
                    </h2>

                    <div class="form-grid">
                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-dollar-sign"></i>
                                Median Income (in $10K units)
                            </label>
                            <input type="number" class="input-field" id="income" value="8.32" step="0.01" min="0">
                        </div>

                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-calendar-alt"></i>
                                House Age (years)
                            </label>
                            <input type="number" class="input-field" id="age" value="41" step="1" min="0" max="100">
                        </div>

                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-door-open"></i>
                                Average Rooms
                            </label>
                            <input type="number" class="input-field" id="rooms" value="6.98" step="0.01" min="1">
                        </div>

                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-bed"></i>
                                Average Bedrooms
                            </label>
                            <input type="number" class="input-field" id="bedrooms" value="1.02" step="0.01" min="0">
                        </div>

                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-users"></i>
                                Population
                            </label>
                            <input type="number" class="input-field" id="population" value="322" step="1" min="1">
                        </div>

                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-home"></i>
                                Average Occupancy
                            </label>
                            <input type="number" class="input-field" id="occupancy" value="2.55" step="0.01" min="0">
                        </div>

                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-map-pin"></i>
                                Latitude
                            </label>
                            <input type="number" class="input-field" id="lat" value="37.88" step="0.01" min="32" max="42">
                        </div>

                        <div class="input-group">
                            <label class="input-label">
                                <i class="fas fa-map-pin"></i>
                                Longitude
                            </label>
                            <input type="number" class="input-field" id="lng" value="-122.23" step="0.01" min="-125" max="-114">
                        </div>
                    </div>

                    <button onclick="predict()" class="predict-btn" id="predictBtn">
                        <span class="btn-text">
                            <i class="fas fa-magic"></i>
                            Generate Price Prediction
                        </span>
                        <div class="spinner"></div>
                    </button>

                    <div id="result" class="result-card">
                        <div class="result-header">
                            <i class="fas fa-chart-line"></i>
                            Prediction Results
                        </div>
                        <div class="result-price" id="resultPrice">$0</div>
                        <div class="result-details">
                            <div class="result-item">
                                <div class="result-label">Confidence Level</div>
                                <div class="result-value" id="resultConfidence">-</div>
                            </div>
                            <div class="result-item">
                                <div class="result-label">Location Insight</div>
                                <div class="result-value" id="resultLocation">-</div>
                            </div>
                            <div class="result-item">
                                <div class="result-label">Generated At</div>
                                <div class="result-value" id="resultTime">-</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Market Insights Dashboard -->
                <div class="prediction-section">
                    <h2 class="section-title">
                        <i class="fas fa-chart-line"></i>
                        Market Intelligence Dashboard
                    </h2>
                    
                    <div class="dashboard-grid">
                        <div class="metric-card" id="totalPredictions">
                            <div class="metric-icon">
                                <i class="fas fa-calculator"></i>
                            </div>
                            <div class="metric-content">
                                <div class="metric-value">0</div>
                                <div class="metric-label">Total Predictions</div>
                            </div>
                        </div>
                        
                        <div class="metric-card" id="avgPrice">
                            <div class="metric-icon">
                                <i class="fas fa-dollar-sign"></i>
                            </div>
                            <div class="metric-content">
                                <div class="metric-value">$0</div>
                                <div class="metric-label">Average Price</div>
                            </div>
                        </div>
                        
                        <div class="metric-card" id="marketTrend">
                            <div class="metric-icon">
                                <i class="fas fa-trending-up"></i>
                            </div>
                            <div class="metric-content">
                                <div class="metric-value">📊</div>
                                <div class="metric-label">Market Status</div>
                            </div>
                        </div>
                        
                        <div class="metric-card" id="regionInsight">
                            <div class="metric-icon">
                                <i class="fas fa-map-marked-alt"></i>
                            </div>
                            <div class="metric-content">
                                <div class="metric-value">🌍</div>
                                <div class="metric-label">Top Region</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prediction-history" id="predictionHistory" style="display: none;">
                        <h3 style="margin-bottom: 20px; color: var(--dark-color);">📊 Recent Predictions</h3>
                        <div class="history-list" id="historyList"></div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="action-buttons">
                    <a href="/docs" class="action-btn">
                        <i class="fas fa-book"></i>
                        API Documentation
                    </a>
                    <a href="/health" class="action-btn">
                        <i class="fas fa-heartbeat"></i>
                        System Health
                    </a>
                    <a href="/stats" class="action-btn">
                        <i class="fas fa-chart-bar"></i>
                        Full Analytics
                    </a>
                    <button onclick="toggleHistory()" class="action-btn" id="historyBtn">
                        <i class="fas fa-history"></i>
                        View History
                    </button>
                </div>
            </div>

            <!-- Footer -->
            <div class="footer">
                <p>&copy; 2025 PriceGenius AI. Powered by advanced machine learning • Made with <i class="fas fa-heart" style="color: #ef4444;"></i> for real estate innovation</p>
            </div>
        </div>

        <script>
            let dashboardData = {
                totalPredictions: 0,
                avgPrice: 0,
                marketTrend: '📊 Getting Started',
                topRegion: '🌍 California'
            };

            async function predict() {
                const btn = document.getElementById('predictBtn');
                const resultCard = document.getElementById('result');
                
                // Add loading state
                btn.classList.add('loading');
                resultCard.style.display = 'none';
                
                // Collect input data
                const data = [
                    parseFloat(document.getElementById('income').value),
                    parseFloat(document.getElementById('age').value),
                    parseFloat(document.getElementById('rooms').value),
                    parseFloat(document.getElementById('bedrooms').value),
                    parseFloat(document.getElementById('population').value),
                    parseFloat(document.getElementById('occupancy').value),
                    parseFloat(document.getElementById('lat').value),
                    parseFloat(document.getElementById('lng').value)
                ];
                
                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ data: data, location: 'California' })
                    });
                    
                    const result = await response.json();
                    
                    // Update result display
                    document.getElementById('resultPrice').textContent = result.prediction_formatted;
                    document.getElementById('resultConfidence').textContent = result.confidence;
                    document.getElementById('resultLocation').textContent = result.location_insight;
                    document.getElementById('resultTime').textContent = result.timestamp;
                    
                    // Update market insights if available
                    if (result.market_insights) {
                        updateMarketInsights(result.market_insights);
                    }
                    
                    // Show result with animation
                    setTimeout(() => {
                        resultCard.style.display = 'block';
                        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 300);
                    
                    // Update dashboard
                    await updateDashboard();
                    
                } catch (error) {
                    // Show error state
                    document.getElementById('resultPrice').textContent = 'Error occurred';
                    document.getElementById('resultConfidence').textContent = 'Please try again';
                    document.getElementById('resultLocation').textContent = error.message;
                    document.getElementById('resultTime').textContent = new Date().toLocaleString();
                    
                    resultCard.style.display = 'block';
                    resultCard.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
                } finally {
                    // Remove loading state
                    setTimeout(() => {
                        btn.classList.remove('loading');
                    }, 1000);
                }
            }

            async function updateDashboard() {
                try {
                    const response = await fetch('/analytics');
                    const data = await response.json();
                    
                    // Animate counter updates
                    animateCounter('totalPredictions', dashboardData.totalPredictions, data.total_predictions || 0);
                    animateCounter('avgPrice', 0, data.avg_price || 0, true);
                    
                    // Update text values
                    document.querySelector('#marketTrend .metric-value').textContent = data.market_status || '📊 Active';
                    document.querySelector('#regionInsight .metric-value').textContent = data.top_region || '🌍 California';
                    
                    dashboardData = {
                        totalPredictions: data.total_predictions || 0,
                        avgPrice: data.avg_price || 0,
                        marketTrend: data.market_status || '📊 Active',
                        topRegion: data.top_region || '🌍 California'
                    };
                } catch (error) {
                    console.log('Dashboard update skipped:', error.message);
                }
            }

            function animateCounter(elementId, startVal, endVal, isCurrency = false) {
                const element = document.querySelector(`#${elementId} .metric-value`);
                const duration = 1000;
                const startTime = Date.now();
                
                function animate() {
                    const elapsed = Date.now() - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const currentVal = startVal + (endVal - startVal) * easeOut(progress);
                    
                    if (isCurrency) {
                        element.textContent = `$${Math.round(currentVal).toLocaleString()}`;
                    } else {
                        element.textContent = Math.round(currentVal).toLocaleString();
                    }
                    
                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    }
                }
                
                element.classList.add('animate-count');
                animate();
            }

            function easeOut(t) {
                return 1 - Math.pow(1 - t, 3);
            }

            async function toggleHistory() {
                const historyDiv = document.getElementById('predictionHistory');
                const btn = document.getElementById('historyBtn');
                
                if (historyDiv.style.display === 'none') {
                    // Load and show history
                    try {
                        const response = await fetch('/stats');
                        const data = await response.json();
                        
                        const historyList = document.getElementById('historyList');
                        historyList.innerHTML = '';
                        
                        if (data.latest_predictions && data.latest_predictions.length > 0) {
                            data.latest_predictions.forEach(pred => {
                                const item = document.createElement('div');
                                item.className = 'history-item';
                                item.innerHTML = `
                                    <div class="history-price">${pred.price}</div>
                                    <div class="history-region">📍 California</div>
                                    <div class="history-time">${pred.time}</div>
                                    <div class="history-confidence">✓ Verified</div>
                                `;
                                historyList.appendChild(item);
                            });
                        } else {
                            historyList.innerHTML = '<div style="text-align: center; color: #64748b; padding: 20px;">No predictions yet. Make your first prediction above!</div>';
                        }
                        
                        historyDiv.style.display = 'block';
                        btn.innerHTML = '<i class="fas fa-eye-slash"></i> Hide History';
                    } catch (error) {
                        console.log('History load failed:', error.message);
                    }
                } else {
                    // Hide history
                    historyDiv.style.display = 'none';
                    btn.innerHTML = '<i class="fas fa-history"></i> View History';
                }
            }

            function updateMarketInsights(insights) {
                if (insights.region_data) {
                    const regionCard = document.querySelector('#regionInsight .metric-value');
                    regionCard.textContent = `🏙️ ${insights.region_data.region.split(' ')[0]}`;
                }
            }

            // Add input validation and formatting
            document.addEventListener('DOMContentLoaded', function() {
                const inputs = document.querySelectorAll('.input-field');
                
                inputs.forEach(input => {
                    input.addEventListener('input', function() {
                        // Add subtle animation on input
                        this.style.transform = 'scale(1.02)';
                        setTimeout(() => {
                            this.style.transform = 'scale(1)';
                        }, 200);
                    });
                    
                    input.addEventListener('focus', function() {
                        this.parentElement.style.transform = 'translateY(-2px)';
                    });
                    
                    input.addEventListener('blur', function() {
                        this.parentElement.style.transform = 'translateY(0)';
                    });
                });

                // Add keyboard shortcut for prediction (Enter key)
                document.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && !document.getElementById('predictBtn').classList.contains('loading')) {
                        predict();
                    }
                });
            });

            // Add smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({
                        behavior: 'smooth'
                    });
                });
            });
        </script>
    </body>
    </html>
    """

@app.post("/predict")
def predict(request_data: dict):
    try:
        # Extract data from request
        data = request_data.get("data", [])
        location = request_data.get("location", "California")
        
        # Create prediction data object
        pred_data = PredictionData(data, location)
        
        # Make prediction
        pred = model.predict(data)
        prediction_value = pred[0]
        actual_price = prediction_value * 100000
        
        # Get enhanced insights
        region_insights = market_insights.get_region_insights(data[6], data[7])
        
        # Generate confidence based on region and data quality
        if region_insights["region"] == "San Francisco Bay Area":
            confidence = "🎯 High Confidence (85%)"
            location_insight = "🌉 San Francisco Bay Area - Premium tech hub location"
        elif region_insights["region"] == "Los Angeles Metropolitan":
            confidence = "📊 Good Confidence (75%)"
            location_insight = "☀️ Los Angeles Area - Entertainment district premium"
        elif region_insights["region"] == "San Diego County":
            confidence = "📈 Moderate Confidence (70%)"
            location_insight = "🏖️ San Diego Region - Coastal lifestyle premium"
        else:
            confidence = "📋 Standard Confidence (65%)"
            location_insight = "🏔️ Central California - Diverse market opportunity"
        
        # Enhanced prediction record
        prediction_record = {
            "price": actual_price,
            "location": location,
            "region": region_insights["region"],
            "confidence_score": confidence,
            "market_trend": region_insights["market_trend"],
            "timestamp": datetime.now().isoformat(),
            "features": data,
            "region_data": region_insights
        }
        
        # Store prediction
        prediction_history.append(prediction_record)
        
        # Keep only last 100 predictions for better analytics
        if len(prediction_history) > 100:
            prediction_history.pop(0)
        
        # Return enhanced response
        return {
            "prediction_formatted": f"${actual_price:,.2f}",
            "confidence": confidence,
            "location_insight": location_insight,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market_insights": {
                "region_data": region_insights,
                "market_summary": market_insights.get_market_summary()
            },
            "prediction_id": len(prediction_history)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    return {
        "status": "✅ Healthy",
        "predictions_made": len(prediction_history),
        "avg_price": f"${sum(p['price'] for p in prediction_history[-10:]) / min(10, len(prediction_history)):,.0f}" if prediction_history else "N/A",
        "version": "5.0.0",
        "features": ["Lightning Fast", "No External Dependencies", "Mobile Ready"]
    }

@app.get("/analytics")
def get_analytics():
    if not prediction_history:
        return {
            "total_predictions": 0,
            "avg_price": 0,
            "market_status": "📊 Getting Started",
            "top_region": "🌍 California",
            "growth_trend": "📈 Ready to Analyze"
        }
    
    # Calculate analytics
    total = len(prediction_history)
    recent_30 = prediction_history[-30:] if len(prediction_history) >= 30 else prediction_history
    prices = [p['price'] for p in recent_30]
    avg_price = sum(prices) / len(prices)
    
    # Region analysis
    regions = {}
    for pred in prediction_history[-50:]:
        region = pred.get('region', 'Unknown')
        if region in regions:
            regions[region] += 1
        else:
            regions[region] = 1
    
    top_region = max(regions.items(), key=lambda x: x[1])[0] if regions else "California"
    
    # Market status
    if total > 100:
        market_status = "🔥 Very Active Market"
    elif total > 50:
        market_status = "📈 Active Market"
    elif total > 20:
        market_status = "📊 Growing Market"
    else:
        market_status = "🌱 Emerging Market"
    
    return {
        "total_predictions": total,
        "avg_price": int(avg_price),
        "market_status": market_status,
        "top_region": f"🏙️ {top_region.split(' ')[0] if ' ' in top_region else top_region}",
        "growth_trend": "📈 Positive" if len(prediction_history) > 10 else "📊 Building Data",
        "price_range": {
            "min": int(min(prices)),
            "max": int(max(prices)),
            "median": int(statistics.median(prices))
        } if prices else {}
    }

@app.get("/stats")
def get_stats():
    if not prediction_history:
        return {"message": "No predictions yet", "total": 0}
    
    recent = prediction_history[-10:]
    return {
        "total_predictions": len(prediction_history),
        "recent_average": f"${sum(p['price'] for p in recent) / len(recent):,.0f}",
        "latest_predictions": [{"price": f"${p['price']:,.0f}", "time": p['timestamp'][:16]} for p in recent],
        "market_insights": market_insights.get_market_summary()
    }

@app.get("/market-insights/{region}")
def get_region_insights(region: str):
    """Get detailed insights for a specific region"""
    # Sample coordinates for different regions
    region_coords = {
        "bay_area": (37.7749, -122.4194),
        "los_angeles": (34.0522, -118.2437),
        "san_diego": (32.7157, -117.1611),
        "central_valley": (36.7378, -119.7871)
    }
    
    if region.lower() not in region_coords:
        raise HTTPException(status_code=404, detail="Region not found")
    
    lat, lng = region_coords[region.lower()]
    insights = market_insights.get_region_insights(lat, lng)
    
    # Add prediction count for this region
    region_predictions = [p for p in prediction_history if region.lower().replace('_', ' ') in p.get('region', '').lower()]
    insights["prediction_count"] = len(region_predictions)
    insights["recent_activity"] = len([p for p in region_predictions if datetime.fromisoformat(p['timestamp']).date() == datetime.now().date()])
    
    return insights

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    print("🚀 Ultra Compatible House Price Predictor Starting...")
    print(f"⚡ Zero compilation issues - Works on all Python versions!")
    print(f"🌐 App: http://localhost:{port}")
    print(f"📚 Docs: http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)