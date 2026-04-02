[![PyPI version](https://img.shields.io/pypi/v/streamlit-tour)](https://pypi.org/project/streamlit-tour/)
[![Python versions](https://img.shields.io/pypi/pyversions/streamlit-tour)](https://pypi.org/project/streamlit-tour/)
[![License](https://img.shields.io/pypi/l/streamlit-tour)](./LICENSE)


# 🚗 streamlit-tour

A [Driver.js](https://driverjs.com/) integration for [Streamlit](https://streamlit.io/) - add beautiful, interactive guided tours to your Streamlit apps with a single Python call.

<!-- Replace the line below with your actual GIF -->
![streamlit-tour demo](https://your-demo-gif-url-here.gif)


## Features

- 🎯 **Bind tour steps to any Streamlit widget** by its `key`
- 📦 **Sidebar-aware** - highlights sidebar components without z-index glitches
- 🪟 **Element-free info steps** - show contextual popups not anchored to any component
- 💾 **One-time tours** - automatically skip tours the user has already completed (via `localStorage`)
- ↩️ **State feedback** - know exactly when a tour was finished, dismissed, or skipped
- 🎨 **Configurable** - control overlay opacity, animations, progress indicators, and popover alignment


## Installation

```bash
pip install streamlit-tour
```
Or in a more modern way:

```bash
uv add streamlit-tour
```


## Quickstart

```python
import streamlit as st
from streamlit_tour import Tour

st.title("My App")
st.text_input("Name", key="name_input")

if st.button("Start Tour"):
    Tour.start(
        steps=[
            Tour.bind("name_input", title="Your Name", desc="Enter your name here."),
            Tour.info(title="That's it!", desc="You're ready to go."),
        ]
    )
```


## Usage

### `Tour.start()`

Launches the tour. Call this inside any conditional block (e.g. a button click).

```python
result = Tour.start(
    steps=[...],
    show_progress=True,       # Show "Step 1/3" counter
    animate=True,             # Animate transitions between steps
    overlay_opacity=0.75,     # Background overlay darkness (0.0–1.0)
    one_time_tour=False,      # If True, skip the tour after first completion
    key="my_tour",            # Unique key - change it for each tour
)
```

**Return value** - a dict with the tour's final state:

| Key            | Type   | Description                                          |
|----------------|--------|------------------------------------------------------|
| `currentStep`  | `int`  | Last step index the user reached                     |
| `dismissed`    | `bool` | `True` if the user closed the tour before finishing  |
| `finished`     | `bool` | `True` if the user completed all steps               |
| `skipped`      | `bool` | `True` if the tour was skipped (one-time, already seen) |

### `Tour.bind()`

---

Attaches a tour step to a Streamlit widget via its `key`.

```python
Tour.bind(
    key="my_widget_key",        # Must match the widget's key= argument
    title="Step Title",
    desc="Step description text.",
    side="bottom",              # "top" | "bottom" | "left" | "right" (optional)
    align="center",             # "start" | "center" | "end" (optional)
)
```

> **How it works:** `Tour.bind` resolves the widget using Streamlit's `.st-key-<key>` CSS class, which is automatically injected on any widget that has a `key=` argument.


### `Tour.info()`

---

Creates a floating step with no element anchor - useful for introductory or summary slides.

```python
Tour.info(
    title="Welcome!",
    desc="This tour will walk you through the main features of this app.",
)
```


## One-Time Tour

Set `one_time_tour=True` to automatically skip the tour for users who have already seen it. Completion is tracked in the browser's `localStorage` using the tour's `key`.

```python
Tour.start(
    steps=[...],
    one_time_tour=True,
    key="onboarding_tour",   # Must be unique and stable across reruns
)
```

To reset the tour (e.g. for testing), clear `localStorage` in your browser's DevTools, or use a different `key`.

Check out `example.py` file for a complete example of usage.

## Tips

- **Always provide a `key`** when using `one_time_tour=True` or when you have multiple tours on the same page.
- **Widgets must have a `key=` argument** for `Tour.bind()` to locate them. Anonymous widgets (no `key`) are not bindable.
- **Re-triggering a tour:** Change the `key` value between Streamlit reruns to force the tour to restart.
- **Column layouts:** Use `side` and `align` on `Tour.bind()` to control which side the popover appears on narrow widgets.


## Roadmap / Possible Improvements

- [ ] **Better output** - make the Tour returns an object instead of a simple dict
- [ ] **Custom button labels** - override "Next", "Previous", "Done" text per step or globally
- [ ] **Step grouping** - define multiple named tours and selectively launch them
- [ ] **`Tour.reset(key)`** - a utility function to clear the one-time-tour flag from `localStorage`
- [ ] **Theme support** - CSS variable overrides to match Streamlit's light/dark mode



