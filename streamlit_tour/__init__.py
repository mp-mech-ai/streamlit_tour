from __future__ import annotations
from typing import Any
import streamlit.components.v2 as components
from importlib.metadata import version
from typing import Optional, Literal
import streamlit as st

__version__ = version("streamlit_tour")

# Register the component once at import time.
out = components.component(
    name="streamlit-tour.streamlit_tour",
    js="index-*.js",                # glob — matches the hashed vite output
)

def on_unused_state_change():
    pass

class Step:
    element: str
    popover: dict

    def __init__(self, element: str, popover: dict):
        self.element = element
        self.popover = popover
    
    def to_dict(self):
        if self.element:
            return {
                "element": self.element,
                "popover": self.popover
            }
        else:
            return {
                "popover": self.popover
            }

class TourStatus:
    """
    Object containing the status of a Driver.js tour.
    """
    currentStep: int
    dismissed: bool
    finished: bool
    skipped: bool

    def __init__(self, currentStep: int, dismissed: bool, finished: bool, skipped: bool):
        self.currentStep = currentStep
        self.dismissed = dismissed
        self.finished = finished
        self.skipped = skipped
    
    def to_dict(self):
        return {
            "currentStep": self.currentStep,
            "dismissed": self.dismissed,
            "finished": self.finished
        }
    

class Tour:
    def start(
            steps: list[dict[str, Any]],
            *,
            show_progress: bool = True,
            animate: bool = True,
            overlay_opacity: float = 0.75,
            one_time_tour: bool = False,
            key: str | None = None,
        ):
        """
        Start a Driver.js guided tour.

        Parameters
        ----------
        steps : list of Step, i.e. tour.bind(...)
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
            - ``finished``   (bool)  : True when the tour has been completed
            - ``skipped``    (bool)  : True when the tour has been skipped because the user has already seen it
        """
        steps_list_of_dict = [step.to_dict() for step in steps]

        component_value = out(
            data={
                "steps": steps_list_of_dict,
                "showProgress": show_progress,
                "animate": animate,
                "overlayOpacity": overlay_opacity,
                "oneTimeTour": one_time_tour,
                "key": key
            },
            default={
                "currentStep": 0, 
                "dismissed": False,
                "finished": False,
                "skipped": False,
            },
            key=key,
            height=0,
            on_currentStep_change=on_unused_state_change,
            on_dismissed_change=on_unused_state_change,
            on_finished_change=on_unused_state_change,
            on_skipped_change=on_unused_state_change
        )

        return TourStatus(**component_value)
    
    def bind(
            key: str,
            title: str = "Title",
            desc: str = "Description",
            side: Optional[Literal["top", "bottom", "left", "right"]] = None,
            align: Optional[Literal["start", "center", "end"]] = None,
            ):
        """
        Binds a streamlit component to a step in the tour.
        """
        if side is None and align is None:
            return Step(".st-key-" + key, {"title": title, "description": desc})
        elif side is None and align is not None:
            return Step(".st-key-" + key, {"title": title, "description": desc, "align": align})
        elif side is not None and align is None:
            return Step(".st-key-" + key, {"title": title, "description": desc, "side": side})
        else:
            return Step(".st-key-" + key, {"title": title, "description": desc, "side": side, "align": align})
    
    def info(
            title: str = "Title",
            desc: str = "Description",
            ):
        return Step("", {"title": title, "description": desc})