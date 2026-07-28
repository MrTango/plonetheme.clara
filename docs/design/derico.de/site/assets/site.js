(() => {
  const header = document.querySelector("[data-site-header]");

  if (header) {
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
        panel.removeAttribute("data-open");
      });
      if (backdrop) backdrop.hidden = true;
      document.body.removeAttribute("data-mega-open");
      if (restoreFocus && lastTrigger) lastTrigger.focus();
      lastTrigger = null;
    };

    const openPanel = (trigger) => {
      const panel = document.getElementById(trigger.getAttribute("aria-controls"));
      if (!panel) return;
      closePanels();
      trigger.setAttribute("aria-expanded", "true");
      panel.hidden = false;
      panel.setAttribute("data-open", "true");
      lastTrigger = trigger;
      document.body.setAttribute("data-mega-open", "true");
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
      if (event.key === "Escape") {
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
  }

  const contactForm = document.querySelector("[data-contact-form]");
  if (!contactForm) return;

  const status = contactForm.querySelector("[data-form-status]");
  const fields = [...contactForm.querySelectorAll("[data-required]")];
  const messages = {
    de: {
      required: "Bitte füllen Sie dieses Feld aus.",
      email: "Bitte geben Sie eine vollständige E-Mail-Adresse ein, zum Beispiel name@unternehmen.de.",
      status: "Ihr E-Mail-Programm wird geöffnet. Prüfen Sie die Nachricht dort und senden Sie sie ab.",
      subject: "Anfrage über derico.de",
    },
    en: {
      required: "Please complete this field.",
      email: "Enter a complete email address, for example name@company.com.",
      status: "Your email application is opening. Review the message there and send it when ready.",
      subject: "Enquiry via derico.de",
    },
  };
  const lang = document.documentElement.lang === "en" ? "en" : "de";
  const copy = messages[lang];

  const validate = (field) => {
    const error = document.getElementById(`${field.id}-error`);
    let message = "";
    if (!field.value.trim()) message = copy.required;
    else if (field.type === "email" && !field.validity.valid) message = copy.email;
    field.setAttribute("aria-invalid", String(Boolean(message)));
    if (error) {
      error.textContent = message;
      error.hidden = !message;
    }
    return !message;
  };

  fields.forEach((field) => field.addEventListener("blur", () => validate(field)));

  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const valid = fields.map(validate).every(Boolean);
    if (!valid) {
      contactForm.querySelector('[aria-invalid="true"]')?.focus();
      return;
    }

    const data = new FormData(contactForm);
    const lines = [
      `${lang === "de" ? "Name" : "Name"}: ${data.get("name")}`,
      `${lang === "de" ? "Unternehmen" : "Company"}: ${data.get("company") || "—"}`,
      `${lang === "de" ? "E-Mail" : "Email"}: ${data.get("email")}`,
      `${lang === "de" ? "Thema" : "Topic"}: ${data.get("topic")}`,
      "",
      String(data.get("message")),
    ];
    const mailto = `mailto:md@derico.de?subject=${encodeURIComponent(copy.subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
    if (status) {
      status.textContent = copy.status;
      status.hidden = false;
      status.focus();
    }
    window.location.href = mailto;
  });
})();
