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
  oneTimeTour?: boolean;
  key?: string;
}

interface ComponentProps {
  parentElement: HTMLElement;
  data: ComponentData;
  setStateValue: (key: string, value: unknown) => void;
  setTriggerValue: (key: string, value: unknown) => void;
}

const STYLE_ID = "streamlitTourStyle";  // for z-index overrides
const TOUR_STORAGE_PREFIX = "streamlitTour_"; // for tracking seen tours

function getTourStorageKey(tourKey: string): string {
  return `${TOUR_STORAGE_PREFIX}${tourKey}`;
}

function hasTourBeenSeen(tourKey: string): boolean {
  try {
    return localStorage.getItem(getTourStorageKey(tourKey)) === "1";
  } catch {
    return false; // private browsing or storage blocked
  }
}

function markTourAsSeen(tourKey: string): void {
  try {
    localStorage.setItem(getTourStorageKey(tourKey), "1");
  } catch {
    // silently ignore if storage is unavailable
  }
}

// Injects z-index overrides for the sidebar, header, and driver.js popovers
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
let currentStepIndex = 0;
let hasReachedLastStep = false;

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

  // Destroy any existing tour
  if (activeDriver) {
    activeDriver.destroy();
    activeDriver = null;
  }

  const {
    steps = [],
    showProgress = true,
    animate = true,
    overlayOpacity = 0.75,
    oneTimeTour = false,
    key = "driverjs",
  } = data;

  // If this is a one-time tour and it has already been seen, skip it
  if (oneTimeTour && hasTourBeenSeen(key)) {
    setStateValue("skipped", true);
    return () => {};
  }

  // If there are no steps, do nothing and log it
  if (steps.length === 0) {
    console.warn("[streamlit-driverjs] No steps provided.");
    setStateValue("skipped", true);
    return () => {};
  }

  currentStepIndex = 0;
  hasReachedLastStep = steps.length <= 1;

  const config: Config = {
    showProgress,
    animate,
    overlayOpacity,
    steps: steps as DriveStep[],

    onNextClick: () => {
      currentStepIndex += 1;

      if (currentStepIndex >= steps.length - 1) {
        hasReachedLastStep = true;
      }
      setStateValue("currentStep", currentStepIndex);
      activeDriver?.moveNext();
    },
    onPrevClick: () => {
      currentStepIndex -= 1;
      setStateValue("currentStep", currentStepIndex);
      activeDriver?.movePrevious();
    },
    onDestroyStarted: () => {
      const wasFinished = hasReachedLastStep || (activeDriver?.isLastStep() ?? false);
      
      // If the user succesfully went to the last step and this is a one-time tour, mark it as seen
      if (oneTimeTour && wasFinished) {
        markTourAsSeen(key);
      }

      setStateValue("currentStep", currentStepIndex);
      setStateValue("dismissed", !wasFinished);
      setStateValue("finished", wasFinished);
      setStateValue("skipped", false);
      activeDriver?.destroy();
      activeDriver = null;
    },
  };

  activeDriver = driver(config);
  activeDriver.drive();

  return () => {
    if (activeDriver && !activeDriver.isActive()) {
      activeDriver.destroy();
      activeDriver = null;
    }
  };
};

export default DriverJsComponent;