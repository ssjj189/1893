# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 15:22:30 2025

@author: Samar Mohapatra 2025 08110034 BKRKRTARWS
"""
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import ephem
import math

# Function to calculate lunar phase using ephem
def get_lunar_phase(date):
    """
    Calculates the lunar phase for a given date using ephem.

    Args:
        date: datetime object representing the date.

    Returns:
        A float value representing the lunar phase (0: New Moon, 0.5: Full Moon).
    """
    observer = ephem.Observer()
    observer.date = date.strftime("%Y/%m/%d")  # Format date for ephem
    moon = ephem.Moon()
    moon.compute(observer)
    phase = moon.phase / 100.0  # Convert phase from percentage to fraction
    return phase

# Generate sample data (replace with actual lunar cycle data)
start_date = datetime(2000, 1, 1)
end_date = datetime(4096, 12, 12)  # Adjust end date as needed
date_range = [start_date + timedelta(days=x) for x in range(0, (end_date - start_date).days)]
lunar_phases = [get_lunar_phase(date) for date in date_range]

# Create time data (year as a feature)
years = np.array([date.year for date in date_range]).reshape(-1, 1)

# **Simulate full moon probabilities**
# This simulates a sinusoidal trend with some noise 
amplitude = 0.2  # Amplitude of the sine wave
period = 11  # Approximate lunar cycle in years
noise_std = 0.05  # Standard deviation of noise
full_moon_probs = amplitude * np.sin(2 * np.pi * years / period) + np.random.normal(0, noise_std, size=years.shape)
full_moon_probs = np.clip(full_moon_probs, 0, 1)  # Ensure probabilities are within 0-1 range

# Create input data
input_data = np.concatenate((years, np.array(lunar_phases).reshape(-1, 1)), axis=1)

# Define hyperparameters
learning_rate = 0.01
training_epochs = 18

# Create TensorFlow model (functional API)
inputs = tf.keras.Input(shape=(2,))  # Input shape: (year, lunar_phase)
hidden = tf.keras.layers.Dense(1008, activation='relu')(inputs)  # Hidden layer with 10 neurons and ReLU activation
outputs = tf.keras.layers.Dense(1)(hidden)  # Output layer with 1 neuron

model = tf.keras.Model(inputs=inputs, outputs=outputs)

# Compile the model
model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate))
model.fit(input_data, full_moon_probs, epochs=training_epochs, batch_size=32, verbose=0)  # Suppress training output

# Predict probabilities for future years
future_start_date = datetime(2025, 1, 2)  # Start date for prediction
future_end_date = datetime(2030, 1, 1)
future_date_range = [future_start_date + timedelta(days=x) for x in range(0, (future_end_date - future_start_date).days)]
future_years = np.array([date.year for date in future_date_range]).reshape(-1, 1)
future_lunar_phases = [get_lunar_phase(date) for date in future_date_range]
future_input_data = np.concatenate((future_years, np.array(future_lunar_phases).reshape(-1, 1)), axis=1)
predicted_probs = model.predict(future_input_data)

# Plot the results
plt.figure(figsize=(10, 6))  # Adjust figure size for better readability
plt.plot(years, full_moon_probs, label='Actual', marker='o') 
plt.plot(future_years, predicted_probs.squeeze(), label='Predicted', marker='x')
plt.xlabel('Year')
plt.ylabel('Probability of Full Moon')
plt.title('Full Moon Probability Prediction')
plt.legend()
plt.grid(True)
plt.show()
