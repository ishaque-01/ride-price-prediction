import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime

try:
    from streamlit_folium import st_folium
    import folium
    FOLIUM_AVAILABLE = True
except Exception:
    FOLIUM_AVAILABLE = False

st.set_page_config(page_title="Taxi Fare Predictor", page_icon="🚖")

@st.cache_resource
def load_model():
    return joblib.load('ride_fare_model.pkl')

try:
    model = load_model()
except FileNotFoundError:
    st.error("Error: 'ride_fare_model.pkl' not found. Please put the pkl file in the same folder as this script.")
    st.stop()

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of Earth in km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c


def request_rerun():
    try:
        st.experimental_rerun()
        return
    except Exception:
        pass

    try:
        # Fallback to internal API
        from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx is not None:
            ctx.request_rerun()
            return
    except Exception:
        pass

    try:
        # Older Streamlit versions might expose a RerunException
        from streamlit.runtime.scriptrunner import RerunException
        raise RerunException()
    except Exception:
        # Last resort: do nothing
        return


st.title("🚖 AI Ride Fare Estimator")
st.markdown("Enter the trip details below to predict the **Total Fare Amount**.")

if 'pending_click' in st.session_state:
    pc = st.session_state.pop('pending_click')
    pmode = pc.get('mode', 'pickup')
    plat = pc.get('lat')
    plon = pc.get('lon')
    if plat is not None and plon is not None:
        if pmode == 'pickup':
            st.session_state['pickup_lat'] = float(plat)
            st.session_state['pickup_lon'] = float(plon)
        else:
            st.session_state['dropoff_lat'] = float(plat)
            st.session_state['dropoff_lon'] = float(plon)

with st.sidebar:
    st.header("Trip Details")

    if 'pickup_lat' not in st.session_state:
        st.session_state['pickup_lat'] = 27.528372115874646
    if 'pickup_lon' not in st.session_state:
        st.session_state['pickup_lon'] = 68.75816592404738
    if 'dropoff_lat' not in st.session_state:
        st.session_state['dropoff_lat'] = 27.288129454747526
    if 'dropoff_lon' not in st.session_state:
        st.session_state['dropoff_lon'] = 68.50705633107253

    st.subheader("📍 Pickup Location")

    st.number_input("Pickup Latitude", format="%f", key='pickup_lat')
    st.number_input("Pickup Longitude", format="%f", key='pickup_lon')

    st.subheader("📍 Dropoff Location")
    st.number_input("Dropoff Latitude", format="%f", key='dropoff_lat')
    st.number_input("Dropoff Longitude", format="%f", key='dropoff_lon')

    st.subheader("🕒 Date & Time")
    if 'trip_date' not in st.session_state:
        st.session_state['trip_date'] = datetime.date.today()
    if 'trip_time' not in st.session_state:
        st.session_state['trip_time'] = datetime.datetime.now().time()
    d = st.date_input("Date", key='trip_date')
    t = st.time_input("Time", key='trip_time')

    st.markdown("---")
    st.write("Map click mode:")
    if 'map_mode' not in st.session_state:
        st.session_state['map_mode'] = 'pickup'
    st.radio("Choose which marker to set by clicking the map:", options=['pickup', 'dropoff'], index=0, key='map_mode')

pickup_lat = float(st.session_state['pickup_lat'])
pickup_lon = float(st.session_state['pickup_lon'])
dropoff_lat = float(st.session_state['dropoff_lat'])
dropoff_lon = float(st.session_state['dropoff_lon'])

dist = haversine_distance(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)

st.subheader(" Trip Map")
if FOLIUM_AVAILABLE:
    center_lat = (pickup_lat + dropoff_lat) / 2
    center_lon = (pickup_lon + dropoff_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    folium.Marker([pickup_lat, pickup_lon], tooltip='Pickup', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([dropoff_lat, dropoff_lon], tooltip='Dropoff', icon=folium.Icon(color='red')).add_to(m)

    map_data = st_folium(m, width=700, height=450)

    last_clicked = None
    if isinstance(map_data, dict):
        last_clicked = map_data.get('last_clicked') or map_data.get('last_object_clicked')

    if last_clicked:
        lat = last_clicked.get('lat') or last_clicked.get('latitude')
        lon = last_clicked.get('lng') or last_clicked.get('lon') or last_clicked.get('longitude')
        if lat is not None and lon is not None:
            st.session_state['pending_click'] = {
                'mode': st.session_state.get('map_mode', 'pickup'),
                'lat': float(lat),
                'lon': float(lon)
            }
            request_rerun()
else:
    st.warning("For interactive map clicks install `streamlit-folium` and `folium` (see `requirements.txt`). Showing static map instead.")
    map_data = pd.DataFrame({
        'lat': [pickup_lat, dropoff_lat],
        'lon': [pickup_lon, dropoff_lon]
    })
    st.map(map_data)

if st.button("Predict Fare 💰", type="primary"):
    
    trip_datetime = datetime.datetime.combine(d, t)
    
    input_data = pd.DataFrame({
        'pickup_location_latitude': [pickup_lat],
        'pickup_location_longitude': [pickup_lon],
        'dropoff_location_latitude': [dropoff_lat],
        'dropoff_location_longitude': [dropoff_lon],
        'distance_km': [dist],
        'hour': [trip_datetime.hour],
        'day_of_week': [trip_datetime.weekday()]
    })

    prediction = model.predict(input_data)[0]
    
    st.success(f"Estimated Fare: ${prediction:.2f}")
    
    with st.expander("See Trip Details"):
        st.write(f"**Distance:** {dist:.2f} km")
        st.write(f"**Hour of Day:** {trip_datetime.hour}:00")
        st.write(f"**Day of Week:** {trip_datetime.strftime('%A')}")