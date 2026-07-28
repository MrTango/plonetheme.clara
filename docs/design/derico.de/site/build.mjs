import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));

const slugs = {
  de: {
    home: "index.html",
    services: "leistungen.html",
    odoo: "odoo.html",
    odooDevelopment: "odoo-entwicklung.html",
    odooConsulting: "odoo-beratung.html",
    odooOperations: "odoo-betrieb.html",
    plone: "plone.html",
    python: "python.html",
    sustainability: "nachhaltigkeit.html",
    care: "support-wartung.html",
    support: "support.html",
    maintenance: "wartung.html",
    knowledge: "schulungen-vortraege.html",
    training: "schulungen.html",
    talks: "vortraege.html",
    contact: "kontakt.html",
    imprint: "impressum.html",
  },
  en: {
    home: "index.html",
    services: "services.html",
    odoo: "odoo.html",
    odooDevelopment: "odoo-development.html",
    odooConsulting: "odoo-consulting.html",
    odooOperations: "odoo-operations.html",
    plone: "plone.html",
    python: "python.html",
    sustainability: "sustainability.html",
    care: "support-maintenance.html",
    support: "support.html",
    maintenance: "maintenance.html",
    knowledge: "training-talks.html",
    training: "training.html",
    talks: "talks.html",
    contact: "contact.html",
    imprint: "legal-notice.html",
  },
};

const navigation = {
  de: {
    skip: "Zum Inhalt springen",
    menu: "Menü",
    homeLabel: "derico.de Startseite",
    services: {
      label: "Leistungen",
      intro: "Anwendungsentwicklung mit offenem Fundament und einem klaren Plan für die Jahre nach dem Start.",
      overview: "Alle Leistungen",
      proof: "Zwanzig Jahre Python-Erfahrung fließen in Architektur, Betrieb und Weiterentwicklung ein.",
      links: [
        ["odoo", "Odoo", "Geschäftsprozesse verbinden und dauerhaft weiterentwickeln", [["odooDevelopment", "Entwicklung"], ["odooConsulting", "Beratung"], ["odooOperations", "Betrieb"]]],
        ["plone", "Plone", "Inhalte, Workflows und Berechtigungen verlässlich organisieren"],
        ["python", "Django, Pyramid & FastAPI", "Passende Python-Architekturen für individuelle Anwendungen"],
      ],
    },
    sustainability: "Nachhaltigkeit",
    care: {
      label: "Support & Wartung",
      intro: "Verlässliche Betreuung für Anwendungen, die täglich gebraucht werden und mit ihrer Aufgabe wachsen.",
      overview: "Support & Wartung im Überblick",
      proof: "Pflege bleibt planbar: Zuständigkeiten, Reaktionswege und Upgrade-Zyklen werden gemeinsam festgelegt.",
      links: [
        ["support", "Support", "Direkte Hilfe durch Menschen, die Anwendung und Betrieb verstehen"],
        ["maintenance", "Wartung", "Updates, Sicherheit und technische Erneuerung mit langfristigem Horizont"],
      ],
    },
    knowledge: {
      label: "Schulungen & Vorträge",
      intro: "Erfahrung wird nutzbar, wenn Teams Zusammenhänge verstehen und Entscheidungen selbst tragen können.",
      overview: "Wissen weitergeben",
      proof: "Schulungen entstehen aus realen Projekten und Beiträgen zur Open-Source-Community.",
      links: [
        ["training", "Schulungen", "Formate für Teams, Administrator:innen und Entwickler:innen"],
        ["talks", "Vorträge", "Konferenzbeiträge, Themen und buchbare Sessions"],
      ],
    },
    contact: "Kontakt",
    firstTalk: "Erstgespräch vereinbaren",
    contactLead: "Sie schildern die Aufgabe. Wir klären gemeinsam, welcher nächste Schritt sinnvoll ist.",
    email: "E-Mail schreiben",
    location: "Neuhaus/Elbe · Deutschland",
    footerLine: "Nachhaltige Lösungen für Anwendungen, die bleiben.",
    imprint: "Impressum",
  },
  en: {
    skip: "Skip to content",
    menu: "Menu",
    homeLabel: "derico.de home",
    services: {
      label: "Services",
      intro: "Application development with an open foundation and a clear plan for the years after launch.",
      overview: "All services",
      proof: "Twenty years of Python experience inform architecture, operations and continued development.",
      links: [
        ["odoo", "Odoo", "Connect business processes and develop them sustainably", [["odooDevelopment", "Development"], ["odooConsulting", "Consulting"], ["odooOperations", "Operations"]]],
        ["plone", "Plone", "Organise content, workflows and permissions reliably"],
        ["python", "Django, Pyramid & FastAPI", "Purpose-fit Python architectures for individual applications"],
      ],
    },
    sustainability: "Sustainability",
    care: {
      label: "Support & maintenance",
      intro: "Dependable care for applications that matter every day and continue to grow with their task.",
      overview: "Support & maintenance overview",
      proof: "Care stays predictable: responsibilities, response paths and upgrade cycles are agreed together.",
      links: [
        ["support", "Support", "Direct help from people who understand the application and its operations"],
        ["maintenance", "Maintenance", "Updates, security and technical renewal with a long horizon"],
      ],
    },
    knowledge: {
      label: "Training & talks",
      intro: "Experience becomes useful when teams understand the connections and can carry decisions themselves.",
      overview: "Sharing knowledge",
      proof: "Training grows from real projects and contributions to open-source communities.",
      links: [
        ["training", "Training", "Formats for teams, administrators and developers"],
        ["talks", "Talks", "Conference sessions, topics and bookable presentations"],
      ],
    },
    contact: "Contact",
    firstTalk: "Arrange an initial conversation",
    contactLead: "Tell us about the task. Together, we identify a useful next step.",
    email: "Write an email",
    location: "Neuhaus/Elbe · Germany",
    footerLine: "Sustainable solutions for applications, grown to last.",
    imprint: "Legal notice",
  },
};

const pages = {
  de: {
    home: {
      type: "home",
      title: "Anwendungen, die bleiben.",
      context: "Nachhaltige Lösungen, seit über 20 Jahren",
      lede: "Wir entwickeln Geschäftsanwendungen auf Basis von Python, modernem JavaScript und Open Source. Wartbarkeit, offene Standards und klare Entscheidungen sichern ihren Wert über viele Jahre.",
    },
    services: {
      type: "overview",
      title: "Anwendungsentwicklung mit langem Horizont.",
      context: "Leistungen",
      lede: "Technologie ist tragfähig, wenn sie zur Aufgabe passt, verständlich bleibt und zuverlässig weiterentwickelt werden kann.",
      introTitle: "Drei erprobte Grundlagen",
      intro: "Wir wählen Frameworks nach Prozess, Organisation und Lebensdauer der Anwendung. Architektur, Benutzeroberfläche und Betrieb werden dabei als zusammenhängende Aufgabe geplant.",
      children: ["odoo", "plone", "python"],
    },
    odoo: {
      type: "detail",
      title: "Odoo verbindet Ihre Geschäftsprozesse.",
      context: "Leistungen · Odoo",
      lede: "Wir führen Odoo ein, entwickeln Module nach offenen OCA-Standards und halten das System über Versionswechsel hinweg anschlussfähig.",
      fit: "Vertrieb, Einkauf, Lager und Abrechnung",
      foundation: "Odoo · Python · OCA",
      horizon: "Einführung, Module und Upgrades",
      bodyTitle: "Ein System, das den tatsächlichen Ablauf trägt",
      body: [
        "Eine Odoo-Einführung beginnt mit den Arbeitsschritten, Zuständigkeiten und Daten, die Ihr Team täglich bewegt. Daraus entsteht eine klare Modulgrenze und eine Einführung in sinnvollen Etappen.",
        "Eigene Erweiterungen folgen den Konventionen der Odoo Community Association. Das erleichtert Tests, Reviews und spätere Versionswechsel. Dokumentierte Entscheidungen halten die Anwendung auch für neue Teammitglieder verständlich.",
      ],
      deliverables: ["Prozess- und Modulkonzept", "OCA-konforme Erweiterungen", "Datenmigration und Schnittstellen", "Einführung, Schulung und Upgrade-Plan"],
      childrenTitle: "Odoo-Leistungen im Detail",
      children: ["odooDevelopment", "odooConsulting", "odooOperations"],
      quote: "Eine ERP-Einführung trägt, wenn Teams ihre tägliche Arbeit darin wiederfinden und jede Erweiterung einen nachvollziehbaren Platz hat.",
      proofLinks: [["https://odoo-community.org/", "Odoo Community Association"], ["knowledge", "Schulungen für Ihr Odoo-Team"]],
    },
    odooDevelopment: {
      type: "detail",
      title: "Odoo-Entwicklung für klare Prozesse.",
      context: "Leistungen · Odoo · Entwicklung",
      lede: "Wir entwickeln Odoo-Module und Schnittstellen, die fachliche Abläufe präzise abbilden und sich sauber weiterentwickeln lassen.",
      fit: "Individuelle Abläufe, Integrationen und Erweiterungen",
      foundation: "Odoo · Python · OCA-Standards",
      horizon: "Konzeption, Umsetzung und Weiterentwicklung",
      bodyTitle: "Erweiterungen mit einem klaren Platz im System",
      body: [
        "Am Anfang stehen die Fachbegriffe, Regeln und Datenflüsse des Prozesses. Wir ordnen die Anforderungen den passenden Odoo-Modulen zu und definieren klare Grenzen für eigene Erweiterungen.",
        "Module folgen den Konventionen der Odoo Community Association. Automatisierte Tests, nachvollziehbare Migrationen und dokumentierte Schnittstellen halten die Anwendung über Release-Wechsel hinweg verständlich.",
      ],
      deliverables: ["Individuelle Odoo-Module", "Schnittstellen zu Drittsystemen", "Automatisierte Tests und Migrationen", "Technische Dokumentation und Reviews"],
      quote: "Gute Odoo-Entwicklung übersetzt fachliche Regeln in Module, die Teams verstehen und langfristig pflegen können.",
      proofLinks: [["odoo", "Odoo im Überblick"], ["contact", "Entwicklungsvorhaben besprechen"]],
    },
    odooConsulting: {
      type: "detail",
      title: "Odoo-Beratung verbindet Prozesse und System.",
      context: "Leistungen · Odoo · Beratung",
      lede: "Wir klären Ziele, Prozesse und Verantwortlichkeiten und entwickeln daraus einen belastbaren Weg für Einführung oder Weiterentwicklung.",
      fit: "Einführungen, Erweiterungen und bestehende Odoo-Systeme",
      foundation: "Prozessanalyse · Modulkonzept · Odoo",
      horizon: "Vom Zielbild bis zur umsetzbaren Roadmap",
      bodyTitle: "Entscheidungen auf Grundlage der täglichen Arbeit",
      body: [
        "In Workshops erfassen wir Arbeitsabläufe, Rollen, Daten und Schnittstellen gemeinsam mit den beteiligten Teams. Daraus entsteht ein Zielbild mit nachvollziehbaren Prioritäten und Etappen.",
        "Bestehende Installationen prüfen wir anhand ihrer Module, Anpassungen, Datenqualität und Betriebswege. Die Ergebnisse werden als konkrete Entscheidungen, Risiken und nächste Schritte dokumentiert.",
      ],
      deliverables: ["Prozess- und Anforderungsworkshops", "Modul- und Einführungskonzept", "Analyse bestehender Installationen", "Priorisierte Roadmap und Aufwandseinschätzung"],
      quote: "Eine tragfähige Odoo-Entscheidung beginnt mit einem gemeinsamen Verständnis von Prozess, Verantwortung und Ziel.",
      proofLinks: [["odooDevelopment", "Odoo-Entwicklung"], ["contact", "Beratungsbedarf einordnen"]],
    },
    odooOperations: {
      type: "detail",
      title: "Odoo-Betrieb hält Anwendungen verlässlich verfügbar.",
      context: "Leistungen · Odoo · Betrieb",
      lede: "Wir planen Deployment, Überwachung, Backups und Updates als zusammenhängenden Betriebsweg für Ihre Odoo-Anwendung.",
      fit: "Produktive Odoo-Anwendungen mit verlässlichen Betriebsanforderungen",
      foundation: "Odoo · Linux · automatisierte Deployments",
      horizon: "Laufender Betrieb und vorbereitete Versionswechsel",
      bodyTitle: "Betrieb mit klaren Zuständigkeiten und überprüfbaren Wegen",
      body: [
        "Gemeinsam legen wir Umgebungen, Zugriffswege, Sicherungen, Überwachung und Wiederherstellung fest. Automatisierte Deployments sorgen dafür, dass Änderungen reproduzierbar in Test- und Produktivsysteme gelangen.",
        "Updates und Release-Wechsel werden früh geplant und unter realistischen Bedingungen geprüft. Status, Risiken und notwendige Entscheidungen bleiben für verantwortliche Personen transparent.",
      ],
      deliverables: ["Betriebs- und Deploymentkonzept", "Monitoring, Backups und Wiederherstellung", "Staging- und Produktivumgebungen", "Update- und Upgrade-Planung"],
      quote: "Verlässlicher Betrieb macht den Zustand einer Anwendung sichtbar und jeden notwendigen Eingriff nachvollziehbar.",
      proofLinks: [["maintenance", "Wartung über Release-Zyklen"], ["contact", "Betrieb besprechen"]],
    },
    plone: {
      type: "detail",
      title: "Plone für Inhalte mit Verantwortung.",
      context: "Leistungen · Plone",
      lede: "Wir bauen und modernisieren Plone-Anwendungen für Organisationen, die verlässliche Workflows, Berechtigungen und lange Wartungszeiträume benötigen.",
      fit: "Portale, Wissensplattformen und Intranets",
      foundation: "Plone · Python · offene Standards",
      horizon: "Konzeption, Migration und Pflege",
      bodyTitle: "Struktur für anspruchsvolle Inhalte",
      body: [
        "Plone verbindet ein ausgereiftes Inhaltsmodell mit fein steuerbaren Rollen und Arbeitsabläufen. Wir übersetzen fachliche Zuständigkeiten in eine Architektur, die Redaktionen sicher bedienen und Entwickler:innen sauber erweitern können.",
        "Bei bestehenden Installationen analysieren wir Erweiterungen, Inhalte und Betriebswege. Migrationen werden in überprüfbaren Schritten geplant, damit Redaktionen weiterarbeiten und Entscheidungen nachvollziehen können.",
      ],
      deliverables: ["Informationsarchitektur und Workflows", "Individuelle Inhaltstypen und Integrationen", "Barrierearme Benutzeroberflächen", "Upgrades und Migrationen"],
      quote: "Unsere Plone-Werkzeuge werden upstream genutzt. Diese Nähe zur Community verbessert jede Kundenanwendung.",
      proofLinks: [["https://github.com/plone/plonecli", "plonecli auf GitHub"], ["https://github.com/plone/bobtemplates.plone", "bobtemplates.plone auf GitHub"]],
    },
    python: {
      type: "detail",
      title: "Python-Architektur passend zur Aufgabe.",
      context: "Leistungen · Django, Pyramid & FastAPI",
      lede: "Django, Pyramid und FastAPI decken unterschiedliche Aufgaben ab. Wir wählen die Grundlage nach Domäne, Team, Schnittstellen und erwarteter Lebensdauer.",
      fit: "Fachanwendungen, APIs und Integrationen",
      foundation: "Django · Pyramid · FastAPI",
      horizon: "Architektur, Entwicklung und Betrieb",
      bodyTitle: "Eine klare Domäne im Mittelpunkt",
      body: [
        "Am Anfang stehen Begriffe, Regeln und Abläufe der Fachdomäne. Darauf bauen Datenmodell, Schnittstellen und Benutzeroberfläche auf. Der gewählte Rahmen unterstützt diese Struktur und bleibt für das Team nachvollziehbar.",
        "Automatisierte Tests, reproduzierbare Deployments und dokumentierte Entscheidungen gehören zur Anwendung. So bleiben Änderungen beherrschbar, wenn Anforderungen, Team oder Infrastruktur wachsen.",
      ],
      deliverables: ["Domänen- und Systemarchitektur", "Webanwendungen und APIs", "Schnittstellen und Datenmigration", "Tests, Deployment und technische Dokumentation"],
      quote: "Bewährte Python-Werkzeuge geben uns die Freiheit, die Architektur an der Aufgabe auszurichten.",
      proofLinks: [["https://www.djangoproject.com/", "Django"], ["https://fastapi.tiangolo.com/", "FastAPI"], ["https://trypyramid.com/", "Pyramid"]],
    },
    sustainability: {
      type: "sustainability",
      title: "Nachhaltigkeit entsteht in der Architektur.",
      context: "Nachhaltigkeit",
      lede: "Eine nachhaltige Anwendung bleibt verständlich, sicher, aktualisierbar und übertragbar. Diese Eigenschaften werden von Beginn an geplant und regelmäßig gepflegt.",
    },
    care: {
      type: "overview",
      title: "Verantwortung über den Start hinaus.",
      context: "Support & Wartung",
      lede: "Betriebssicherheit wächst aus klaren Zuständigkeiten, kurzen Wegen und einer Wartung, die technische Entwicklungen früh einplant.",
      introTitle: "Zwei Aufgaben, ein verlässlicher Rahmen",
      intro: "Support löst konkrete Fragen im laufenden Betrieb. Wartung hält die technische Basis gesund. Beide Leistungen werden so kombiniert, wie Ihre Anwendung und Ihr Team sie benötigen.",
      children: ["support", "maintenance"],
    },
    support: {
      type: "detail",
      title: "Support mit direktem Weg zur Lösung.",
      context: "Support & Wartung · Support",
      lede: "Anfragen erreichen Menschen, die Ihre Anwendung, ihre Architektur und ihren Betrieb kennen. Das verkürzt die Analyse und macht Antworten belastbar.",
      fit: "Produktive Anwendungen und verantwortliche Teams",
      foundation: "Vereinbarte Wege und Zuständigkeiten",
      horizon: "Laufende Begleitung",
      bodyTitle: "Hilfe mit Kontext",
      body: [
        "Gemeinsam legen wir fest, wer Anfragen stellt, wie Dringlichkeit bewertet wird und welche Informationen die Analyse beschleunigen. Kritische Situationen erhalten einen klaren Eskalationsweg.",
        "Wiederkehrende Fragen fließen in Dokumentation, Schulung oder technische Verbesserungen ein. Support trägt dadurch zur Qualität der gesamten Anwendung bei.",
      ],
      deliverables: ["Definierte Kontakt- und Eskalationswege", "Nachvollziehbare Bearbeitung", "Analyse von Fehlern und Betriebsfragen", "Rückfluss in Dokumentation und Wartung"],
      quote: "Guter Support kennt den Unterschied zwischen einer schnellen Antwort und einer tragfähigen Lösung.",
      proofLinks: [["maintenance", "Wartung ergänzend planen"], ["contact", "Supportbedarf besprechen"]],
    },
    maintenance: {
      type: "detail",
      title: "Wartung hält Anwendungen beweglich.",
      context: "Support & Wartung · Wartung",
      lede: "Regelmäßige Updates, Sicherheitsarbeit und vorbereitete Versionswechsel erhalten die Handlungsfähigkeit Ihrer Anwendung.",
      fit: "Langfristig betriebene Geschäftsanwendungen",
      foundation: "Tests, Updates und Upgrade-Zyklen",
      horizon: "Planbar über Jahre",
      bodyTitle: "Technische Pflege mit Übersicht",
      body: [
        "Wir beobachten Abhängigkeiten, Sicherheitsmeldungen und Release-Zyklen. Notwendige Änderungen werden nach Risiko und Nutzen priorisiert und in einem gemeinsamen Wartungsplan sichtbar gemacht.",
        "Größere Upgrades werden früh vorbereitet. Automatisierte Tests und Staging-Umgebungen schaffen Sicherheit, bevor eine neue Version den produktiven Betrieb erreicht.",
      ],
      deliverables: ["Abhängigkeits- und Sicherheitsupdates", "Regelmäßige technische Zustandsberichte", "Test- und Staging-Strategie", "Geplante Versionswechsel und Migrationen"],
      quote: "Jedes gepflegte Release fügt der Anwendung einen weiteren gesunden Ring hinzu.",
      proofLinks: [["sustainability", "Unsere Nachhaltigkeitsprinzipien"], ["contact", "Wartungsbedarf einordnen"]],
    },
    knowledge: {
      type: "overview",
      title: "Wissen, das im Team weiterarbeitet.",
      context: "Schulungen & Vorträge",
      lede: "Wir vermitteln Zusammenhänge aus realen Projekten, geben erprobte Arbeitsweisen weiter und schaffen Raum für konkrete Fragen.",
      introTitle: "Lernen im passenden Format",
      intro: "Schulungen bearbeiten die Anwendung und das Team im Detail. Vorträge verdichten Erfahrungen zu einem klaren Thema und eröffnen die Diskussion.",
      children: ["training", "talks"],
    },
    training: {
      type: "training",
      title: "Schulungen für die nächste sichere Entscheidung.",
      context: "Schulungen & Vorträge · Schulungen",
      lede: "Von der kompakten Einführung bis zum mehrtägigen Teamformat: Inhalte, Übungen und Beispiele richten sich nach Vorkenntnissen und tatsächlicher Anwendung.",
    },
    talks: {
      type: "talks",
      title: "Vorträge aus gelebter Entwicklungspraxis.",
      context: "Schulungen & Vorträge · Vorträge",
      lede: "Konferenzbeiträge und buchbare Sessions zu Plone, Python, nachhaltiger Architektur und der Arbeit in Open-Source-Communities.",
    },
    contact: {
      type: "contact",
      title: "Erzählen Sie uns von Ihrer Anwendung.",
      context: "Kontakt",
      lede: "Ein erstes Gespräch ist kostenlos. Wir hören zu, ordnen die Aufgabe ein und benennen einen sinnvollen nächsten Schritt — auf Deutsch oder Englisch, remote oder in Neuhaus/Elbe.",
    },
    imprint: {
      type: "imprint",
      title: "Impressum",
      context: "Impressum",
      lede: "Angaben zum Anbieter dieser Website und Nachweise für verwendete Inhalte.",
    },
  },
  en: {
    home: {
      type: "home",
      title: "Applications, grown to last.",
      context: "Sustainable solutions for more than 20 years",
      lede: "We develop business applications with Python, modern JavaScript and open source. Maintainability, open standards and clear decisions protect their value for years to come.",
    },
    services: {
      type: "overview",
      title: "Application development with a long horizon.",
      context: "Services",
      lede: "Technology carries its task when it fits the organisation, stays understandable and can be developed reliably.",
      introTitle: "Three proven foundations",
      intro: "We select frameworks according to process, organisation and expected lifetime. Architecture, interface and operations are planned as one connected task.",
      children: ["odoo", "plone", "python"],
    },
    odoo: {
      type: "detail",
      title: "Odoo connects your business processes.",
      context: "Services · Odoo",
      lede: "We introduce Odoo, develop modules to open OCA standards and keep the system ready for future releases.",
      fit: "Sales, purchasing, warehouse and invoicing",
      foundation: "Odoo · Python · OCA",
      horizon: "Introduction, modules and upgrades",
      bodyTitle: "A system that carries the real process",
      body: [
        "An Odoo introduction begins with the steps, responsibilities and data your team moves every day. This creates clear module boundaries and a rollout in useful stages.",
        "Custom extensions follow Odoo Community Association conventions. That improves testing, review and later upgrades. Documented decisions keep the application understandable as the team changes.",
      ],
      deliverables: ["Process and module concept", "OCA-compliant extensions", "Data migration and integrations", "Introduction, training and upgrade plan"],
      childrenTitle: "Odoo services in detail",
      children: ["odooDevelopment", "odooConsulting", "odooOperations"],
      quote: "An ERP system carries its value when teams recognise their daily work and each extension has a clear place.",
      proofLinks: [["https://odoo-community.org/", "Odoo Community Association"], ["knowledge", "Training for your Odoo team"]],
    },
    odooDevelopment: {
      type: "detail",
      title: "Odoo development for clear processes.",
      context: "Services · Odoo · Development",
      lede: "We develop Odoo modules and integrations that represent business processes precisely and remain ready for continued development.",
      fit: "Individual processes, integrations and extensions",
      foundation: "Odoo · Python · OCA standards",
      horizon: "Concept, implementation and continued development",
      bodyTitle: "Extensions with a clear place in the system",
      body: [
        "The work begins with the domain language, rules and data flows of the process. We map requirements to suitable Odoo modules and define clear boundaries for custom extensions.",
        "Modules follow Odoo Community Association conventions. Automated tests, traceable migrations and documented interfaces keep the application understandable across release changes.",
      ],
      deliverables: ["Custom Odoo modules", "Integrations with third-party systems", "Automated tests and migrations", "Technical documentation and reviews"],
      quote: "Good Odoo development translates domain rules into modules teams can understand and maintain over the long term.",
      proofLinks: [["odoo", "Odoo overview"], ["contact", "Discuss a development project"]],
    },
    odooConsulting: {
      type: "detail",
      title: "Odoo consulting connects processes and system.",
      context: "Services · Odoo · Consulting",
      lede: "We clarify goals, processes and responsibilities and turn them into a dependable path for introduction or continued development.",
      fit: "Introductions, extensions and existing Odoo systems",
      foundation: "Process analysis · module concept · Odoo",
      horizon: "From target state to an actionable roadmap",
      bodyTitle: "Decisions grounded in daily work",
      body: [
        "In workshops, we capture processes, roles, data and integrations with the teams involved. The result is a target state with traceable priorities and delivery stages.",
        "We assess existing installations through their modules, customisations, data quality and operational paths. Findings become documented decisions, risks and concrete next steps.",
      ],
      deliverables: ["Process and requirements workshops", "Module and introduction concept", "Assessment of existing installations", "Prioritised roadmap and effort estimate"],
      quote: "A durable Odoo decision begins with a shared understanding of process, responsibility and purpose.",
      proofLinks: [["odooDevelopment", "Odoo development"], ["contact", "Discuss your consulting needs"]],
    },
    odooOperations: {
      type: "detail",
      title: "Odoo operations keep applications reliably available.",
      context: "Services · Odoo · Operations",
      lede: "We plan deployment, monitoring, backups and updates as one connected operational path for your Odoo application.",
      fit: "Production Odoo applications with dependable operational requirements",
      foundation: "Odoo · Linux · automated deployments",
      horizon: "Continuous operations and prepared release changes",
      bodyTitle: "Operations with clear ownership and verifiable paths",
      body: [
        "Together we define environments, access paths, backups, monitoring and recovery. Automated deployments move changes reproducibly into staging and production systems.",
        "Updates and release changes are planned early and tested under realistic conditions. Status, risks and required decisions remain transparent for responsible roles.",
      ],
      deliverables: ["Operations and deployment concept", "Monitoring, backups and recovery", "Staging and production environments", "Update and upgrade planning"],
      quote: "Dependable operations make an application's condition visible and every necessary intervention traceable.",
      proofLinks: [["maintenance", "Maintenance across release cycles"], ["contact", "Discuss operations"]],
    },
    plone: {
      type: "detail",
      title: "Plone for content with responsibility.",
      context: "Services · Plone",
      lede: "We build and modernise Plone applications for organisations that need dependable workflows, permissions and long maintenance horizons.",
      fit: "Portals, knowledge platforms and intranets",
      foundation: "Plone · Python · open standards",
      horizon: "Concept, migration and care",
      bodyTitle: "Structure for demanding content",
      body: [
        "Plone combines a mature content model with precise roles and workflows. We translate responsibilities into an architecture editors can use safely and developers can extend cleanly.",
        "For existing installations, we analyse extensions, content and operations. Migrations proceed in verifiable stages so editorial work can continue and decisions remain traceable.",
      ],
      deliverables: ["Information architecture and workflows", "Custom content types and integrations", "Accessible interfaces", "Upgrades and migrations"],
      quote: "Our Plone tools are used upstream. That closeness to the community improves every client application.",
      proofLinks: [["https://github.com/plone/plonecli", "plonecli on GitHub"], ["https://github.com/plone/bobtemplates.plone", "bobtemplates.plone on GitHub"]],
    },
    python: {
      type: "detail",
      title: "Python architecture fitted to the task.",
      context: "Services · Django, Pyramid & FastAPI",
      lede: "Django, Pyramid and FastAPI address different needs. We choose the foundation around domain, team, integrations and expected lifetime.",
      fit: "Business applications, APIs and integrations",
      foundation: "Django · Pyramid · FastAPI",
      horizon: "Architecture, development and operations",
      bodyTitle: "A clear domain at the centre",
      body: [
        "The work starts with the terms, rules and processes of the domain. Data, interfaces and user experience grow from that model. The selected framework supports the structure and stays readable for the team.",
        "Automated tests, reproducible deployment and documented decisions belong to the application. Change remains manageable as requirements, team and infrastructure grow.",
      ],
      deliverables: ["Domain and system architecture", "Web applications and APIs", "Integrations and data migration", "Tests, deployment and technical documentation"],
      quote: "Proven Python tools let us align architecture with the real task.",
      proofLinks: [["https://www.djangoproject.com/", "Django"], ["https://fastapi.tiangolo.com/", "FastAPI"], ["https://trypyramid.com/", "Pyramid"]],
    },
    sustainability: {
      type: "sustainability",
      title: "Sustainability starts in the architecture.",
      context: "Sustainability",
      lede: "A sustainable application remains understandable, secure, upgradable and transferable. These qualities are planned from the start and maintained throughout its life.",
    },
    care: {
      type: "overview",
      title: "Responsibility beyond launch.",
      context: "Support & maintenance",
      lede: "Operational confidence grows from clear ownership, short paths and maintenance that plans technical change early.",
      introTitle: "Two tasks, one dependable framework",
      intro: "Support resolves concrete questions in daily operation. Maintenance keeps the technical foundation healthy. We combine both around your application and team.",
      children: ["support", "maintenance"],
    },
    support: {
      type: "detail",
      title: "Support with a direct path to resolution.",
      context: "Support & maintenance · Support",
      lede: "Requests reach people who know your application, architecture and operations. Analysis becomes faster and answers become more reliable.",
      fit: "Production applications and responsible teams",
      foundation: "Agreed paths and ownership",
      horizon: "Continuous guidance",
      bodyTitle: "Help with context",
      body: [
        "Together we define who raises requests, how urgency is assessed and which information speeds analysis. Critical situations receive a clear escalation path.",
        "Recurring questions feed documentation, training or technical improvements. Support therefore contributes to the quality of the whole application.",
      ],
      deliverables: ["Defined contact and escalation paths", "Traceable handling", "Analysis of faults and operational questions", "Feedback into documentation and maintenance"],
      quote: "Good support understands the difference between a quick answer and a durable resolution.",
      proofLinks: [["maintenance", "Plan complementary maintenance"], ["contact", "Discuss your support needs"]],
    },
    maintenance: {
      type: "detail",
      title: "Maintenance keeps applications adaptable.",
      context: "Support & maintenance · Maintenance",
      lede: "Regular updates, security work and prepared release changes preserve your application's ability to move.",
      fit: "Long-running business applications",
      foundation: "Tests, updates and upgrade cycles",
      horizon: "Predictable across years",
      bodyTitle: "Technical care with visibility",
      body: [
        "We monitor dependencies, security notices and release cycles. Necessary changes are prioritised by risk and value and remain visible in a shared maintenance plan.",
        "Larger upgrades are prepared early. Automated tests and staging environments create confidence before a new release reaches production.",
      ],
      deliverables: ["Dependency and security updates", "Regular technical health reports", "Test and staging strategy", "Planned upgrades and migrations"],
      quote: "Every maintained release adds another healthy ring to the application.",
      proofLinks: [["sustainability", "Our sustainability principles"], ["contact", "Assess your maintenance needs"]],
    },
    knowledge: {
      type: "overview",
      title: "Knowledge that keeps working in the team.",
      context: "Training & talks",
      lede: "We share connections from real projects, pass on proven practices and create room for specific questions.",
      introTitle: "Learning in the right format",
      intro: "Training explores the application and team in detail. Talks focus experience into a clear subject and open the discussion.",
      children: ["training", "talks"],
    },
    training: {
      type: "training",
      title: "Training for the next confident decision.",
      context: "Training & talks · Training",
      lede: "From a focused introduction to a multi-day team format: content, exercises and examples reflect existing knowledge and the real application.",
    },
    talks: {
      type: "talks",
      title: "Talks grounded in development practice.",
      context: "Training & talks · Talks",
      lede: "Conference contributions and bookable sessions on Plone, Python, sustainable architecture and work in open-source communities.",
    },
    contact: {
      type: "contact",
      title: "Tell us about your application.",
      context: "Contact",
      lede: "An initial conversation is free. We listen, assess the task and identify a useful next step — in German or English, remotely or in Neuhaus/Elbe.",
    },
    imprint: {
      type: "imprint",
      title: "Legal notice",
      context: "Legal notice",
      lede: "Provider information for this website and credits for licensed content.",
    },
  },
};

const groupFor = (key) => {
  if (["services", "odoo", "odooDevelopment", "odooConsulting", "odooOperations", "plone", "python"].includes(key)) return "services";
  if (["care", "support", "maintenance"].includes(key)) return "care";
  if (["knowledge", "training", "talks"].includes(key)) return "knowledge";
  return null;
};

const href = (lang, key) => slugs[lang][key];
const resolvedHref = (lang, value) => (slugs[lang][value] ? href(lang, value) : value);

function megaPanel(lang, name, current) {
  const item = navigation[lang][name];
  return `<div class="mega-panel" id="mega-${name}" data-mega-panel hidden>
    <div class="mega-inner">
      <div class="mega-intro">
        <h2><a href="${href(lang, name)}">${item.label}</a></h2>
        <p>${item.intro}</p>
        <a class="mega-overview" href="${href(lang, name)}">${item.overview}</a>
      </div>
      <ul class="mega-links">
        ${item.links.map(([key, title, text, children = []]) => `<li><a href="${href(lang, key)}"${current === key ? ' aria-current="page"' : ""}><span><strong>${title}</strong><span>${text}</span></span></a>${children.length ? `<ul class="mega-sublinks" aria-label="${title}">${children.map(([childKey, childTitle]) => `<li><a href="${href(lang, childKey)}"${current === childKey ? ' aria-current="page"' : ""}>${childTitle}</a></li>`).join("")}</ul>` : ""}</li>`).join("")}
      </ul>
      <p class="mega-proof">${item.proof}</p>
    </div>
  </div>`;
}

function header(lang, current) {
  const nav = navigation[lang];
  const group = groupFor(current);
  const currentAttr = (key) => (current === key ? ' aria-current="page"' : "");
  const groupClass = (key) => (group === key ? " is-current" : "");
  return `<a class="skip-link" href="#main">${nav.skip}</a>
  <header class="site-header" data-site-header data-nav-open="false">
    <div class="header-shell shell">
      <a class="brand-mark" href="${href(lang, "home")}" aria-label="${nav.homeLabel}">
        <img src="../assets/derico-logo.svg" alt="" width="423" height="146">
      </a>
      <button class="menu-toggle" type="button" data-menu-toggle aria-controls="site-navigation" aria-expanded="false">
        <span class="menu-toggle__icon" aria-hidden="true"></span><span>${nav.menu}</span>
      </button>
      <nav class="site-nav" id="site-navigation" aria-label="${lang === "de" ? "Hauptnavigation" : "Primary navigation"}">
        <ul class="primary-nav">
          <li>
            <button class="nav-trigger${groupClass("services")}" type="button" data-mega-trigger aria-expanded="false" aria-controls="mega-services">${nav.services.label}</button>
            ${megaPanel(lang, "services", current)}
          </li>
          <li><a class="nav-link" href="${href(lang, "sustainability")}"${currentAttr("sustainability")}>${nav.sustainability}</a></li>
          <li>
            <button class="nav-trigger${groupClass("care")}" type="button" data-mega-trigger aria-expanded="false" aria-controls="mega-care">${nav.care.label}</button>
            ${megaPanel(lang, "care", current)}
          </li>
          <li>
            <button class="nav-trigger${groupClass("knowledge")}" type="button" data-mega-trigger aria-expanded="false" aria-controls="mega-knowledge">${nav.knowledge.label}</button>
            ${megaPanel(lang, "knowledge", current)}
          </li>
          <li><a class="nav-link" href="${href(lang, "contact")}"${currentAttr("contact")}>${nav.contact}</a></li>
        </ul>
      </nav>
      <ul class="utility-nav" aria-label="${lang === "de" ? "Sprachauswahl" : "Language selection"}">
        <li><a href="../de/${slugs.de[current]}"${lang === "de" ? ' aria-current="page"' : ""} lang="de">DE</a></li>
        <li aria-hidden="true">/</li>
        <li><a href="../en/${slugs.en[current]}"${lang === "en" ? ' aria-current="page"' : ""} lang="en">EN</a></li>
      </ul>
    </div>
    <button class="mega-backdrop" type="button" data-mega-backdrop hidden aria-label="${lang === "de" ? "Menü schließen" : "Close menu"}"></button>
  </header>`;
}

function breadcrumbs(lang, key, label) {
  if (key === "home") return "";
  const home = lang === "de" ? "Startseite" : "Home";
  const group = groupFor(key);
  const groupLabel = group ? navigation[lang][group].label : null;
  const groupCrumb = group && group !== key ? `<li><a href="${href(lang, group)}">${groupLabel}</a></li>` : "";
  const odooChildren = ["odooDevelopment", "odooConsulting", "odooOperations"];
  const parentCrumb = odooChildren.includes(key) ? `<li><a href="${href(lang, "odoo")}">Odoo</a></li>` : "";
  return `<nav class="breadcrumbs" aria-label="${lang === "de" ? "Brotkrümelnavigation" : "Breadcrumb"}"><div class="shell"><ol><li><a href="${href(lang, "home")}">${home}</a></li>${groupCrumb}${parentCrumb}<li aria-current="page">${label}</li></ol></div></nav>`;
}

function footer(lang) {
  const nav = navigation[lang];
  return `<footer class="site-footer"><div class="shell footer-grid">
    <div><p><strong>derico</strong> · ${nav.footerLine}</p><p>Maik Derstappen · Laaver Weg 2 · 19273 Neuhaus/Elbe</p></div>
    <ul class="footer-links"><li><a href="tel:+491788612833">+49 178 861 2 833</a></li><li><a href="mailto:md@derico.de">md@derico.de</a></li><li><a href="${href(lang, "imprint")}">${nav.imprint}</a></li></ul>
  </div></footer>`;
}

function rings(lang) {
  const labels = lang === "de"
    ? [["schneller Prototyp", "in Wochen bedienbar"], ["erste Anwendung", "trägt die tägliche Arbeit"], ["erfahrener Begleiter", "wächst mit den Anforderungen"], ["mit der Zeit gegangen", "offen, aktuell, migrierbar"]]
    : [["rapid prototype", "usable within weeks"], ["first application", "supports daily work"], ["experienced companion", "grows with requirements"], ["kept current", "open, maintained, portable"]];
  return `<figure class="rings-figure">
    <div class="rings-stage">
      <svg class="rings-disc" viewBox="0 0 680 470" role="img" aria-label="${lang === "de" ? "Wachstumsringe einer Anwendung" : "Growth rings of an application"}">
        <g transform="translate(105 0)">
          <circle cx="150" cy="235" r="40" class="ring-thin"/>
          <circle cx="153" cy="232" r="80"/>
          <circle cx="147" cy="238" r="125" class="ring-thin"/>
          <circle cx="154" cy="231" r="170"/>
          <circle cx="148" cy="237" r="215" class="ring-thin"/>
          <circle cx="152" cy="234" r="250"/>
          <circle cx="150" cy="235" r="290" class="ring-now"/>
          <circle cx="151" cy="234" r="315" class="ring-future"/>
        </g>
      </svg>
      <ol class="ring-markers" aria-hidden="true"><li>1</li><li>2</li><li>3</li><li class="is-now">4</li></ol>
    </div>
    <dl class="ring-legend">${labels.map(([title, text], index) => `<div${index === 3 ? ' class="is-now"' : ""}><b>${index + 1}</b><dt>${title}</dt><dd>${text}</dd></div>`).join("")}</dl>
  </figure>`;
}

function pageHero(page) {
  return `<section class="page-hero"><div class="shell page-hero__grid"><div><p class="page-context">${page.context}</p><h1>${page.title}</h1></div><p class="lede">${page.lede}</p></div></section>`;
}

function contactBand(lang) {
  const nav = navigation[lang];
  return `<section class="contact-band"><div class="shell"><h2>${nav.firstTalk}</h2><p>${nav.contactLead}</p><div class="action-row"><a class="button" href="${href(lang, "contact")}">${nav.contact}</a><a class="quiet-link" href="mailto:md@derico.de">${nav.email}</a></div></div></section>`;
}

function heroMedia() {
  return `<picture class="hero-media" aria-hidden="true">
    <source media="(max-width: 55.99rem)" type="image/avif" srcset="../assets/images/hero-managed-forest-portrait-720.avif 720w, ../assets/images/hero-managed-forest-portrait-1080.avif 1080w" sizes="100vw">
    <source media="(max-width: 55.99rem)" type="image/webp" srcset="../assets/images/hero-managed-forest-portrait-720.webp 720w, ../assets/images/hero-managed-forest-portrait-1080.webp 1080w" sizes="100vw">
    <source type="image/avif" srcset="../assets/images/hero-managed-forest-wide-960.avif 960w, ../assets/images/hero-managed-forest-wide-1600.avif 1600w, ../assets/images/hero-managed-forest-wide-2400.avif 2400w" sizes="100vw">
    <source type="image/webp" srcset="../assets/images/hero-managed-forest-wide-960.webp 960w, ../assets/images/hero-managed-forest-wide-1600.webp 1600w, ../assets/images/hero-managed-forest-wide-2400.webp 2400w" sizes="100vw">
    <source media="(max-width: 55.99rem)" type="image/jpeg" srcset="../assets/images/hero-managed-forest-portrait-720.jpg 720w, ../assets/images/hero-managed-forest-portrait-1080.jpg 1080w" sizes="100vw">
    <img src="../assets/images/hero-managed-forest-wide-1600.jpg" srcset="../assets/images/hero-managed-forest-wide-960.jpg 960w, ../assets/images/hero-managed-forest-wide-1600.jpg 1600w, ../assets/images/hero-managed-forest-wide-2400.jpg 2400w" sizes="100vw" width="2400" height="1200" alt="" fetchpriority="high" decoding="async">
  </picture><div class="hero-wash" aria-hidden="true"></div>`;
}

function serviceDiagram(kind) {
  const diagrams = {
    care: `<svg viewBox="0 0 240 120" aria-hidden="true" focusable="false">
      <g class="diagram-surface">
        <rect x="67" y="22" width="106" height="62" rx="3" />
        <path d="M82 84v15h76V84" />
      </g>
      <g class="diagram-lines">
        <path d="M84 39h72M84 52h48M84 65h58" />
        <path d="M43 45v45c0 11 9 20 20 20h114c11 0 20-9 20-20V45" />
      </g>
      <g class="diagram-accent">
        <circle cx="43" cy="39" r="6" /><circle cx="197" cy="39" r="6" />
        <path d="M111 98h18M120 89v18" />
      </g>
    </svg>`,
  };
  return diagrams[kind];
}

function guideGraphic(lang, subject, className) {
  return `<img class="${className}" src="../assets/images/${subject}_${lang}.png" width="1254" height="1254" alt="" loading="lazy" decoding="async">`;
}

function renderServiceGuide(lang) {
  const isDe = lang === "de";
  const copy = isDe ? {
    heading: "Ein Bestimmungsbuch unserer Arbeit.",
    intro: "Zwei Plattformen, spezialisierte Frameworks und eine Betreuung, die Anwendungen über ihren gesamten Lebenszyklus begleitet.",
    label: "Technische Grundlagen und Betreuung",
    action: "Mehr erfahren",
    odooPurpose: "Geschäftsanwendungen",
    odooText: "Geschäftsanwendungen für verbundene Prozesse – von Vertrieb und Einkauf bis Lager und Abrechnung.",
    plonePurpose: "Sichere Inhaltsplattformen",
    ploneText: "Sichere Inhaltsplattformen für Redaktionen, Gruppen, Workflows und fein abgestufte Berechtigungen.",
    frameworksTitle: "Spezialisierte Frameworks",
    frameworksPurpose: "Fokussiert auf die konkrete Aufgabe",
    frameworksText: "Mit Django, Pyramid, FastAPI und SvelteKit entwickeln wir fokussierte Anwendungen für spezialisierte Anforderungen.",
    careTitle: "Support & Wartung",
    carePurpose: "Begleitung über den gesamten Lebenszyklus",
    careText: "Support, Updates und Migration für Anwendungen im täglichen Betrieb.",
  } : {
    heading: "A field guide to our work.",
    intro: "Two platforms, specialised frameworks and dependable care across the complete application lifecycle.",
    label: "Technical foundations and ongoing care",
    action: "Learn more",
    odooPurpose: "Business applications",
    odooText: "Business applications for connected processes, from sales and purchasing to inventory and accounting.",
    plonePurpose: "Secure content platforms",
    ploneText: "Secure content platforms for editorial teams, groups, workflows and finely controlled permissions.",
    frameworksTitle: "Specialised frameworks",
    frameworksPurpose: "Focused on the task at hand",
    frameworksText: "We use Django, Pyramid, FastAPI and SvelteKit to build focused applications for specialised requirements.",
    careTitle: "Support & maintenance",
    carePurpose: "Care across the complete lifecycle",
    careText: "Support, updates and migration for applications in daily operation.",
  };
  const action = `<span class="service-action">${copy.action}<span aria-hidden="true">→</span></span>`;
  return `<section class="section services-guide-section" aria-labelledby="services-guide-title"><div class="shell">
    <div class="services-guide-header"><h2 class="section-heading" id="services-guide-title">${copy.heading}</h2><p class="section-intro">${copy.intro}</p></div>
    <nav class="service-atlas" aria-label="${copy.label}">
      <div class="service-platforms">
        <a class="service-node service-platform service-platform--odoo" href="${href(lang, "odoo")}">
          <span class="service-platform__disc">${guideGraphic(lang, "odoo", "service-platform-graphic")}<h3 class="visually-hidden">Odoo · ${copy.odooPurpose}</h3></span>
          <span class="service-copy">${copy.odooText}</span>${action}
        </a>
        <a class="service-node service-platform service-platform--plone" href="${href(lang, "plone")}">
          <span class="service-platform__disc">${guideGraphic(lang, "plone", "service-platform-graphic")}<h3 class="visually-hidden">Plone · ${copy.plonePurpose}</h3></span>
          <span class="service-copy">${copy.ploneText}</span>${action}
        </a>
      </div>
      <a class="service-node service-frameworks" href="${href(lang, "python")}">
        ${guideGraphic(lang, "frameworks", "service-frameworks-graphic")}
        <h3 class="visually-hidden">${copy.frameworksTitle}</h3><span class="visually-hidden">${copy.frameworksPurpose}. Django, Pyramid, FastAPI, SvelteKit. ${copy.frameworksText}</span>${action}
      </a>
      <a class="service-node service-care" href="${href(lang, "care")}">
        <svg class="service-care__cradle" viewBox="0 0 1000 250" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M24 10c42 178 168 224 476 224S934 188 976 10"/><circle cx="24" cy="10" r="7"/><circle cx="976" cy="10" r="7"/></svg>
        <span class="service-care__content"><span class="service-illustration">${serviceDiagram("care")}</span><span><span class="service-purpose">${copy.carePurpose}</span><h3>${copy.careTitle}</h3><span class="service-copy">${copy.careText}</span>${action}</span></span>
      </a>
    </nav>
  </div></section>`;
}

function renderHome(lang, page) {
  const nav = navigation[lang];
  const manifesto = lang === "de" ? [
    ["Solide und durchdacht", "Bewährte Frameworks, wenige Abhängigkeiten und dokumentierte Entscheidungen schaffen Anwendungen, die im Alltag zuverlässig funktionieren."],
    ["Arbeit wird spürbar leichter", "Unsere Lösungen unterstützen Teams in ihren Abläufen und erhöhen die Produktivität und Qualität der Ergebnisse."],
    ["Offene Standards sichern den Wert", "Open Source und offene Schnittstellen halten Systeme zugänglich, erweiterbar und übertragbar."],
    ["Pflege ist Teil der Architektur", "Updates, Sicherheitsarbeit und Migration werden früh mitgedacht und über Jahre planbar gemacht."],
  ] : [
    ["Solid and considered", "Proven frameworks, limited dependencies and documented decisions create applications that work reliably in daily use."],
    ["Work becomes noticeably easier", "Our solutions support teams in their processes and improve productivity and the quality of their results."],
    ["Open standards protect value", "Open source and open interfaces keep systems accessible, extensible and transferable."],
    ["Care belongs in the architecture", "Updates, security work and migration are planned early and made predictable across years."],
  ];
  return `<section class="home-hero">${heroMedia()}<div class="shell home-hero__grid"><div><p class="kicker">${page.context}</p><h1>${page.title}</h1><p class="lede">${page.lede}</p><div class="action-row"><a class="button" href="${href(lang, "contact")}">${nav.firstTalk}</a><a class="quiet-link" href="${href(lang, "services")}">${nav.services.overview}</a></div></div>${rings(lang)}</div></section>
  <section class="section section--band"><div class="shell"><h2 class="section-heading">${lang === "de" ? "Nachhaltige Anwendungen sind eine Investition, die trägt." : "Sustainable applications are investments that keep delivering."}</h2><div class="manifesto-grid">${manifesto.map(([title, text]) => `<article class="manifesto-item"><h3>${title}</h3><p>${text}</p></article>`).join("")}</div></div></section>
  ${renderServiceGuide(lang)}`;
}

function renderIndex(lang, children) {
  const descriptions = {
    de: {
      odoo: "ERP und eigene Module für verbundene Geschäftsprozesse.", odooDevelopment: "Individuelle Module und Schnittstellen nach OCA-Standards.", odooConsulting: "Prozesse, Anforderungen und Einführungsschritte gemeinsam klären.", odooOperations: "Deployment, Monitoring, Backups und Updates verlässlich organisieren.", plone: "Inhaltsplattformen mit Workflows, Berechtigungen und langer Lebensdauer.", python: "Individuelle Anwendungen und APIs mit Django, Pyramid oder FastAPI.", care: "Support, Updates und Migration für Anwendungen im täglichen Betrieb.", support: "Direkte Hilfe mit Kenntnis von Architektur und Betrieb.", maintenance: "Planbare technische Pflege über Release-Zyklen hinweg.", training: "Praxisnahe Formate für Teams und Verantwortliche.", talks: "Vorträge zu Plone, Python, Open Source und nachhaltiger Architektur.",
    },
    en: {
      odoo: "ERP and custom modules for connected business processes.", odooDevelopment: "Custom modules and integrations following OCA standards.", odooConsulting: "Clarify processes, requirements and introduction stages together.", odooOperations: "Organise deployment, monitoring, backups and updates reliably.", plone: "Content platforms with workflows, permissions and a long service life.", python: "Individual applications and APIs with Django, Pyramid or FastAPI.", care: "Support, updates and migration for applications in daily operation.", support: "Direct help with knowledge of architecture and operations.", maintenance: "Predictable technical care across release cycles.", training: "Practical formats for teams and responsible roles.", talks: "Talks about Plone, Python, open source and sustainable architecture.",
    },
  };
  const action = lang === "de" ? "Mehr erfahren" : "Learn more";
  return `<dl class="section-index">${children.map((key) => `<div class="section-index__row"><dt><a href="${href(lang, key)}">${pages[lang][key].context.split(" · ").at(-1)}</a></dt><dd>${descriptions[lang][key]}<br><a class="section-index__action" href="${href(lang, key)}">${action} →</a></dd></div>`).join("")}</dl>`;
}

function renderOverview(lang, page) {
  return `${pageHero(page)}<section class="section"><div class="shell"><h2 class="section-heading">${page.introTitle}</h2><p class="section-intro">${page.intro}</p>${renderIndex(lang, page.children)}</div></section>`;
}

function renderDetail(lang, page) {
  const labels = lang === "de" ? ["Geeignet für", "Technische Grundlage", "Zeithorizont"] : ["Suitable for", "Technical foundation", "Horizon"];
  const deliverablesTitle = lang === "de" ? "Was wir gemeinsam erarbeiten" : "What we build together";
  const childPages = page.children?.length
    ? `<section class="section section--soft"><div class="shell"><h2 class="section-heading">${page.childrenTitle}</h2>${renderIndex(lang, page.children)}</div></section>`
    : "";
  return `${pageHero(page)}<section class="section"><div class="shell detail-grid"><div class="prose"><h2>${page.bodyTitle}</h2>${page.body.map((text) => `<p>${text}</p>`).join("")}<h2>${deliverablesTitle}</h2><ul>${page.deliverables.map((item) => `<li>${item}</li>`).join("")}</ul></div><dl class="detail-aside"><dt>${labels[0]}</dt><dd>${page.fit}</dd><dt>${labels[1]}</dt><dd>${page.foundation}</dd><dt>${labels[2]}</dt><dd>${page.horizon}</dd></dl></div></section>${childPages}<section class="section section--band"><div class="shell proof-band"><blockquote>“${page.quote}”<cite>— ${lang === "de" ? "Arbeitsprinzip, derico" : "Working principle, derico"}</cite></blockquote><div class="proof-links">${page.proofLinks.map(([target, label]) => `<a href="${resolvedHref(lang, target)}"${target.startsWith("http") ? ' rel="external"' : ""}>${label}</a>`).join("")}</div></div></section>`;
}

function renderSustainability(lang, page) {
  const steps = lang === "de" ? [
    ["Verstehen", "Fachbegriffe, Verantwortlichkeiten und echte Arbeitsabläufe bilden die Grundlage der Architektur."],
    ["Offen bauen", "Offene Standards, dokumentierte Schnittstellen und verfügbare Quelltexte erhalten Wahlfreiheit."],
    ["Pflegen", "Updates, Sicherheitsarbeit und technische Zustandsberichte halten die Anwendung gesund."],
    ["Erneuern", "Versionswechsel und Migrationen werden vorbereitet, getestet und nachvollziehbar umgesetzt."],
  ] : [
    ["Understand", "Domain language, responsibilities and real working processes form the architectural foundation."],
    ["Build openly", "Open standards, documented interfaces and available source code preserve choice."],
    ["Maintain", "Updates, security work and technical health reports keep the application healthy."],
    ["Renew", "Release changes and migrations are prepared, tested and implemented transparently."],
  ];
  const mechanisms = lang === "de" ? [
    ["Wartbarkeit", "Klare Module, Tests und Dokumentation senken die Kosten jeder späteren Änderung."],
    ["Sicherheit", "Regelmäßige Updates und überprüfbare Betriebswege begrenzen technische Risiken."],
    ["Übertragbarkeit", "Offene Formate und Standards halten einen Wechsel von Betrieb oder Partner möglich."],
    ["Effizienz", "Schlanke Auslieferung und angemessene Infrastruktur reduzieren laufenden Aufwand."],
  ] : [
    ["Maintainability", "Clear modules, tests and documentation reduce the cost of every later change."],
    ["Security", "Regular updates and verifiable operations limit technical risk."],
    ["Portability", "Open formats and standards keep a change of operator or partner possible."],
    ["Efficiency", "Lean delivery and proportionate infrastructure reduce ongoing effort."],
  ];
  return `${pageHero(page)}<section class="section"><div class="shell detail-grid"><div><h2 class="section-heading">${lang === "de" ? "Vier wiederkehrende Aufgaben" : "Four recurring responsibilities"}</h2><ol class="sequence">${steps.map(([title, text]) => `<li><div><h3>${title}</h3><p>${text}</p></div></li>`).join("")}</ol></div><div class="detail-aside"><p class="page-context">${lang === "de" ? "Der Maßstab" : "The measure"}</p><p>${lang === "de" ? "Eine Anwendung bleibt wertvoll, wenn Menschen sie verstehen, sicher betreiben und ohne Sackgasse weiterentwickeln können." : "An application keeps its value when people can understand it, operate it safely and continue its development without a dead end."}</p></div></div></section><section class="section section--band"><div class="shell"><h2 class="section-heading">${lang === "de" ? "Mechanismen, die den Anspruch belegen" : "Mechanisms that support the claim"}</h2><div class="manifesto-grid">${mechanisms.map(([title, text]) => `<article class="manifesto-item"><h3>${title}</h3><p>${text}</p></article>`).join("")}</div></div></section>`;
}

function renderTraining(lang, page) {
  const formats = lang === "de" ? [
    ["Team-Workshop", "Ein bis zwei Tage", "Gemeinsames Verständnis für Architektur, Arbeitsweise oder eine anstehende Entscheidung."],
    ["Technische Schulung", "Ein bis drei Tage", "Plone, Odoo, Python oder Svelte mit Übungen an realistischen Beispielen."],
    ["Begleitendes Mentoring", "Über mehrere Wochen", "Regelmäßige Sessions zu Fragen, Reviews und der Anwendung des Gelernten im Projekt."],
  ] : [
    ["Team workshop", "One to two days", "Shared understanding of architecture, working practices or an upcoming decision."],
    ["Technical training", "One to three days", "Plone, Odoo, Python or Svelte with exercises based on realistic examples."],
    ["Ongoing mentoring", "Across several weeks", "Regular sessions for questions, reviews and applying learning within the project."],
  ];
  return `${pageHero(page)}<section class="section"><div class="shell"><h2 class="section-heading">${lang === "de" ? "Formate nach Aufgabe und Team" : "Formats fitted to task and team"}</h2><ul class="talk-list">${formats.map(([title, meta, text]) => `<li><p class="talk-meta">${meta}</p><h3>${title}</h3><p>${text}</p></li>`).join("")}</ul></div></section><section class="section section--soft"><div class="shell proof-band"><div><h2 class="section-heading">${lang === "de" ? "Vorbereitung mit echtem Kontext" : "Preparation with real context"}</h2><p class="section-intro">${lang === "de" ? "Vorab klären wir Ziele, Vorkenntnisse und die eingesetzte Anwendung. Materialien und Übungen werden anschließend für Ihr Team zusammengestellt." : "Beforehand we clarify goals, existing knowledge and the application in use. Materials and exercises are then assembled for your team."}</p></div><div class="proof-links"><a href="${href(lang, "contact")}">${lang === "de" ? "Schulung anfragen" : "Request training"}</a><a href="${href(lang, "talks")}">${lang === "de" ? "Vortragsthemen ansehen" : "View talk topics"}</a></div></div></section>`;
}

function renderTalks(lang, page) {
  const talks = lang === "de" ? [
    ["Konferenzbeitrag", "Anwendungen, die bleiben", "Welche Architekturentscheidungen Wartbarkeit, Upgradefähigkeit und offene Übergaben über viele Jahre ermöglichen."],
    ["Plone & Python", "Werkzeuge, die eine Community weiterträgt", "Erfahrungen aus plonecli, bobtemplates.plone und der Zusammenarbeit in offenen Projekten."],
    ["Team & Technik", "Vom Prototyp zur gepflegten Anwendung", "Wie Domänenmodell, Tests, Betrieb und Verantwortung gemeinsam mit dem Produkt wachsen."],
  ] : [
    ["Conference session", "Applications, grown to last", "Architectural decisions that support maintenance, upgrades and open handovers across many years."],
    ["Plone & Python", "Tools carried forward by a community", "Experience from plonecli, bobtemplates.plone and collaboration in open projects."],
    ["Team & technology", "From prototype to maintained application", "How domain model, tests, operations and responsibility grow with the product."],
  ];
  return `${pageHero(page)}<section class="section"><div class="shell"><h2 class="section-heading">${lang === "de" ? "Aktuelle Themen" : "Current topics"}</h2><ul class="talk-list">${talks.map(([meta, title, text]) => `<li><p class="talk-meta">${meta}</p><h3>${title}</h3><p>${text}</p></li>`).join("")}</ul></div></section><section class="section section--soft"><div class="shell empty-state"><h3>${lang === "de" ? "Neue Termine werden nach Bestätigung veröffentlicht." : "New dates are published once confirmed."}</h3><p>${lang === "de" ? "Für eine Veranstaltung oder ein internes Format können Sie ein Thema direkt anfragen." : "You can request a topic directly for an event or an internal session."}</p><div class="action-row"><a class="button" href="${href(lang, "contact")}">${lang === "de" ? "Vortrag anfragen" : "Request a talk"}</a></div></div></section>`;
}

function renderContact(lang, page) {
  const isDe = lang === "de";
  return `${pageHero(page)}<section class="section"><div class="shell contact-layout"><div class="contact-direct"><h2 class="section-heading">${isDe ? "Direkt erreichbar" : "Reach us directly"}</h2><p class="section-intro">${isDe ? "Maik Derstappen antwortet persönlich. In der Regel erhalten Sie innerhalb von zwei Werktagen eine Rückmeldung." : "Maik Derstappen replies personally. You will usually hear back within two working days."}</p><a href="mailto:md@derico.de">md@derico.de</a><dl class="contact-details"><div><dt>${isDe ? "Telefon" : "Phone"}</dt><dd><a href="tel:+491788612833">+49 178 861 2 833</a></dd></div><div><dt>${isDe ? "Standort" : "Location"}</dt><dd>Laaver Weg 2<br>19273 Neuhaus/Elbe<br>${isDe ? "Deutschland" : "Germany"}</dd></div><div><dt>${isDe ? "Gespräch" : "Conversation"}</dt><dd>${isDe ? "Deutsch oder Englisch · remote oder vor Ort" : "German or English · remote or on site"}</dd></div></dl></div><form class="contact-form" data-contact-form novalidate><h2>${isDe ? "E-Mail vorbereiten" : "Prepare an email"}</h2><p class="muted">${isDe ? "Das Formular öffnet Ihr E-Mail-Programm. Ihre Angaben werden nicht an diese Vorschau übertragen." : "The form opens your email application. Your details are not transmitted to this preview."}</p>${formField(lang, "name", isDe ? "Ihr Name" : "Your name", "text", true)}${formField(lang, "company", isDe ? "Unternehmen" : "Company", "text", false)}${formField(lang, "email", isDe ? "Ihre E-Mail-Adresse" : "Your email address", "email", true)}<div class="form-field"><label for="topic">${isDe ? "Thema" : "Topic"}</label><select id="topic" name="topic"><option>${isDe ? "Neue Anwendung" : "New application"}</option><option>Odoo</option><option>Plone</option><option>Django, Pyramid & FastAPI</option><option>${isDe ? "Support & Wartung" : "Support & maintenance"}</option><option>${isDe ? "Schulung oder Vortrag" : "Training or talk"}</option></select></div><div class="form-field"><label for="message">${isDe ? "Worum geht es?" : "What would you like to discuss?"}</label><textarea id="message" name="message" data-required aria-describedby="message-error" placeholder="${isDe ? "Aufgabe, heutiger Stand und gewünschter nächster Schritt" : "Task, current situation and desired next step"}"></textarea><p class="field-error" id="message-error" hidden></p></div><button class="button" type="submit">${isDe ? "E-Mail im eigenen Programm öffnen" : "Open email in your application"}</button><p class="form-note">${isDe ? "Pflichtfelder: Name, E-Mail-Adresse und Nachricht." : "Required: name, email address and message."}</p><p class="form-status" data-form-status role="status" tabindex="-1" hidden></p></form></div></section>`;
}

function formField(lang, id, label, type, required) {
  return `<div class="form-field"><label for="${id}">${label}</label><input id="${id}" name="${id}" type="${type}"${required ? ` data-required aria-describedby="${id}-error"` : ""}>${required ? `<p class="field-error" id="${id}-error" hidden></p>` : ""}</div>`;
}

function renderImprint(lang, page) {
  const isDe = lang === "de";
  return `${pageHero(page)}<section class="section"><div class="shell"><div class="prose"><h2>${isDe ? "Anbieter" : "Provider"}</h2><p>Maik Derstappen<br>Laaver Weg 2<br>19273 Neuhaus/Elbe<br>${isDe ? "Deutschland" : "Germany"}</p><h2>${isDe ? "Kontakt" : "Contact"}</h2><p>${isDe ? "Telefon" : "Phone"}: <a href="tel:+491788612833">+49 178 861 2 833</a><br>${isDe ? "E-Mail" : "Email"}: <a href="mailto:md@derico.de">md@derico.de</a></p><h2>${isDe ? "Bildnachweis" : "Image credit"}</h2><p>${isDe ? "Das Hintergrundfoto der Startseite stammt von" : "The homepage background photograph is by"} <a href="https://unsplash.com/photos/brown-and-green-trees-on-brown-grass-field-during-daytime-hZX4tYgljUI" rel="external">Kat Closon</a>${isDe ? " und wird unter der" : " and is used under the"} <a href="https://unsplash.com/license" rel="external">Unsplash License</a>${isDe ? " verwendet." : "."}</p></div></div></section>`;
}

function renderBody(lang, page) {
  if (page.type === "home") return renderHome(lang, page);
  if (page.type === "overview") return renderOverview(lang, page);
  if (page.type === "detail") return renderDetail(lang, page);
  if (page.type === "sustainability") return renderSustainability(lang, page);
  if (page.type === "training") return renderTraining(lang, page);
  if (page.type === "talks") return renderTalks(lang, page);
  if (page.type === "contact") return renderContact(lang, page);
  if (page.type === "imprint") return renderImprint(lang, page);
  throw new Error(`Unknown page type: ${page.type}`);
}

function document(lang, key, page) {
  const description = page.lede.replace(/<[^>]+>/g, "");
  const includeContact = !["contact", "imprint"].includes(key);
  const heroPreload = key === "home" ? `
  <link rel="preload" as="image" href="../assets/images/hero-managed-forest-portrait-720.avif" imagesrcset="../assets/images/hero-managed-forest-portrait-720.avif 720w, ../assets/images/hero-managed-forest-portrait-1080.avif 1080w" imagesizes="100vw" type="image/avif" media="(max-width: 55.99rem)">
  <link rel="preload" as="image" href="../assets/images/hero-managed-forest-wide-1600.avif" imagesrcset="../assets/images/hero-managed-forest-wide-960.avif 960w, ../assets/images/hero-managed-forest-wide-1600.avif 1600w, ../assets/images/hero-managed-forest-wide-2400.avif 2400w" imagesizes="100vw" type="image/avif" media="(min-width: 56rem)">` : "";
  return `<!doctype html>
<html lang="${lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="${description}">
  <meta name="theme-color" content="#fafcfd">
  <title>${page.title} · derico</title>
  <link rel="preload" href="../assets/fonts/source-sans-3-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>${heroPreload}
  <link rel="stylesheet" href="../assets/site.css">
  <script>document.documentElement.classList.add("js")</script>
  <script src="../assets/site.js" defer></script>
</head>
<body>
  ${header(lang, key)}
  ${breadcrumbs(lang, key, page.context.split(" · ").at(-1))}
  <main id="main">${renderBody(lang, page)}</main>
  ${includeContact ? contactBand(lang) : ""}
  ${footer(lang)}
</body>
</html>`;
}

for (const lang of ["de", "en"]) {
  await mkdir(join(root, lang), { recursive: true });
  for (const [key, page] of Object.entries(pages[lang])) {
    await writeFile(join(root, lang, slugs[lang][key]), document(lang, key, page));
  }
  const isDe = lang === "de";
  const errorDocument = `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>${isDe ? "Seite nicht gefunden" : "Page not found"} · derico</title><link rel="stylesheet" href="../assets/site.css"><script>document.documentElement.classList.add("js")</script><script src="../assets/site.js" defer></script></head><body>${header(lang, "home")}<main id="main" class="error-page"><div class="shell error-page__inner"><p class="error-page__code">404</p><h1>${isDe ? "Diese Seite ist nicht mehr hier." : "This page is no longer here."}</h1><p>${isDe ? "Die Adresse kann veraltet sein. Über die Leistungen oder die Startseite finden Sie einen neuen Weg." : "The address may be outdated. Services or the home page will give you a current route."}</p><div class="action-row"><a class="button" href="${href(lang, "home")}">${isDe ? "Zur Startseite" : "Go to home"}</a><a class="quiet-link" href="${href(lang, "services")}">${navigation[lang].services.overview}</a></div></div></main>${footer(lang)}</body></html>`;
  await writeFile(join(root, lang, "404.html"), errorDocument);
}

await writeFile(join(root, "index.html"), `<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0; url=de/index.html"><title>derico</title></head><body><p><a href="de/index.html">derico.de öffnen</a> · <a href="en/index.html" lang="en">Open derico.de in English</a></p></body></html>`);

console.log(`Built ${Object.keys(pages.de).length * 2 + 3} static documents in ${root}`);
