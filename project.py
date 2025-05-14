"XXXX"
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import expon
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt





st.title("BSTA040 Final Project")
st.subheader("Lela Boermeester")
st.subheader("Looking at Influenza cases from 2010-2025")
ili_data = pd.read_csv("ilidata.csv")
ili_data = ili_data.sort_values("epiweek")
ili_data =ili_data.reset_index(drop=True)
weeks=[]
for i in range(len(ili_data)):
    w = i // 51
    weeks.append(w)
ili_data["weeks"]= weeks
choice = st.selectbox("Select a State", ili_data['state'].unique())
ili_data_state_choice = ili_data[ili_data["state"] == choice]
st.line_chart(data=ili_data_state_choice, x="weeks", y="ili", x_label = "Time in Weeks", y_label ="ILI %")
st.caption("Pictured above is a graph that uses Influenza data from 2010-2025 to show the unweighted percentage of patient visits in each state for influenza-like illnesses. The unweighted percentage is calculated by taking the number of influenza-like illness cases and dividing it by the total number of patient visits, multiplied by 100. The x-axis, “Time in Weeks”,  consists of time in weeks starting in 2010 at week 40 (Week 1) to 2025 week 16 (Week 766). The y-axis, ILI %, represents the unweighted percentage we discussed above. The graph will represent the state selected in the dropdown above and only data from that state. From the graph we can identify periodic peaks, followed by luls, which coincide with seasonal outbreaks of influenza. The peaks represent spikes or outbreaks of influenza-like illnesses that range in severity.")
ili_values_all = ili_data["ili"].dropna()
ili_values = ili_data_state_choice["ili"].dropna()
mean_val = ili_values_all.mean()
lambda_h = 1 / mean_val
x_d = np.linspace(0,ili_values_all.max(), 200)
pdf = lambda_h * np.exp(-lambda_h *x_d)

fig,ax = plt.subplots(figsize=(8,5))
ax.hist(ili_values, density = True, alpha=0.6, label ="ILI Histogram")
ax.plot(x_d,pdf, label = "Exponential PDF", color = "red")
ax.set_xlabel("ILI %")
ax.set_ylabel("Density")
ax.set_title("ILI Histogram w/ Distribution Overlay")
ax.legend()
ax.grid(True)

st.pyplot(fig)
st.markdown("The graph above is a histogram that displays the density of the percentage of influenza-like illnesses. The histogram changes based on the state selected, only displaying the data for that specific state. It visualizes the distribution of ILI % in the population. It is overlaid by a red line which is an estimated exponential distribution based on data from all data across 50 states. The distribution assumes that all of the ILI values were drawn independently from the same distribution. Lambda “hat” which is used in the exponential distribution in the y-value for the overlay is 1 over the average value of the ILI %. The line represents the probability density function of the distribution, which allows us to compare the recorded observations to a theoretical distribution.  Majority of the values are concentrated towards the beginning of the distribution across all states, which tells us that it is more common to see lower percentages of  influenza-like illnesses. The exponential follows a similar path starting at a high density and steeply declining and continuing to taper off as the x-values increase. This displays that the exponential distribution has potential to be a pretty good fit for the data, although there is room for improvement.")

