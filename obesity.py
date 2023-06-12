import hydralit_components as hc
from streamlit_option_menu import option_menu
import streamlit as st
from streamlit_lottie import st_lottie
import json
import pandas as pd
import plotly.offline as py
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import init_notebook_mode
init_notebook_mode(connected = True)
import base64
import os
import cufflinks as cf
from plotly.subplots import make_subplots
cf.go_offline()

st.set_page_config(layout = 'wide')

@st.cache
def load_data():
    df_data = pd.read_csv("data/data.csv")
    df_obesity = pd.read_csv("data/obesity.csv")
    df_obesityByContinent = pd.read_csv("data/obesityByContinent.csv")
    return df_data,df_obesity,df_obesityByContinent

# Load the Data
data,obesity,obesityByContinent = load_data()

def calculate_bmi(weight_kg, height_cm):
    bmi = weight_kg/((height_cm/100)**2)
    if bmi < 16:
        bmi_category = "Severe Thinness"
    elif (bmi >=16) &  (bmi <17):
        bmi_category = "Moderate Thinness"
    elif (bmi >=17) &  (bmi <18.5):
        bmi_category = "Mild Thinness"  
    elif (bmi >=18.5) &  (bmi <25):       
        bmi_category = "Normal"
    elif (bmi >=25) &  (bmi <30):       
       bmi_category = "Overweight"       
    elif (bmi >=30) &  (bmi <35):
        bmi_category = "Obese Class I"  
    elif (bmi >=35) &  (bmi <40):       
        bmi_category = "Obese Class II"
    elif (bmi >=40):       
       bmi_category = "Obese Class III"
    return bmi, bmi_category

#------------------------------------------------------------------------------------#
# Main page

#icons next to title
# File paths to the icons
icon1_path = "C:\\Users\\malak\\OneDrive\\Desktop\\obesity-main\\body-mass-index1.png"
icon2_path = "C:\\Users\\malak\\OneDrive\\Desktop\\obesity-main\\body-mass-index.png"

# Read the icons as bytes
with open(icon1_path, "rb") as icon1_file:
    icon1_bytes = icon1_file.read()
with open(icon2_path, "rb") as icon2_file:
    icon2_bytes = icon2_file.read()

# Encode the icons as base64 strings
icon1_base64 = base64.b64encode(icon1_bytes).decode("utf-8")
icon2_base64 = base64.b64encode(icon2_bytes).decode("utf-8")

# Creating a row layout for the icons and the title
col1, col2, col3 = st.columns([9, 1, 1])

# Displaying the title
col1.title("Obesity")

# Displaying the first icon
col2.markdown(f'<img src="data:image/png;base64,{icon1_base64}" alt="Icon 1" width="50">', unsafe_allow_html=True)

# Displaying the second icon
col3.markdown(f'<img src="data:image/png;base64,{icon2_base64}" alt="Icon 2" width="50">', unsafe_allow_html=True)

#------------------------------------------------------------------------------------------------------------------#
# Menu bar
selected = option_menu(
    menu_title=None,
    options=["Home","Obesity by Gender", "Global Obesity","Top 20 Countries", "BMI Calculator"],
    menu_icon="cast",
    icons=['house', 'globe', 'bar-chart', 'gear', 'pie-chart', 'calculator'],
    default_index=0,
    orientation="horizontal",
    styles={
        "nav-link-selected": {
            "background-color": "#fb9035",  # Color for the selected option
            "color": "white",  # Text color for the selected option
        },
        "nav": {
            "background-color": "#1585a4",  # Background color for the menu
            "padding": "10px",
            "border-radius": "10px",
        },
        "nav-link": {
            "color": "white",  # Text color for the menu options (switched to white)
            "font-size": "16px",  # Font size for the menu options
            "margin": "5px",
        },
    },
)
#----------------------------------------------------------------------------------------------------#
#Page 1 Home

import streamlit as st

if selected == "Home":
    col1 = st.columns(1)[0]

    with col1:
        # Information about obesity
        st.header("What is obesity?")
        st.markdown(
            """
            <div style='background-color: rgba(21, 133, 164, 0.5); color: black; padding: 10px; border-radius: 5px;'>
            <ul style='color: black; list-style-type: disc; padding-left: 20px;'>
            <li><b>Obesity is a medical condition characterized by excessive and unhealthy accumulation of body fat, resulting in an increased risk of various health problems. It is typically diagnosed based on body mass index (BMI) measurements that indicate a person's weight in relation to their height.</b></li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Complications of obesity
        st.header("Obesity Complications")
        st.markdown(
            """
            <div style='background-color: rgba(251, 144, 53, 0.5); color: black; padding: 10px; border-radius: 5px;'>
            <ul style='color: black; list-style-type: disc; padding-left: 20px;'>
            <li><b>Type 2 diabetes</b></li>
            <li><b>Cardiovascular Disease:</b></li>
            <li><b>Joint Problems</b></li>
            <li><b>Sleep Apnea</b></li>
            <li><b>High cholesterol</b></li>
            <li><b>High blood pressure</b></li>
            <li><b>Increased risk of certain cancers (such as breast, colorectal, and endometrial cancer)</b></li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Prevention of obesity
        st.header("Prevention")
        st.markdown(
            """
            <div style='background-color: rgba(21, 133, 164, 0.5); color: black; padding: 10px; border-radius: 5px;'>
            <ul style='color: black; list-style-type: disc; padding-left: 20px;'>
            <li><b>Maintain a balanced and healthy diet</b></li>
            <li><b>Engage in regular physical activity</b></li>
            <li><b>Limit consumption of sugary and high-fat foods</b></li>
            <li><b>Eat smaller portion sizes</b></li>
            <li><b>Avoid sedentary behaviors and aim for regular movement throughout the day</b></li>
            <li><b>Seek professional guidance and support when needed (e.g., from a healthcare provider or registered dietitian)</b></li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
#----------------------------------------------------------#
#Page 2 Obesity by gender

if selected == "Obesity by Gender":
    st.subheader("Gender-based Distribution of Mean Obesity Prevalence Among Adults")
    data1975_2015 = data.query("Year in [1975, 1995, 2016]")

    # Create box plot-- vis1
    box_fig = go.Figure()
    box_fig.add_trace(go.Box(
        x=data1975_2015["Year"],
        y=data1975_2015["Obesity"],
        name="Box Plot",
        boxmean=True,
        marker=dict(color="#FB9035") 
    ))

    # Create bar plot---vis2
    bar_fig = px.bar(
        data1975_2015,
        x="Year",
        y="Obesity",
        color="Sex",
        barmode="group",
        opacity=0.7,
        color_discrete_sequence=["#fb9035", "#1585a4", "#5c6474"]  # List of RGB values
    )

    # Create subplot figure with two columns
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Bar Plot", "Box Plot"), horizontal_spacing=0.05)

    # Add bar plot to the left subplot
    for trace in bar_fig.data:
        fig.add_trace(trace, row=1, col=1)

    # Add box plot to the right subplot
    fig.add_trace(box_fig.data[0], row=1, col=2)

    fig.update_layout(
        width=900,
        height=500,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    # Display the plots in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(bar_fig, use_container_width=True)

    with col2:
        st.plotly_chart(box_fig, use_container_width=True)
        
    st.markdown(
        """
        <div style='background-color: rgba(21, 133, 164, 0.5); color: black; padding: 10px; border-radius: 5px;'>
        <b>The prevalence rate of obesity among the total population (both sexes) has significantly increased from 1975 to 2015. Notably, it is evident that the rate of obesity among females has consistently remained higher than that observed among males.</b>
        </div>
        """,
        unsafe_allow_html=True
    )
#------------------------------------------------------------------------------------------------------------------------------------------------------#  
#Page 3 Global Obesity

# Define the sharper color palette
color_palette = px.colors.diverging.RdYlBu

# Page 2: Global Obesity
if selected == "Global Obesity":
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Visualization no. 3
        # Global Obesity Visualization
        st.subheader("Examining the Obesity Prevalence among adults by country from 1975 to 2016")
        fig = px.choropleth(obesity, locations="ISO3", color="Obesity", hover_name="Country", 
                            animation_frame="Year", color_continuous_scale=color_palette,
                            hover_data=["Year", "ISO3", "Obesity", "Population", "Obesity_count"],
                            range_color=[0, 45],
                            height=600, width=750,
                            labels={'Obesity': 'Obesity rate'},
                            projection="natural earth")
        st.write(fig)
    
    with col2:
        # Visualization no. 4
        st.subheader("Examining the Shift in Obesity Prevalence Among Adults across Continents, from 1975 to 2016.")
        fig = px.line(obesityByContinent, x="Year", y="WeightedObesity", color='Continent',
                      range_x=[1975, 2016], range_y=[0, 45], color_discrete_sequence=color_palette) 

        fig.update_layout(
            yaxis_title="Obesity Prevalence (%)",
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)")

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.write(fig)
    st.markdown(
            """
            <div style='background-color: rgba(21, 133, 164, 0.5); color: black; padding: 10px; border-radius: 5px;'>
            <b>We observe a concerning trend where the prevalence rates of obesity and overweight continue to escalate.</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        #st.info("**We observe a concerning trend where the prevalence rates of obesity and overweight continue to escalate.**")
#-------------------------------------------------#
# Page 4: Top 20 Countries
import streamlit as st
import plotly.graph_objects as go

if selected == "Top 20 Countries":
    # Visualization no. 5
    st.subheader(f"Top 20 Countries by Mean Obesity Prevalence Among Adults")
    sel_col, disp_col = st.columns([1, 4], gap="large")
    with sel_col:
        sel_year = st.slider("Select a year", min_value=1976, max_value=2016, value=2016, step=1, format="%d", key="my_slider")

        track_color = '#1585a4'

    with disp_col:
        obesity_for_selected_year = obesity.query("Year==" + str(sel_year)).sort_values(by='Obesity', ascending=False).head(20)
        
        # Customize the color of the bars in the bar chart
        bar_color = '#fb9035'
        
        fig = go.Figure(go.Bar(
            y=obesity_for_selected_year.Country,
            x=obesity_for_selected_year.Obesity,
            orientation='h',
            marker=dict(color=bar_color)  # Set the color of the bars
        ))

        fig.update_layout(
            title='Top 20 Countries by Mean Obesity Prevalence Among Adults in ' + str(sel_year),
            yaxis_title="Obesity Prevalence (%)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            width=800, height=500)

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig)

    st.markdown(
            """
            <div style='background-color: rgba(21, 133, 164, 0.5); color: black; padding: 10px; border-radius: 5px;'>
            <b>As the years progress, there is a noticeable correlation between the increase in time and the rise in obesity rates.</b>
            </div>
            """,
            unsafe_allow_html=True)
#-----------------------------------------------------------------------#
#Page 5: BMI Calculator

import streamlit as st
import plotly.graph_objects as go

if selected == "BMI Calculator":
    left_col, info_col, sel_col, disp_col, right_col = st.columns([.5, 3, 3, 3, 1], gap='large')

    with info_col:
        st.header("Obesity Categories")
        st.markdown(""" 
            |Category          |BMI range - kg/m2|
            |:-----------------|:----------------|
            |Severe Thinness   |< 16             |
            |Moderate Thinness |16 - 17          |
            |Mild Thinness     |17 - 18.5        |
            |Normal            |18.5 - 25        |
            |Overweight        |25 - 30          |
            |Obese Class I     |30 - 35          |
            |Obese Class II    |35 - 40          |
            |Obese Class III   |> 40             |
            """)

    with disp_col:
        st.header("Results")
        BMI_result = st.empty()
        msg = st.empty()

    with sel_col:
        st.header("BMI Calculator")     
        BMI_value = 0 
        height_cm = st.text_input('Height in cm')
        weight_kg = st.text_input("Weight in kg")
        if st.button("Calculate", key="calculate_button"):
            try:
                if (float(height_cm) <= 50):
                    raise Exception("Height must be over 50")
                height_cm = float(height_cm)
                weight_kg = float(weight_kg)
                BMI_value, bmi_category = calculate_bmi(weight_kg, height_cm)
                BMI_result.text_input('Your BMI Result', str(round(BMI_value, 2)) + ' kg/m2')
                if bmi_category == "Normal":
                    msg.success(bmi_category)
                elif bmi_category in ["Moderate Thinness", "Overweight"]:
                    msg.warning(bmi_category)
                elif bmi_category in ["Severe Thinness", "Obese Class I", "Obese Class II", "Obese Class III"]:
                    msg.error(bmi_category)
                else:
                    msg.write(bmi_category)

            except ZeroDivisionError:
                st.error("You can't divide by zero!")
            except ValueError:
                st.error('Height and weight must be numeric')
            except Exception as e:
                st.error(e)

    # CSS style for the calculate button
    st.markdown(
        """
        <style>
        .stButton button {
            background-color: #fb9035;
            color: #000000;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # CSS style for the result box
    st.markdown(
        """
        <style>
        .stTextInput div div input {
            background-color: #fb9035;
            color: #000000;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
