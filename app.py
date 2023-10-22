import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load your dataset
data = pd.read_csv('data.csv')

# Read the list of job roles from roles.txt
with open('roles.txt', 'r') as file:
    job_roles = [line.strip() for line in file]

# Set a title for your app
st.title("AI Job Threat Index App")

# Create a selectbox with a default value of "Select a Job Role"
selected_job = st.selectbox("Select a Job Role", ["Select a Job Role"] + job_roles)

# Define the threat level color ranges
color_ranges = [(0, 25, "green"), (26, 55, "yellow"), (56, 75, "orange"), (76, 100, "red")]

# Check if a job role is selected
if selected_job != "Select a Job Role":
    # Filter the dataset based on the selected job role
    job_data = data[data['Job titles'].str.contains(selected_job, case=False)]

    if not job_data.empty:
        # Display the threat level for the selected job role
        threat_level = job_data['AI Impact'].values[0]  # Assuming 'AI Impact' is the threat level column
        threat_level = int(threat_level.strip('%'))
        st.write(f"### Threat Level")
        
        # Determine the color based on the threat level range
        color = "gray"  # Default color
        for start, end, col in color_ranges:
            if start <= threat_level <= end:
                color = col
        
        # Angular Gauge Chart (for numerical threat level)
        fig = go.Figure(go.Indicator(
            value=threat_level,
            title="Threat Level",
            mode="gauge+number",
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': color}}
        ))
        fig.update_layout(height=350)
        st.plotly_chart(fig)



    else:
        st.write(f"No data found for '{selected_job}'. Please try a different job role.")
