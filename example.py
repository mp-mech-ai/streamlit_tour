import streamlit as st
from streamlit_tour import Tour
import streamlit_tour

st.title("Driver.js Tour Demo")
st.write(streamlit_tour.__version__)
with st.sidebar:
    st.button("Sidebar button", key="sidebar_btn")

st.text_input("Main area input", key="driver_step_1")

with st.container(key="driver_step_2"):
    st.write("This is a paragraph. " * 10)

if st.button("Start Tour"):
    st.session_state["tour_active"] = True
    if "tour_run" not in st.session_state: 
        st.session_state["tour_run"] = 1 
    else: 
        st.session_state["tour_run"] += 1

# Mount the component persistently — survives reruns while tour is active
if st.session_state.get("tour_active"):
    result = Tour.start(
        steps=[
            Tour.bind("driver_step_1", title="Driver.js step 1"),
            Tour.bind("driver_step_2", title="Driver.js step 2"),
            Tour.bind("sidebar_btn", title="Driver.js step 3"),
        ],
        show_progress=True,
        key=f"my_tour_{st.session_state['tour_run']}",
    )

    # Tour finished — clean up and show final state
    if result and result.get("dismissed") is not False or result.get("currentStep", 0) > 0:
        st.session_state["tour_active"] = False
        st.write("Tour finished at step:", result.get("currentStep"))
        st.write("Tour dismissed", result.get("dismissed"))
    