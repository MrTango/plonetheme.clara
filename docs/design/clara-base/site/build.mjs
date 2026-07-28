#!/usr/bin/env node
// Generates the clara-base demo pages. Run: node build.mjs
// The emitted HTML files are committed; this script only keeps the shared
// header, footer and CTA band identical across pages.
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));

const ploneLogo = `<img class="brand-logo" src="assets/images/plone-logo.svg" width="215" height="56" alt="">`;

const communityPanel = (current) => `<div class="mega-panel" id="mega-community" data-mega-panel hidden>
    <div class="mega-inner">
      <div class="mega-intro">
        <h2><a href="community.html">Community</a></h2>
        <p>Plone is built, documented and secured by a worldwide open-source community. Meet it where it works.</p>
        <a class="mega-overview" href="community.html">Community overview</a>
      </div>
      <ul class="mega-links">
        <li><a href="forum.html"${current === "forum" ? ' aria-current="page"' : ""}><span><strong>Forum</strong><span>Questions and answers in the open, from users to core developers</span></span></a></li>
        <li><a href="sprints.html"${current === "sprints" ? ' aria-current="page"' : ""}><span><strong>Sprints</strong><span>Focused development meetings where the platform moves forward</span></span></a></li>
        <li><a href="conferences.html"${current === "conferences" ? ' aria-current="page"' : ""}><span><strong>Conferences</strong><span>The annual Plone Conference and community days worldwide</span></span></a></li>
      </ul>
      <p class="mega-proof">Hundreds of contributors, one steady release cadence: Plone has shipped since 2001.</p>
    </div>
  </div>`;

const header = (current) => {
  const communityCurrent = ["community", "forum", "sprints", "conferences"].includes(current);
  const link = (href, key, label) =>
    `<a class="nav-link" href="${href}"${current === key ? ' aria-current="page"' : ""}>${label}</a>`;
  return `<header class="site-header" data-site-header data-nav-open="false">
    <div class="header-shell shell">
      <a class="brand-mark" href="index.html" aria-label="Plone Blicca Theme Clara home">${ploneLogo}</a>
      <button class="menu-toggle" type="button" data-menu-toggle aria-controls="site-navigation" aria-expanded="false">
        <span class="menu-toggle__icon" aria-hidden="true"></span><span>Menu</span>
      </button>
      <nav class="site-nav" id="site-navigation" aria-label="Primary navigation">
        <ul class="primary-nav">
          <li>${link("index.html", "home", "Home")}</li>
          <li>${link("why-plone.html", "why-plone", "Why Plone")}</li>
          <li>${link("secure-content.html", "secure-content", "Secure Content")}</li>
          <li>
            <button class="nav-trigger${communityCurrent ? " is-current" : ""}" type="button" data-mega-trigger aria-expanded="false" aria-controls="mega-community">Community</button>
            ${communityPanel(current)}
          </li>
        </ul>
      </nav>
      <ul class="utility-nav" aria-label="Related sites">
        <li><a href="https://plone.org" rel="external">plone.org</a></li>
      </ul>
    </div>
    <button class="mega-backdrop" type="button" data-mega-backdrop hidden aria-label="Close menu"></button>
  </header>`;
};

const ctaBand = `<section class="cta-band"><div class="shell"><h2>Open source, open to you.</h2><p>Plone is free software: download it, try the demo and bring your questions along.</p><div class="action-row"><a class="button" href="https://plone.org" rel="external">Get Plone</a><a class="quiet-link" href="forum.html">Ask in the forum</a></div></div></section>`;

const footer = `<footer class="site-footer"><div class="shell footer-grid">
    <div><p><strong>Clara</strong> · A lightweight theme for Plone. Content, secure in every sense.</p><p>Demo content — built with and for the Plone community.</p></div>
    <ul class="footer-links"><li><a href="https://plone.org" rel="external">plone.org</a></li><li><a href="https://community.plone.org" rel="external">community.plone.org</a></li><li><a href="https://docs.plone.org" rel="external">docs.plone.org</a></li></ul>
  </div></footer>`;

const breadcrumbs = (items) =>
  `<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="shell"><ol>${items
    .map(([label, href]) =>
      href ? `<li><a href="${href}">${label}</a></li>` : `<li aria-current="page">${label}</li>`,
    )
    .join("")}</ol></div></nav>`;

const page = ({ file, title, description, current, crumbs, main, extraHead = "" }) => `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="description" content="${description}">
  <meta name="theme-color" content="#fbfcfd">
  <title>${title}</title>
  <link rel="preload" href="assets/fonts/source-sans-3-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
${extraHead}  <link rel="stylesheet" href="assets/site.css">
  <script>document.documentElement.classList.add("js")</script>
  <script src="assets/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  ${header(current)}
  ${crumbs ? breadcrumbs(crumbs) : ""}
  <main id="main">${main}</main>
  ${ctaBand}
  ${footer}
</body>
</html>`;

/* ---------------------------------------------------------------- home */

const structureFigure = `<figure class="structure-figure">
      <div class="structure-stage">
        <svg class="structure-svg" viewBox="0 0 560 350" role="img" aria-label="A content tree: one site root branching into sections; one section holds three documents in the workflow states private, pending review and published.">
          <g class="tree-lines">
            <path class="tree-line" d="M280 42 140 150M280 42v108M280 42l140 108"/>
            <path class="tree-line" d="M420 150 340 278M420 150v128M420 150l80 128"/>
          </g>
          <circle class="tree-node" cx="280" cy="42" r="26"/>
          <circle class="tree-node" cx="140" cy="150" r="22"/>
          <circle class="tree-node" cx="280" cy="150" r="22"/>
          <circle class="tree-node" cx="420" cy="150" r="22"/>
          <circle class="tree-node" cx="340" cy="278" r="18"/>
          <circle class="tree-node tree-node--pending" cx="420" cy="278" r="18"/>
          <circle class="tree-node tree-node--published" cx="500" cy="278" r="18"/>
        </svg>
      </div>
      <dl class="state-legend">
        <div><span class="state-dot" aria-hidden="true"></span><dt>Private</dt><dd>visible to its owners and editors only</dd></div>
        <div class="is-pending"><span class="state-dot" aria-hidden="true"></span><dt>Pending review</dt><dd>submitted, waiting for a reviewer's decision</dd></div>
        <div class="is-published"><span class="state-dot" aria-hidden="true"></span><dt>Published</dt><dd>public — the state readers actually see</dd></div>
      </dl>
    </figure>
    <p class="structure-note"><a class="quiet-link" href="secure-content.html">How states and permissions work together</a></p>`;

const homeMain = `<section class="home-hero"><div class="shell home-hero__grid"><div><p class="kicker">Theme Clara for Plone Blicca</p><h1>Content, secure in every sense.</h1><p class="lede">Plone is the open-source CMS for organisations that publish with responsibility: workflow and permissions protect every item, migrations carry it across versions, and the REST API keeps it open.</p><div class="action-row"><a class="button" href="secure-content.html">What secure content means</a><a class="quiet-link" href="why-plone.html">Why Plone</a></div></div><figure class="hero-figure">
    <picture>
      <source type="image/webp" srcset="assets/images/plone_en.webp">
      <img src="assets/images/plone_en.png" width="1254" height="1254" alt="Diagram: Plone, a great choice for content-heavy platforms — multiple editors and groups, powerful content workflows, granular permissions and roles, great user experience, built for content at scale. Loved by editors, trusted by developers." fetchpriority="high" decoding="async">
    </picture>
    <figcaption>Why teams pick Plone, at a glance.</figcaption>
  </figure></div></section>
  <section class="section section--band"><div class="shell"><h2 class="section-heading">A CMS that takes content seriously.</h2><div class="manifesto-grid"><article class="manifesto-item"><h3>Protected by the platform</h3><p>Workflow states and granular permissions decide who sees, changes and publishes every single item.</p></article><article class="manifesto-item"><h3>Durable across versions</h3><p>Six major releases since 2001, each with migration steps that carry existing content safely forward.</p></article><article class="manifesto-item"><h3>Open through the REST API</h3><p>Everything in the site reads and writes as structured JSON — for any front end, integration or export.</p></article><article class="manifesto-item"><h3>Built for content at scale</h3><p>Hundreds of thousands of pages, files and records stay organised in one consistent content tree.</p></article></div></div></section>
  <section class="section structure-section" aria-labelledby="structure-title"><div class="shell"><h2 class="section-heading" id="structure-title">Every item knows its place — and its state.</h2><p class="section-intro">Clara's namesake is clarity: content lives in one tree, and each item carries a workflow state everyone can read.</p>${structureFigure}</div></section>
  <section class="section section--soft" aria-labelledby="index-title"><div class="shell"><h2 class="section-heading" id="index-title">Start where it matters.</h2><dl class="section-index"><div class="section-index__row"><dt><a href="why-plone.html">Why Plone</a></dt><dd>The case for Plone: editors, workflows, scale and a track record reaching back to 2001.<br><a class="section-index__action" href="why-plone.html">Read the case</a></dd></div><div class="section-index__row"><dt><a href="secure-content.html">Secure Content</a></dt><dd>Protected by permissions and workflow, durable across version upgrades, open through the REST API.<br><a class="section-index__action" href="secure-content.html">See what secure means</a></dd></div><div class="section-index__row"><dt><a href="community.html">Community</a></dt><dd>Forum, sprints and conferences: the people behind the platform.<br><a class="section-index__action" href="community.html">Meet the community</a></dd></div></dl></div></section>`;

/* ----------------------------------------------------------- why plone */

const whyPloneMain = `<section class="page-hero"><div class="shell page-hero__grid"><div><p class="page-context">The case for Plone</p><h1>A great choice for content-heavy platforms.</h1></div><p class="lede">Plone pairs a mature content model with editorial workflows and permissions that scale from a single site to hundreds.</p></div></section>
  <section class="section"><div class="shell detail-grid"><div class="prose"><h2>Editors first</h2><p>Plone was built for the people who work in it every day. Editors write, arrange and publish in the same structure readers navigate; reviewers see exactly what waits for them; administrators delegate without giving everything away.</p><p>That is what "loved by editors, trusted by developers" means in practice: the daily work is comfortable, and the platform underneath is a real application server with typed content, an addressable API and a disciplined upgrade path.</p><h2>A platform, not a page builder</h2><p>Content in Plone is structured data, not fragments of layout. Every item has a type, a place in the tree, a workflow state and a history. On top of that foundation you get:</p><ul><li>Custom content types without programming</li><li>Editorial workflows you can adapt to your organisation</li><li>A complete REST API for any front end</li><li>Documented migrations that carry content across major releases</li><li>Versioning, staging and full-text search built in</li><li>Accessibility as a project standard, not an afterthought</li></ul><p>Two of those points carry Plone's secure-content promise: migrations keep your content <a href="secure-content.html#durable">durable across versions</a>, and the REST API keeps it <a href="secure-content.html#open">open to you at any time</a>.</p></div><dl class="detail-aside"><dt>Suitable for</dt><dd>Portals, intranets and knowledge platforms</dd><dt>Foundation</dt><dd>Python · open standards · REST API</dd><dt>License</dt><dd>Free and open source (GPL)</dd><dt>First release</dt><dd>2001, with a steady cadence since</dd></dl></div></section>
  <section class="section section--band" aria-labelledby="six-title"><div class="shell"><h2 class="section-heading" id="six-title">Six reasons, in short.</h2><div class="manifesto-grid"><article class="manifesto-item"><h3>Multiple editors and groups</h3><p>Teams, departments and external partners work side by side, each with their own reach.</p></article><article class="manifesto-item"><h3>Powerful content workflows</h3><p>Submission, review and publication follow rules your organisation defines once and relies on daily.</p></article><article class="manifesto-item"><h3>Granular permissions and roles</h3><p>Access control follows the content tree and can be tightened for one folder or one document.</p></article><article class="manifesto-item"><h3>Great user experience</h3><p>Editing happens in context, with modern UI and sensible defaults.</p></article><article class="manifesto-item"><h3>Built for content at scale</h3><p>Large trees, large files and many editors are the normal case, not the stress test.</p></article><article class="manifesto-item"><h3>Loved by editors, trusted by developers</h3><p>A comfortable daily tool on top of a serious, extensible Python platform.</p></article></div></div></section>`;

/* ------------------------------------------------------ secure content */

const secureMain = `<section class="page-hero"><div class="shell page-hero__grid"><div><p class="page-context">What secure means</p><h1>Secure content is protected, durable and open.</h1></div><p class="lede">Plone enforces who may see and change every item today, carries it intact across version upgrades for decades, and serves it as structured data whenever you ask.</p></div></section>
  <section class="section section--tight section--soft" aria-label="The three parts of secure content"><div class="shell"><dl class="pillar-list">
      <div><dt><a href="#protected">Protected</a></dt><dd>Permissions and workflow decide who sees and changes every item.</dd></div>
      <div><dt><a href="#durable">Durable</a></dt><dd>Every major release carries your content forward with documented migrations.</dd></div>
      <div><dt><a href="#open">Open</a></dt><dd>The REST API reads and manages all of it, whenever you ask.</dd></div>
    </dl></div></section>
  <section class="section" id="protected" aria-labelledby="protected-title"><div class="shell"><h2 class="section-heading" id="protected-title">Protected, down to a single document.</h2><p class="section-intro">Who may see, change and publish an item is enforced by the platform.</p><div class="detail-grid chapter-body"><div class="prose"><h3>Granular permissions and roles</h3><p>Permissions in Plone follow the content tree. A role granted on a folder applies below it; a sharing entry on one document applies to that document alone. Editors see the sharing view in place, so access control stays part of everyday work instead of a ticket to an administrator.</p><h3>Workflow as a security boundary</h3><p>Workflow states are permission sets. A private draft is invisible to readers because the <em>private</em> state grants no view permission beyond its owners and editors. Moving an item to <em>published</em> is an auditable decision by someone entitled to make it.</p><h3>A record you can check</h3><p>Plone has a dedicated security team, publishes advisories and ships coordinated hotfixes for supported releases. The track record is public — check it rather than take our word for it.</p><p class="voice-line">Content, clearly governed.</p></div><dl class="detail-aside"><dt>Permissions</dt><dd>Per site, per folder, per item</dd><dt>Workflows</dt><dd>State-based, auditable, customisable</dd><dt>Security team</dt><dd>Coordinated advisories and hotfixes</dd></dl></div><figure class="layers-figure">
      <div class="layers-stage">
        <svg class="layers-svg" viewBox="0 0 480 380" role="img" aria-label="A document at the core of four concentric permission layers, from owners and managers at the centre to anonymous visitors at the outside.">
          <rect class="layer layer--soft" x="16" y="16" width="448" height="348" rx="26"/>
          <rect class="layer" x="66" y="60" width="348" height="260" rx="20"/>
          <rect class="layer" x="116" y="104" width="248" height="172" rx="14"/>
          <rect class="layer-core" x="178" y="146" width="124" height="88" rx="9"/>
          <path class="layer-doc" d="M212 172h56M212 190h38M212 208h46"/>
        </svg>
      </div>
      <dl class="layer-legend">
        <div><b>1</b><dt>Owners &amp; managers</dt><dd>full control of the item and its sharing</dd></div>
        <div><b>2</b><dt>Editors &amp; reviewers</dt><dd>write, review and publish</dd></div>
        <div><b>3</b><dt>Members</dt><dd>read internal, logged-in content</dd></div>
        <div><b>4</b><dt>Anonymous visitors</dt><dd>published content only</dd></div>
      </dl>
      <figcaption class="figure-note">The numbers order the layers from most to least privileged.</figcaption>
    </figure></div></section>
  <section class="section section--soft" id="durable" aria-labelledby="durable-title"><div class="shell"><h2 class="section-heading" id="durable-title">Durable across versions and decades.</h2><p class="section-intro">Content you enter today stays meaningful, usable and accessible years from now.</p><div class="detail-grid chapter-body"><div class="prose"><h3>Structured content survives redesigns</h3><p>Every item is typed, structured data: fields, history and a place in the tree. A redesign or a new front end simply re-renders that data — nothing is trapped inside page layouts, so nothing has to be copied out of them.</p><h3>Migrations are part of every release</h3><p>Plone has shipped six major releases since 2001, and each one includes documented migration steps that carry existing sites forward. Editors keep their content, their history and their permissions while the platform underneath renews itself.</p><h3>History you can return to</h3><p>Items keep their revision history: what changed, when and by whom stays visible, and an earlier state can be restored when it is needed.</p></div><dl class="detail-aside"><dt>First release</dt><dd>2001, six majors since</dd><dt>Upgrade path</dt><dd>Documented migration steps per release</dd><dt>History</dt><dd>Revision history built in</dd></dl></div><figure class="versions-figure">
      <div class="versions-stage">
        <svg class="versions-svg" viewBox="0 0 640 200" role="img" aria-label="The same document at each of Plone's six major releases along one upgrade path; the current release holds it highlighted in amber, and the next release is already outlined.">
          <path class="vp-line" d="M48 132h472"/>
          <path class="vp-line vp-line--next" d="M520 132h90"/>
          <rect class="vp-doc" x="26" y="104" width="44" height="56" rx="6"/>
          <rect class="vp-doc" x="116" y="104" width="44" height="56" rx="6"/>
          <rect class="vp-doc" x="206" y="104" width="44" height="56" rx="6"/>
          <rect class="vp-doc" x="296" y="104" width="44" height="56" rx="6"/>
          <rect class="vp-doc" x="386" y="104" width="44" height="56" rx="6"/>
          <rect class="vp-doc vp-doc--now" x="472" y="100" width="52" height="64" rx="7"/>
          <path class="vp-doclines" d="M482 118h32M482 130h22M482 142h27"/>
          <rect class="vp-doc vp-doc--next" x="566" y="104" width="44" height="56" rx="6"/>
        </svg>
      </div>
      <dl class="version-legend">
        <div><span class="vdot" aria-hidden="true"></span><dt>Since 2001</dt><dd>six major releases, each with documented migration steps</dd></div>
        <div class="is-now"><span class="vdot" aria-hidden="true"></span><dt>Today</dt><dd>the current release still serves content from the earliest sites</dd></div>
        <div class="is-next"><span class="vdot" aria-hidden="true"></span><dt>Next</dt><dd>the release your content moves to — the path is part of the product</dd></div>
      </dl>
    </figure></div></section>
  <section class="section" id="open" aria-labelledby="open-title"><div class="shell"><h2 class="section-heading" id="open-title">Open through a proven REST API.</h2><p class="section-intro">Everything in the site is also available as structured JSON — to read and to manage.</p><div class="detail-grid chapter-body"><div class="prose"><h3>One API for the whole site</h3><p>plone.restapi exposes every item, folder, search and workflow action over HTTP. It is the same API Plone's own Volto front end runs on, so it is exercised in production every day.</p><h3>Manage content from anywhere</h3><p>Create, update, review and publish through the same endpoints your editors use in the browser. Scripts, migration jobs and neighbouring systems become first-class editors — with the same permissions and workflow rules applied.</p><h3>The way in is also the way out</h3><p>Your content is yours: read the full tree out as JSON at any time, archive it, move it, or feed it to whatever comes next. That openness is part of what keeps the investment secure.</p></div><dl class="detail-aside"><dt>API</dt><dd>plone.restapi · JSON over HTTP</dd><dt>First-party use</dt><dd>Volto, Plone's React front end</dd><dt>Access control</dt><dd>The API enforces the same permissions</dd></dl></div><figure class="flows-figure">
      <div class="flows-stage">
        <svg class="flows-svg" viewBox="0 0 520 340" role="img" aria-label="A site's content tree behind one API port, connected to three external consumers; content flows out to all of them, and changes flow back in through the same port.">
          <rect class="fl-boundary" x="20" y="48" width="190" height="244" rx="18"/>
          <path class="fl-line" d="M115 120 75 196M115 120l40 76"/>
          <circle class="fl-node" cx="115" cy="120" r="16"/>
          <circle class="fl-node" cx="75" cy="196" r="12"/>
          <circle class="fl-node" cx="155" cy="196" r="12"/>
          <path class="fl-arrow" d="M232 154h68V80h60M232 170h128M232 186h68v74h60"/>
          <path class="fl-arrow" d="M352 72l10 8-10 8M352 162l10 8-10 8M352 252l10 8-10 8"/>
          <path class="fl-arrow" d="M250 162l-10 8 10 8"/>
          <rect class="fl-port" x="192" y="142" width="36" height="56" rx="7"/>
          <rect class="fl-consumer" x="368" y="48" width="120" height="64" rx="8"/>
          <rect class="fl-consumer" x="368" y="138" width="120" height="64" rx="8"/>
          <rect class="fl-consumer" x="368" y="228" width="120" height="64" rx="8"/>
        </svg>
      </div>
      <dl class="flow-legend">
        <div><span class="fkey fkey--site" aria-hidden="true"></span><dt>Your site</dt><dd>the content tree, with workflow and permissions still in charge</dd></div>
        <div><span class="fkey fkey--api" aria-hidden="true"></span><dt>REST API</dt><dd>every item, search and workflow action as JSON over HTTP</dd></div>
        <div><span class="fkey fkey--front" aria-hidden="true"></span><dt>Any consumer</dt><dd>Volto, apps, integrations and exports all use the same door</dd></div>
      </dl>
    </figure></div></section>
  <section class="section section--band" aria-labelledby="secure-title"><div class="shell proof-band"><div><h2 class="section-heading" id="secure-title">All of it together is secure content.</h2><p class="section-intro">Protected today, durable across versions, open at any time — and each claim is public, so you can check it.</p></div><div class="proof-links"><a href="https://plone.org/security" rel="external">Plone security advisories</a><a href="https://6.docs.plone.org/backend/upgrading/index.html" rel="external">Upgrade guide in the Plone docs</a><a href="https://github.com/plone/plone.restapi" rel="external">plone.restapi on GitHub</a><a href="https://plone.org/security/report" rel="external">Report a vulnerability</a></div></div></section>`;

/* ----------------------------------------------------------- community */

const photoFigure = (name, alt, caption) => `<section class="section--photo"><div class="shell"><figure class="photo-figure">
      <div class="photo-frame">
        <picture>
          <source type="image/webp" srcset="assets/images/photo-${name}-800.webp 800w, assets/images/photo-${name}.webp 1600w" sizes="(min-width: 76rem) 72rem, calc(100vw - clamp(2rem, 6vw, 6rem))">
          <img src="assets/images/photo-${name}.jpg" width="1600" height="1067" alt="${alt}" loading="lazy" decoding="async">
        </picture>
      </div>
      <figcaption>${caption}</figcaption>
    </figure></div></section>`;

const communityMain = `<section class="page-hero"><div class="shell page-hero__grid"><div><p class="page-context">Community</p><h1>Made by people you can meet.</h1></div><p class="lede">Plone is built, documented and secured by a worldwide community. Ask a question in the forum, join a sprint or come to a conference.</p></div></section>
  ${photoFigure(
    "community",
    "A group of people working side by side on laptops around one wooden table.",
    "Working in the open — photo by Annie Spratt on Unsplash.",
  )}
  <section class="section section--tight"><div class="shell"><dl class="section-index"><div class="section-index__row"><dt><a href="forum.html">Forum</a></dt><dd>Questions and answers in the open — from first installation to core development, searchable for the next person.<br><a class="section-index__action" href="forum.html">About the forum</a></dd></div><div class="section-index__row"><dt><a href="sprints.html">Sprints</a></dt><dd>Focused development meetings, a Plone tradition since the beginning. Newcomers are onboarded, not tolerated.<br><a class="section-index__action" href="sprints.html">About sprints</a></dd></div><div class="section-index__row"><dt><a href="conferences.html">Conferences</a></dt><dd>The annual Plone Conference and community days around the world — talks, trainings and the sprint that follows.<br><a class="section-index__action" href="conferences.html">About conferences</a></dd></div></dl></div></section>
  <section class="section section--band"><div class="shell proof-band"><blockquote>“Come for the software, stay for the community.”<cite>— a Plone community saying</cite></blockquote><div class="proof-links"><a href="https://community.plone.org" rel="external">community.plone.org</a><a href="https://plone.org/events" rel="external">Events on plone.org</a><a href="https://github.com/plone" rel="external">Plone on GitHub</a></div></div></section>`;

/* --------------------------------------------------------------- forum */

const forumMain = `<section class="page-hero"><div class="shell page-hero__grid"><div><p class="page-context">Community · Forum</p><h1>Ask in the open.</h1></div><p class="lede">The Plone forum at community.plone.org is where users, integrators and core developers answer each other — in public, so every answer helps the next person too.</p></div></section>
  <section class="section"><div class="shell detail-grid"><div class="prose"><h2>What you will find</h2><p>Categories for setup and support, theming, deployment, add-on development and the REST API — plus announcements of releases, security hotfixes and community events. Years of solved questions are a searchable archive; most problems you meet have been met before.</p><h2>How it works</h2><p>Reading is open to everyone; asking requires a free account. Describe what you tried, name your Plone version, and expect direct, friendly answers. The people replying often wrote the code in question.</p><div class="action-row"><a class="button" href="https://community.plone.org" rel="external">Open the forum</a></div></div><dl class="detail-aside"><dt>Where</dt><dd>community.plone.org</dd><dt>Costs</dt><dd>Free, public archive</dd><dt>Who answers</dt><dd>Users, integrators and core developers</dd></dl></div></section>`;

/* ------------------------------------------------------------- sprints */

const sprintsMain = `<section class="page-hero"><div class="shell page-hero__grid"><div><p class="page-context">Community · Sprints</p><h1>Where the work gets done.</h1></div><p class="lede">Sprints are focused development meetings, a Plone tradition since the beginning: a few days, one topic, shoulder to shoulder.</p></div></section>
  ${photoFigure(
    "sprint",
    "Laptops, notebooks and coffee crowded around a shared work table, seen from above.",
    "One table, one topic — photo by Marvin Meyer on Unsplash.",
  )}
  <section class="section"><div class="shell detail-grid"><div class="prose"><h2>A tradition, not an event format</h2><p>Much of Plone was designed, built and documented at sprints. A sprint has a topic, a small crowd and a bias for finishing: features land, documentation improves, releases get closer.</p><h2>Newcomers are the point</h2><p>Sprints are the easiest door into contribution. Someone sits down with you, gets your environment running and finds a task that fits. You leave as a contributor with names and faces behind the commits.</p></div><dl class="detail-aside"><dt>Duration</dt><dd>Two days to a week</dd><dt>Bring</dt><dd>A laptop and curiosity</dd><dt>Experience needed</dt><dd>None — onboarding is part of the plan</dd></dl></div></section>
  <section class="section section--soft" aria-labelledby="sprint-list-title"><div class="shell"><h2 class="section-heading" id="sprint-list-title">Sprints with a history.</h2><ul class="event-list"><li><span class="event-meta">Innsbruck, Austria</span><h3>Alpine City Sprint</h3><p>A winter classic: a week of concentrated core and documentation work in the Alps.</p></li><li><span class="event-meta">After each conference</span><h3>Conference sprints</h3><p>Two days following every Plone Conference, where talk ideas become branches and pull requests.</p></li><li><span class="event-meta">Announced in the forum</span><h3>Topic sprints</h3><p>Smaller meetings around one goal — a release, an upgrade guide, an add-on ecosystem.</p></li></ul></div></section>`;

/* --------------------------------------------------------- conferences */

const conferencesMain = `<section class="page-hero"><div class="shell page-hero__grid"><div><p class="page-context">Community · Conferences</p><h1>Once a year, in person.</h1></div><p class="lede">The annual Plone Conference brings the community together for a week of trainings, talks and sprints — in a different host city every year.</p></div></section>
  ${photoFigure(
    "conference",
    "A conference audience watching a talk in a darkened hall.",
    "Talks worth the trip — photo by Headway on Unsplash.",
  )}
  <section class="section"><div class="shell detail-grid"><div class="prose"><h2>One week, three parts</h2><p>Conference week opens with hands-on trainings, continues with two or three days of talks — case studies, core development, design, deployment — and closes with a sprint that turns hallway conversations into working code.</p><h2>Worth the trip</h2><p>Decisions about the platform's direction are presented and discussed where everyone can join. If you run Plone, one conference week answers more questions than a year of tickets.</p></div><dl class="detail-aside"><dt>Rhythm</dt><dd>Annual, rotating host city</dd><dt>Format</dt><dd>Trainings · talks · sprint</dd><dt>Recordings</dt><dd>Talks are published openly</dd></dl></div></section>
  <section class="section section--soft" aria-labelledby="conf-list-title"><div class="shell"><h2 class="section-heading" id="conf-list-title">Mark the calendar.</h2><ul class="event-list"><li><span class="event-meta">Annual · one week</span><h3>Plone Conference</h3><p>The main gathering: trainings, talks and the closing sprint, hosted by a local community.</p></li><li><span class="event-meta">Each spring · worldwide</span><h3>World Plone Day</h3><p>Local events on one shared day — user groups and companies open their doors and show their work.</p></li><li><span class="event-meta">Year round</span><h3>Python &amp; web events</h3><p>Plone people speak at PyCons and web conferences; the platform travels well beyond its own stage.</p></li></ul><p class="structure-note"><a class="quiet-link" href="https://plone.org/events" rel="external">Current dates on plone.org</a></p></div></section>`;

/* ----------------------------------------------------------------- 404 */

const notFoundMain = `<section class="error-page"><div class="shell error-page__inner"><p class="error-page__code">Error 404</p><h1>This page went private.</h1><p>The address may have changed, or the content is no longer published. The homepage will get you back on track.</p><div class="action-row"><a class="button" href="index.html">Back to the homepage</a><a class="quiet-link" href="community.html">Ask the community</a></div></div></section>`;

/* ---------------------------------------------------------------- emit */

const pages = [
  {
    file: "index.html",
    title: "Content, secure in every sense. · Clara",
    description: "Clara is a lightweight theme for Plone, the open-source CMS whose content stays secure in every sense: protected by workflow and permissions, durable across versions, open through the REST API.",
    current: "home",
    main: homeMain,
    extraHead: `  <link rel="preload" as="image" href="assets/images/plone_en.webp" type="image/webp">\n`,
  },
  {
    file: "why-plone.html",
    title: "Why Plone · Clara",
    description: "The case for Plone: editorial workflows, granular permissions, a complete REST API, safe migrations and a track record reaching back to 2001.",
    current: "why-plone",
    crumbs: [["Home", "index.html"], ["Why Plone"]],
    main: whyPloneMain,
  },
  {
    file: "secure-content.html",
    title: "Secure Content · Clara",
    description: "Secure content is protected, durable and open: permissions and workflow today, safe migrations across major versions, and full access through Plone's REST API.",
    current: "secure-content",
    crumbs: [["Home", "index.html"], ["Secure Content"]],
    main: secureMain,
  },
  {
    file: "community.html",
    title: "Community · Clara",
    description: "Plone is built, documented and secured by a worldwide community: the forum, sprints and the annual Plone Conference.",
    current: "community",
    crumbs: [["Home", "index.html"], ["Community"]],
    main: communityMain,
  },
  {
    file: "forum.html",
    title: "Forum · Community · Clara",
    description: "The Plone forum at community.plone.org: public questions and answers from users, integrators and core developers.",
    current: "forum",
    crumbs: [["Home", "index.html"], ["Community", "community.html"], ["Forum"]],
    main: forumMain,
  },
  {
    file: "sprints.html",
    title: "Sprints · Community · Clara",
    description: "Plone sprints: focused development meetings where the platform moves forward and newcomers become contributors.",
    current: "sprints",
    crumbs: [["Home", "index.html"], ["Community", "community.html"], ["Sprints"]],
    main: sprintsMain,
  },
  {
    file: "conferences.html",
    title: "Conferences · Community · Clara",
    description: "The annual Plone Conference — trainings, talks and sprints — plus World Plone Day and community events worldwide.",
    current: "conferences",
    crumbs: [["Home", "index.html"], ["Community", "community.html"], ["Conferences"]],
    main: conferencesMain,
  },
  {
    file: "404.html",
    title: "Page not found · Clara",
    description: "This page is not published here. Return to the Clara demo homepage.",
    current: "none",
    main: notFoundMain,
  },
];

for (const p of pages) {
  writeFileSync(join(root, p.file), page(p));
  console.log("wrote", p.file);
}
