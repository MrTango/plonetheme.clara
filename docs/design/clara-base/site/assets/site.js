(() => {
  const header = document.querySelector("[data-site-header]");
  if (!header) return;

  const menuToggle = header.querySelector("[data-menu-toggle]");
  const triggers = [...header.querySelectorAll("[data-mega-trigger]")];
  const panels = [...header.querySelectorAll("[data-mega-panel]")];
  const backdrop = header.querySelector("[data-mega-backdrop]");
  const desktop = window.matchMedia("(min-width: 70rem)");
  let lastTrigger = null;

  const closePanels = ({ restoreFocus = false } = {}) => {
    triggers.forEach((trigger) => trigger.setAttribute("aria-expanded", "false"));
    panels.forEach((panel) => {
      panel.hidden = true;
    });
    if (backdrop) backdrop.hidden = true;
    if (restoreFocus && lastTrigger) lastTrigger.focus();
    lastTrigger = null;
  };

  const openPanel = (trigger) => {
    const panel = document.getElementById(trigger.getAttribute("aria-controls"));
    if (!panel) return;
    closePanels();
    trigger.setAttribute("aria-expanded", "true");
    panel.hidden = false;
    lastTrigger = trigger;
    if (backdrop && desktop.matches) backdrop.hidden = false;
  };

  triggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const wasOpen = trigger.getAttribute("aria-expanded") === "true";
      if (wasOpen) closePanels();
      else openPanel(trigger);
    });
  });

  menuToggle?.addEventListener("click", () => {
    const isOpen = header.getAttribute("data-nav-open") === "true";
    closePanels();
    header.setAttribute("data-nav-open", String(!isOpen));
    menuToggle.setAttribute("aria-expanded", String(!isOpen));
  });

  backdrop?.addEventListener("click", () => closePanels({ restoreFocus: true }));

  document.addEventListener("click", (event) => {
    if (!header.contains(event.target)) closePanels();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    const panelOpen = triggers.some(
      (trigger) => trigger.getAttribute("aria-expanded") === "true",
    );
    if (panelOpen) {
      event.preventDefault();
      closePanels({ restoreFocus: true });
      return;
    }
    if (header.getAttribute("data-nav-open") === "true") {
      header.setAttribute("data-nav-open", "false");
      menuToggle?.setAttribute("aria-expanded", "false");
      menuToggle?.focus();
    }
  });

  header.querySelectorAll(".mega-panel a, .nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      closePanels();
      header.setAttribute("data-nav-open", "false");
      menuToggle?.setAttribute("aria-expanded", "false");
    });
  });

  desktop.addEventListener("change", () => {
    closePanels();
    header.setAttribute("data-nav-open", "false");
    menuToggle?.setAttribute("aria-expanded", "false");
  });
})();
