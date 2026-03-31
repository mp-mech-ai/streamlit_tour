import { driver } from "driver.js";
import type { DriveStep, Config, Driver } from "driver.js";
import "driver.js/dist/driver.css";

interface PopoverConfig {
  title?: string;
  description?: string;
  side?: "top" | "bottom" | "left" | "right";
  align?: "start" | "center" | "end";
}

interface Step {
  element?: string;
  popover?: PopoverConfig;
}

interface ComponentData {
  steps: Step[];
  showProgress?: boolean;
  animate?: boolean;
  overlayOpacity?: number;
}

interface ComponentProps {
  parentElement: HTMLElement;
  data: ComponentData;
  setStateValue: (key: string, value: unknown) => void;
  setTriggerValue: (key: string, value: unknown) => void;
}

const STYLE_ID = "streamlit-driverjs-overrides";

function injectZIndexOverrides(): void {
  if (document.getElementById(STYLE_ID)) return;
  const style = document.createElement("style");
  style.id = STYLE_ID;
  style.textContent = `
    [data-testid="stSidebarContainer"],
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] {
      z-index: 1 !important;
    }
    header[data-testid="stHeader"] {
      z-index: 1 !important;
    }
    .driver-overlay {
      z-index: 999999 !important;
    }
    .driver-popover {
      z-index: 1000000 !important;
    }
    .driver-active-element,
    [data-testid="stSidebar"].driver-active-element {
      z-index: 1000000 !important;
    }
  `;
  document.head.appendChild(style);
}

let activeDriver: Driver | null = null;

// Track step locally in JS — never triggers a Streamlit rerun
let currentStepIndex = 0;

const DriverJsComponent = ({
  data,
  setStateValue,
}: ComponentProps): (() => void) => {

  injectZIndexOverrides();

  // Only destroy if there's an active tour — do NOT restart if already running
  // This prevents the rerun loop from killing the tour mid-navigation
  if (activeDriver?.isActive()) {
    return () => {};   // ← tour is already running, do nothing on remount
  }

  if (activeDriver) {
    activeDriver.destroy();
    activeDriver = null;
  }

  const {
    steps = [],
    showProgress = true,
    animate = true,
    overlayOpacity = 0.75,
  } = data;

  if (steps.length === 0) {
    console.warn("[streamlit-driverjs] No steps provided.");
    return () => {};
  }

  currentStepIndex = 0;

  const config: Config = {
    showProgress,
    animate,
    overlayOpacity,
    steps: steps as DriveStep[],

    // Track step locally — no Streamlit rerun triggered here
    onNextClick: () => {
      currentStepIndex += 1;
      activeDriver?.moveNext();
    },

    onPrevClick: () => {
      currentStepIndex -= 1;
      activeDriver?.movePrevious();
    },

    // Only report to Python when tour is fully over
    // setStateValue here triggers ONE rerun after the tour ends — that's fine
    onDestroyStarted: () => {
      const wasFinished =
        activeDriver?.isLastStep() ?? false;

      setStateValue("currentStep", currentStepIndex);
      setStateValue("dismissed", !wasFinished);

      activeDriver?.destroy();
      activeDriver = null;
    },
  };

  activeDriver = driver(config);
  activeDriver.drive();

  return () => {
    if (activeDriver) {
      activeDriver.destroy();
      activeDriver = null;
    }
  };
};

export default DriverJsComponent;