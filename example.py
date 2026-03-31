import streamlit as st
from streamlit_tour import tour

st.title("Driver.js Tour Demo")

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
    result = tour(
        steps=[
            {
                "key": "driver_step_1",
                "popover": {
                    "title": "Step 1",
                    "description": "This is the main area input.",
                    "side": "top",
                },
            },
            {
                "key": "driver_step_2",
                "popover": {
                    "title": "Step 2",
                    "description": "This is a paragraph.",
                },
            },
            {
                "key": "sidebar_btn",
                "popover": {
                    "title": "Sidebar",
                    "description": "Notice the sidebar is behind the overlay.",
                },
            },
        ],
        show_progress=True,
        key=f"my_tour_{st.session_state['tour_run']}",
    )

    # Tour finished — clean up and show final state
    if result and result.get("dismissed") is not False or result.get("currentStep", 0) > 0:
        st.session_state["tour_active"] = False
        st.write("Tour finished at step:", result.get("currentStep"))
        st.write("Tour dismissed", result.get("dismissed"))
    