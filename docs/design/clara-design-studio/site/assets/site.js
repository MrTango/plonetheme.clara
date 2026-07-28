(() => {
  const variant = document.documentElement.dataset.variant;
  if (variant) {
    document.querySelectorAll('a[href]:not([href^="#"]):not([href^="http"]):not([href^="mailto:"])').forEach((link) => {
      const url = new URL(link.getAttribute("href"), window.location.href);
      url.searchParams.set("variant", variant);
      link.href = url;
    });
  }

  const header = document.querySelector("[data-header]");

  if (header) {
    const menuToggle = header.querySelector("[data-menu-toggle]");
    const disclosures = [...header.querySelectorAll("[data-nav-details]")];
    let activeSummary = null;

    const closeDisclosures = ({ restoreFocus = false, except = null } = {}) => {
      disclosures.forEach((details) => {
        if (details !== except) details.open = false;
      });
      if (restoreFocus && activeSummary) activeSummary.focus();
      if (!except) activeSummary = null;
    };

    disclosures.forEach((details) => {
      details.addEventListener("toggle", () => {
        if (!details.open) return;
        activeSummary = details.querySelector("summary");
        closeDisclosures({ except: details });
      });
    });

    menuToggle?.addEventListener("click", () => {
      const open = header.getAttribute("data-menu-open") === "true";
      if (open) closeDisclosures();
      header.setAttribute("data-menu-open", String(!open));
      menuToggle.setAttribute("aria-expanded", String(!open));
    });

    document.addEventListener("click", (event) => {
      if (!header.contains(event.target)) closeDisclosures();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") return;
      const hasOpenDisclosure = disclosures.some((details) => details.open);
      if (hasOpenDisclosure) {
        event.preventDefault();
        closeDisclosures({ restoreFocus: true });
        return;
      }
      if (header.getAttribute("data-menu-open") === "true") {
        header.setAttribute("data-menu-open", "false");
        menuToggle?.setAttribute("aria-expanded", "false");
        menuToggle?.focus();
      }
    });

    header.querySelectorAll(".mega-panel a, .direct-link").forEach((link) => {
      link.addEventListener("click", () => {
        closeDisclosures();
        header.setAttribute("data-menu-open", "false");
        menuToggle?.setAttribute("aria-expanded", "false");
      });
    });

    window.matchMedia("(min-width: 70rem)").addEventListener("change", () => {
      closeDisclosures();
      header.setAttribute("data-menu-open", "false");
      menuToggle?.setAttribute("aria-expanded", "false");
    });
  }

  const form = document.querySelector("[data-contact-form]");
  if (form) {
    const lang = document.documentElement.lang === "en" ? "en" : "de";
    const messages = {
      de: {
        required: "Bitte füllen Sie dieses Feld aus.",
        email: "Die E-Mail-Adresse braucht ein @-Zeichen und eine Domain, zum Beispiel name@organisation.de.",
        status: "Die Anfrage ist vorbereitet. Ihr E-Mail-Programm wird jetzt geöffnet; prüfen Sie die Nachricht dort und senden Sie sie ab.",
        subject: "Projektanfrage an Clara Design Studio",
      },
      en: {
        required: "Please complete this field.",
        email: "Email addresses need an @ symbol and a domain, for example name@organisation.org.",
        status: "Your enquiry is ready. Your email application will now open; review the message there and send it when ready.",
        subject: "Project enquiry for Clara Design Studio",
      },
    }[lang];
    const requiredFields = [...form.querySelectorAll("[data-required]")];
    const status = form.querySelector("[data-form-status]");

    const validate = (field) => {
      const error = document.getElementById(`${field.id}-error`);
      let message = "";
      if (!field.value.trim()) message = messages.required;
      else if (field.type === "email" && !field.validity.valid) message = messages.email;
      field.setAttribute("aria-invalid", String(Boolean(message)));
      if (error) {
        error.textContent = message;
        error.hidden = !message;
      }
      return !message;
    };

    requiredFields.forEach((field) => field.addEventListener("blur", () => validate(field)));

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const valid = requiredFields.map(validate).every(Boolean);
      if (!valid) {
        form.querySelector('[aria-invalid="true"]')?.focus();
        return;
      }

      const data = new FormData(form);
      const lines = [
        `Name: ${data.get("name")}`,
        `${lang === "de" ? "Organisation" : "Organisation"}: ${data.get("organisation") || "—"}`,
        `${lang === "de" ? "E-Mail" : "Email"}: ${data.get("email")}`,
        `${lang === "de" ? "Thema" : "Topic"}: ${data.get("topic")}`,
        "",
        String(data.get("message")),
      ];
      if (status) {
        status.textContent = messages.status;
        status.hidden = false;
        status.focus();
      }
      window.location.href = `mailto:hello@clara-studio.example?subject=${encodeURIComponent(messages.subject)}&body=${encodeURIComponent(lines.join("\n"))}`;
    });
  }

  const searchForm = document.querySelector("[data-search-form]");
  if (searchForm) {
    const results = [...document.querySelectorAll(".search-results li")];
    const count = document.querySelector(".result-count");
    const lang = document.documentElement.lang === "en" ? "en" : "de";

    searchForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const query = String(new FormData(searchForm).get("q") || "").trim().toLocaleLowerCase(lang);
      let visible = 0;
      results.forEach((result) => {
        const match = !query || result.textContent.toLocaleLowerCase(lang).includes(query);
        result.hidden = !match;
        if (match) visible += 1;
      });
      if (count) {
        const displayQuery = query || (lang === "de" ? "alle Inhalte" : "all content");
        count.textContent = visible
          ? (lang === "de" ? `${visible} Ergebnisse für „${displayQuery}“` : `${visible} results for ‘${displayQuery}’`)
          : (lang === "de" ? `Keine Ergebnisse für „${displayQuery}“. Prüfen Sie die Schreibweise oder suchen Sie nach einem allgemeineren Begriff.` : `No results for ‘${displayQuery}’. Check the spelling or try a broader term.`);
      }
    });
  }
})();
