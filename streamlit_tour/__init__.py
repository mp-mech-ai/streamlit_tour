from __future__ import annotations
from typing import Any
import streamlit.components.v2 as components

# Register the component once at import time.
out = components.component(
    name="streamlit_tour.streamlit_tour",
    js="index-*.js",                # glob — matches the hashed vite output
)

def on_currentStep_change():
    pass

def on_dismissed_change():
    pass

# TODO : - Build a more user-friendly API (give streamlit component instead of css classnames)
def tour(
    steps: list[dict[str, Any]],
    *,
    show_progress: bool = True,
    animate: bool = True,
    overlay_opacity: float = 0.75,
    key: str | None = None,
) -> dict[str, Any]:
    """
    Start a Driver.js guided tour.

    Parameters
    ----------
    steps : list of dicts
        Each step almost matches the Driver.js step schema, e.g.:
        [
            {"key": "my_widget",
             "popover": {"title": "Hello", "description": "This is step 1"}},
        ]
    show_progress : bool
        Show "1/3" step counter in the popover.
    animate : bool
        Animate transitions between steps.
    overlay_opacity : float
        Background overlay opacity (0.0 - 1.0).
    key : str, optional
        Streamlit widget key. Change it to re-trigger the tour before a streamlit rerun.

    Returns
    -------
    dict with keys:
        - ``currentStep`` (int)  : last step index the user reached
        - ``dismissed``  (bool)  : True when the user closed the tour
    """
    for step in steps:
        step["element"] = ".st-key-" + step["key"]
    
    component_value = out(
        data={
            "steps": steps,
            "showProgress": show_progress,
            "animate": animate,
            "overlayOpacity": overlay_opacity,
        },
        default={
            "currentStep": 0, 
            "dismissed": False
        },
        key=key,
        on_currentStep_change=on_currentStep_change,
        on_dismissed_change=on_dismissed_change
    )

    return component_value