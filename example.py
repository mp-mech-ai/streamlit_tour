import streamlit as st
from streamlit_tour import Tour, __version__
import pandas as pd
from numpy.random import default_rng as rng

st.title("Driver.js Tour Demo")
st.write(f"Streamlit Tour version: {__version__}")

with st.sidebar:
    st.button("Sidebar button", key="sidebar_btn")

col1, col2 = st.columns([5, 1], vertical_alignment="bottom")

with col1: st.text_input("Main area input", key="area_input")
with col2: st.button("Submit")

with st.container(key="text_container"):
    st.write("This is a paragraph. " * 10)

with st.container(key="dataframe_container"):
    st.area_chart(pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"]))

tour = Tour(
        steps=[
            Tour.bind("area_input", title="Area Input", desc="Streamlit Tour allows you to provide a tour of your site to the user", align="center"),
            Tour.bind("text_container", title="Text Space", desc="It can highlight every part of your application"),
            Tour.bind("dataframe_container", title="Area Chart", desc="Even complex components can be highlighted"),
            Tour.bind("sidebar_btn", title="Sidebar button", desc="And components from the sidebar"),
            Tour.info(title="Element-free information", desc="You can also provide information without selecting a specific element"),
        ],
        show_progress=True,
        animate=True,
        overlay_opacity=0.75,
        one_time_tour=False,
        key=f"presentation_tour",
    )

if st.button("Start Tour"):
    tour.start()

st.write(tour)
    