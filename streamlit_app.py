import streamlit as st
import pandas as pd
import pickle

df = pd.read_csv('cars-cleaned.csv', index_col='Id')

# set up page name, icon, layout and sidebar behaviour
st.set_page_config(
    page_title="Car Price Predictor App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# hide footer and main menu icon
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden;}
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)



# Add a sidebar to your Streamlit app
st.sidebar.markdown("<h1 style='text-align:center;color:gray;'><i>Car Price Prediction Options</i></h1>", unsafe_allow_html=True)
st.sidebar.write("")

# Define the list of possible locations sorted alphabetically
locations = sorted(df.Location.unique())

# Add a selectbox for choosing the location with Tbilisi as the default value
Location = st.sidebar.selectbox("Select Location:", sorted(locations), index=locations.index("Tbilisi"))

st.sidebar.markdown("<h3 style='color:gray;'><i><u>Main Specifications</u></i></h3>", unsafe_allow_html=True)

# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

# Create a dictionary to store car category by manufacturer
manufacturer_category = df.groupby(['Manufacturer'])['Category'].unique().to_dict()

# Create a dictionary to store car models by manufacturer and category
model = df.groupby(['Manufacturer', 'Category'])['Model'].unique().to_dict()

# Streamlit widgets for Manufacturer, Category, and Model
Manufacturer = col1.selectbox('Manufacturer:', sorted(list(manufacturer_category.keys())), index=sorted(list(manufacturer_category.keys())).index("Toyota"))
Category = col2.selectbox('Category:', sorted(list(manufacturer_category[Manufacturer])), index=sorted(manufacturer_category[Manufacturer]).index("Jeep"))
Model = col3.selectbox('Model:', sorted(model[(Manufacturer, Category)]))

# Create a layout with two columns
col1, col2 = st.sidebar.columns([1,2])

# Dict of possible years based on Manufacturer and Model
years = df.groupby(['Manufacturer', 'Model'])['Year'].unique().to_dict()
Year = col1.selectbox('Year:', sorted(years[(Manufacturer, Model)], reverse=True))

# Add Mileage slider
Mileage = col2.slider('Mileage (0 - 500,000)', min_value=0, max_value=500000, value=100000)

# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

# Dict of possible Fuel Types based on Manufacturer and Model
fuel_types = df.groupby(['Manufacturer', 'Model'])['Fuel type'].unique().to_dict()
Fuel_Type = col1.selectbox('Fuel Type:', fuel_types[(Manufacturer, Model)])

# Dict of possible Engine Volumes based on Manufacturer, Model and Fuel Type
engine_volumes = df.groupby(['Manufacturer', 'Model', 'Fuel type'])['Engine Volume'].unique().to_dict()
Engine_Volume = col2.selectbox('Engine Volume:', sorted(engine_volumes[(Manufacturer, Model, Fuel_Type)]))

# Dict of possible Engine Volumes based on Manufacturer, Model and Fuel Type
cylinders = df.groupby(['Manufacturer', 'Model', 'Fuel type'])['Cylinders'].unique().to_dict()
Cylinder = col3.selectbox('Cylinders:', sorted([int(x) for x in cylinders[(Manufacturer, Model, Fuel_Type)]]))
    
# Dict of possible Gear box types based on Manufacturer and Model
gear_box_types = df.groupby(['Manufacturer', 'Model'])['Gear box type'].unique().to_dict()
Gear_Box_Type = col1.selectbox('Gear box type:', sorted(gear_box_types[(Manufacturer, Model)]))

# Dict of possible Drive Wheels based on Manufacturer and Model
drive_wheels = df['Drive wheels'].unique()
Drive_Wheel = col2.selectbox('Drive wheels:', sorted(drive_wheels))

# Dict of possible Doors based on Manufacturer and Model
doors = df.groupby(['Manufacturer', 'Model'])['Doors'].unique().to_dict()
Door = col3.selectbox('Doors:', sorted(doors[(Manufacturer, Model)]))

# Create a layout with two columns
col1, col2 = st.sidebar.columns(2)

# Dict of possible number of Airbags
airbags = df.groupby(['Manufacturer', 'Category'])['Airbags'].unique().to_dict()
Airbag = col1.selectbox('Airbags:', sorted([int(x) for x in airbags[(Manufacturer, Category)]]))

# Wheels
wheels = df.Wheel.unique()
Wheel = col2.selectbox('Wheels:', wheels)


col1, col2 = st.sidebar.columns(2)
### color
# Define a dictionary of color options (name: hex code)
color_options = {
    'Black': '#000000', 'White': '#808080', 'Blue': '#0000FF', 'Red': '#ff0000', 
    'Grey': '#d3d3d3', 'Silver': '#C0C0C0', 'Golden': '#FFD700', 'Yellow': '#FFFF00', 
    'Brown': '#964B00', 'Orange': '#FFA500', 'Sky Blue': '#87CEEB', 'Carnelian red': '#B31B1B', 
    'Green': '#008000', 'Beige': '#F5F5DC', 'Violet': '#7F00FF', 'Pink': '#FC0FC0'
}

# Create a selectbox for color options in the sidebar
Color = col1.selectbox('Colors:', list(color_options.keys()), index=3)

# Get the hex code for the selected color
hex_color = color_options[Color] 

# Display the selected color as a colored square using HTML and CSS
col1.markdown(
    f"<div style='background-color: {hex_color}; width: 100%; height: 5px;'></div>",
    unsafe_allow_html=True
)

### interior color
# Define a dictionary of color options (name: hex code)
color_options = {
    'Black': '#000000', 'White': '#808080', 'Blue': '#0000FF', 'Red': '#ff0000', 
    'Grey': '#d3d3d3', 'Golden': '#FFD700', 'Yellow': '#FFFF00', 'Beige': '#F5F5DC',
    'Brown': '#964B00', 'Orange': '#FFA500', 'Carnelian red': '#B31B1B', 
}

# Create a selectbox for Interior Color options in the sidebar
Interior_Color = col2.selectbox('Interior Colors:', list(color_options.keys()), index=5)

# Get the hex code for the selected color
hex_color = color_options[Interior_Color] 

# Display the selected color as a colored square using HTML and CSS
col2.markdown(
    f"<div style='background-color: {hex_color}; width: 100%; height: 5px;'></div>",
    unsafe_allow_html=True
)

# Interior material
interior_materials = df['Interior material'].unique()
Interior_Material = st.sidebar.selectbox('Interior materials:', interior_materials)


# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

Exchange = col1.radio("Exchange:", ["Yes", "No"], index=1)

Technical_Inspection = col2.radio("Technical inspection:", ["Yes", "No"])

Catalyst = col3.radio("Catalyst:", ["Yes", "No"])




st.sidebar.markdown("<h3 style='color:gray;'><i><u>Additional Specifications:</u></i></h3>", unsafe_allow_html=True)

st.sidebar.markdown("<h4 style='color:gray;'><i><u>Comfort</u></i></h4>", unsafe_allow_html=True)

# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

Steering_Hydraulics = "Yes" if col1.checkbox("Steering Hydraulics", value=True) else "No"

On_Board_Computer = "Yes" if col2.checkbox("On-Board Computer") else "No"

Air_Conditioning = "Yes" if col3.checkbox("Air Conditioning", value=True) else "No"

Parking_Control = "Yes" if col1.checkbox("Parking Control") else "No"

Rear_View_Camera = "Yes" if col2.checkbox("Rear View Camera", value=True) else "No"

Electric_Side_Mirros = "Yes" if col3.checkbox("Electric Side Mirros", value=True) else "No"

Climate_Control = "Yes" if col1.checkbox("Climate Control") else "No"

Cruise_Control = "Yes" if col2.checkbox("Cruise Control", value=True) else "No"

Start_Stop_System = "Yes" if col3.checkbox("Start-Stop System") else "No"



st.sidebar.markdown("<h4 style='color:gray;'><i><u>Interior</u></i></h4>", unsafe_allow_html=True)

# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

Sunroof = "Yes" if col1.checkbox("Sunroof", value=True) else "No"

Heated_Seats = "Yes" if col2.checkbox("Heated Seats") else "No"

Memory_Seats = "Yes" if col3.checkbox("Memory Seats") else "No"



st.sidebar.markdown("<h4 style='color:gray;'><i><u>Safety</u></i></h4>", unsafe_allow_html=True)

# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

ABSs = "Yes" if col1.checkbox("ABS", value=True) else "No"

ESPs = "Yes" if col2.checkbox("ESP", value=True) else "No"

Central_Locking = "Yes" if col3.checkbox("Central Locking", value=True) else "No"

Alarm_System = "Yes" if col1.checkbox("Alarm System") else "No"

Fog_Lamp = "Yes" if col2.checkbox("Fog Lamp", value=True) else "No"



st.sidebar.markdown("<h4 style='color:gray;'><i><u>Multimedia</u></i></h4>", unsafe_allow_html=True)

# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

Navigation = "Yes" if col1.checkbox("Central Screen (Navigation)") else "No"

AUXs = "Yes" if col2.checkbox("AUX", value=True) else "No"

Bluetooth = "Yes" if col3.checkbox("Bluetooth") else "No"

Multi_Steering_wheel = "Yes" if col1.checkbox("Multifunction Steering Wheel") else "No"



st.sidebar.markdown("<h4 style='color:gray;'><i><u>Other</u></i></h4>", unsafe_allow_html=True)

# Create a layout with two columns
col1, col2, col3 = st.sidebar.columns(3)

Rims = "Yes" if col1.checkbox("Rims", value=True) else "No"

Spare_Tyre = "Yes" if col2.checkbox("Spare Tyre", value=True) else "No"

Didabled_Accessible = "Yes" if col3.checkbox("Didabled Accessible") else "No"


# Add a header to your main content area
st.write("<h1 style='text-align:center;font-size:80px'>Car Prices in Georgia</h1>", unsafe_allow_html=True)

# Add a text description below the header
st.write("<p style='text-align:center'><i>This website will predict car prices based on specifications listed in the sidebar.</i></p>", unsafe_allow_html=True)



################## PREDICTIO N########################
# get data into dataframe
new_row = {
    'Location': [Location], 'Manufacturer': [Manufacturer], 'Model': [Model], 'Year': [Year], 
    'Category': [Category], 'Mileage': [Mileage], 'Fuel type': [Fuel_Type], 'Engine Volume': [Engine_Volume], 
    'Cylinders': [Cylinder], 'Gear box type': [Gear_Box_Type], 'Drive wheels': [Drive_Wheel], 
    'Doors': [Door], 'Airbags': [Airbag], 'Wheel': [Wheel], 'Color': [Color], 'Interior color': [Interior_Color],
    'Interior material': [Interior_Material], 'Exchange': [Exchange], 'Technical inspection': [Technical_Inspection], 
    'Catalyst': [Catalyst], 'Steering Hydraulics': [Steering_Hydraulics], 'On-Board Computer': [On_Board_Computer], 
    'Air Conditioning': [Air_Conditioning], 'Parking Control': [Parking_Control], 'Rear View Camera': [Rear_View_Camera], 
    'Electric Side Mirros': [Electric_Side_Mirros], 'Climate Control': [Climate_Control], 'Cruise Control': [Cruise_Control], 
    'Start-Stop System': [Start_Stop_System], 'Sunroof': [Sunroof], 'Heated Seats': [Heated_Seats], 'Memory Seats': [Memory_Seats], 
    'ABS': [ABSs], 'ESP': [ESPs], 'Central Locking': [Central_Locking], 'Alarm System': [Alarm_System], 'Fog Lamp': [Fog_Lamp], 
    'Central Screen (Navigation)': [Navigation], 'AUX': [AUXs],'Bluetooth': [Bluetooth], 'Multifunction Steering Wheel': [Multi_Steering_wheel], 
    'Rims': [Rims], 'Spare Tyre': [Spare_Tyre], 'Didabled Accessible': [Didabled_Accessible]
    }
pred_df = pd.DataFrame(new_row)

# preprocess
with open('preprocessor.pkl', 'rb') as file:
    preprocessor = pickle.load(file)
data = preprocessor.transform(pred_df).toarray()

# predict
model = pickle.load(open('model.pkl', 'rb'))
pred = model.predict(data)

st.write()

# Use Markdown to style text
st.markdown(
    f"<div style='text-align:center; color:red; font-size:100px; font-weight:bold; font-style:italic;'>{int(round(pred[0], -2))}$</div>",
    unsafe_allow_html=True
)