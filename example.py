import streamlit as st
from streamlit_tour import Tour
import streamlit_tour

st.title("Driver.js Tour Demo")
st.write(f"Streamlit Tour version: {streamlit_tour.__version__}")

with st.sidebar:
    st.button("Sidebar button", key="sidebar_btn")

st.text_input("Main area input", key="driver_step_1")

with st.container(key="driver_step_2"):
    st.write("This is a paragraph. " * 10)

if "tour_done" not in st.session_state:
    st.session_state.tour_done = False

if not st.session_state.tour_done:
    if st.button("Start Tour"):
        result = Tour.start(
            steps=[
                Tour.bind("driver_step_1", title="Driver.js step 1", desc="This is a description", align="center"),
                Tour.bind("driver_step_2", title="Driver.js step 2"),
                Tour.bind("sidebar_btn", title="Driver.js step 3"),
            ],
            show_progress=True,
            animate=True,
            overlay_opacity=0.75,
            one_time_tour=True,
            key=f"presentation_tour",
        )
        
        if result.get("finished") or result.get("skipped"):
            st.session_state.tour_done = True

    