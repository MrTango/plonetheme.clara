"""Setup handlers for plonetheme.clara."""

import logging
from pathlib import Path

from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.textfield.value import RichTextValue
from plone.base.interfaces import INonInstallable
from plone.namedfile.file import NamedBlobImage
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.interface import implementer


logger = logging.getLogger(__name__)

HOME_HTML = """
<div class="clara-home">
  <section class="clara-home-hero" aria-labelledby="clara-home-title">
    <div class="clara-home-copy">
      <h1 id="clara-home-title">Welcome to <strong>Clara Theme.</strong></h1>
      <p class="clara-home-lede">A clear, accessible starting point for Plone sites,
        shaped around structured content and the people who maintain it.</p>
      <div class="clara-home-actions">
        <a class="clara-button" href="https://plone.org/">Explore Plone</a>
        <a class="clara-text-link" href="https://community.plone.org/">Meet the community →</a>
      </div>
    </div>
    <figure class="clara-home-figure">
      <picture>
        <source srcset="++resource++plonetheme.clara/plone_en.webp" type="image/webp" />
        <img src="++resource++plonetheme.clara/plone_en.png" width="1254" height="1254"
          alt="Plone supports large content collections, editorial groups, workflows,
            permissions, and accessible user experiences."
          fetchpriority="high" decoding="async" />
      </picture>
      <figcaption>Plone gives editors and developers a dependable foundation for
        content-heavy platforms.</figcaption>
    </figure>
  </section>

  <section class="clara-community" aria-labelledby="clara-community-title">
    <div class="clara-community-heading">
      <h2 id="clara-community-title">Built with the Plone community.</h2>
      <p>Documentation, conversation, and shared packages are always close at hand.</p>
    </div>
    <ul class="clara-resource-list">
      <li>
        <a href="https://plone.org/">
          <strong>Plone.org</strong>
          <span>Learn about Plone, its features, and the Foundation.</span>
          <b aria-hidden="true">↗</b>
        </a>
      </li>
      <li>
        <a href="https://community.plone.org/">
          <strong>Community forum</strong>
          <span>Ask questions and meet editors, integrators, and developers.</span>
          <b aria-hidden="true">↗</b>
        </a>
      </li>
      <li>
        <a href="https://github.com/collective/awesome-plone">
          <strong>Awesome Plone</strong>
          <span>Browse useful packages, documentation, and community resources.</span>
          <b aria-hidden="true">↗</b>
        </a>
      </li>
    </ul>
  </section>
</div>
""".strip()

CONTACT_HTML = """
<section class="clara-contact" aria-labelledby="clara-contact-title">
  <h2 id="clara-contact-title">Make this page yours.</h2>
  <div class="clara-contact-copy">
    <p>Add the contact details and response expectations that are useful to your visitors.</p>
    <p>For questions about Plone itself, visit the
      <a href="https://community.plone.org/">Plone community forum</a>.</p>
  </div>
</section>
""".strip()

ABOUT_HTML = """
<p>Clara Theme provides a lightweight visual foundation for a standard Plone site.
Its token-based styles can be adapted without replacing the page templates.</p>
""".strip()

NEWS_HTML = """
<p>Your new site is ready. Replace this starter item with news from your organisation,
then use Plone's workflow to review and publish it.</p>
""".strip()


def _rich_text(raw):
    """Return safe rich text for a Dexterity text field."""
    return RichTextValue(
        raw=raw,
        mimeType="text/html",
        outputMimeType="text/x-html-safe",
        encoding="utf-8",
    )


def _ensure_content(container, portal_type, content_id, **values):
    """Create starter content once, preserving later editor changes."""
    if content_id in container:
        obj = container[content_id]
        if obj.portal_type != portal_type:
            logger.warning(
                "Clara starter content skipped %s: expected %s, found %s",
                content_id,
                portal_type,
                obj.portal_type,
            )
            return None, False
        return obj, False

    return (
        api.content.create(
            container=container,
            type=portal_type,
            id=content_id,
            **values,
        ),
        True,
    )


def _publish(objects):
    """Publish starter objects when the active workflow offers that state."""
    for obj in objects:
        try:
            if api.content.get_state(obj, default=None) != "published":
                api.content.transition(obj=obj, to_state="published")
        except (InvalidParameterError, WorkflowException):
            logger.info("No transition to published for Clara starter item %s", obj.id)


def _install_home(portal, created):
    """Install Clara's home page without replacing editor-owned content."""
    front_page, was_created = _ensure_content(
        portal,
        "Document",
        "front-page",
        title="Welcome to Clara Theme",
        description="A community-connected starting point for a new Plone site.",
        text=_rich_text(HOME_HTML),
        exclude_from_nav=True,
    )
    if was_created:
        created.append(front_page)
    elif front_page is not None and front_page.title in {
        "Welcome to Plone",
        "Welcome to Plone!",
    }:
        # A stock, untouched Plone front page is safe to turn into Clara's
        # starter page; any renamed page is treated as editor-owned content.
        front_page.title = "Welcome to Clara Theme"
        front_page.description = "A community-connected starting point for a new Plone site."
        front_page.text = _rich_text(HOME_HTML)
        front_page.exclude_from_nav = True
        front_page.reindexObject()
        created.append(front_page)


def _install_pages(demo, created):
    """Install the Pages branch when its path is available."""
    pages, pages_created = _ensure_content(
        demo,
        "Folder",
        "pages",
        title="Pages",
        description="Long-lived pages for structured information.",
    )
    if pages is None:
        return
    if pages_created:
        created.append(pages)

    about, about_created = _ensure_content(
        pages,
        "Document",
        "about-this-site",
        title="About this site",
        description="A simple example page included with Clara Theme.",
        text=_rich_text(ABOUT_HTML),
        exclude_from_nav=True,
    )
    if about_created:
        created.append(about)


def _install_news(demo, created):
    """Install the News branch when its path is available."""
    news, news_created = _ensure_content(
        demo,
        "Folder",
        "news",
        title="News",
        description="Time-based updates for your visitors.",
    )
    if news is None:
        return
    if news_created:
        created.append(news)

    welcome, welcome_created = _ensure_content(
        news,
        "News Item",
        "welcome-to-clara",
        title="Welcome to Clara Theme",
        description="The base theme and its starter content are ready to use.",
        text=_rich_text(NEWS_HTML),
        exclude_from_nav=True,
    )
    if welcome_created:
        created.append(welcome)


def _install_photos(demo, created):
    """Install the Photos branch when its path is available."""
    photos, photos_created = _ensure_content(
        demo,
        "Folder",
        "photos",
        title="Photos",
        description="An album view for visual content.",
    )
    if photos is None:
        return
    if photos_created:
        photos.setLayout("album_view")
        created.append(photos)

    image_path = Path(__file__).parent / "static" / "plone_en.png"
    image, image_created = _ensure_content(
        photos,
        "Image",
        "plone-for-content-teams",
        title="Plone for content teams",
        description="An overview of Plone's editorial strengths.",
        image=NamedBlobImage(
            data=image_path.read_bytes(),
            filename="plone_en.png",
            contentType="image/png",
        ),
        exclude_from_nav=True,
    )
    if image_created:
        created.append(image)


def _install_demo(portal, created):
    """Install the Pages, News, and Photos demonstration tree."""
    demo, demo_created = _ensure_content(
        portal,
        "Folder",
        "demo-content",
        title="Demo content",
        description="Examples of the standard content structures included with Plone.",
    )
    if demo is None:
        return
    if demo_created:
        created.append(demo)
        # showcase the mega-panel proof zone (IMegamenuSection behavior)
        demo.megamenu_proof = (
            "Every structure here is stock Plone: rebuild it, rename it, "
            "or delete it without losing anything."
        )
        demo.reindexObject()

    _install_pages(demo, created)
    _install_news(demo, created)
    _install_photos(demo, created)


def _install_contact(portal, created):
    """Install a small, editable contact page."""
    contact, contact_created = _ensure_content(
        portal,
        "Document",
        "contact",
        title="Contact",
        description="A starter contact page ready for your organisation's details.",
        text=_rich_text(CONTACT_HTML),
    )
    if contact_created:
        created.append(contact)


def _cover_event_listing(portal):
    """Move the stock events aggregator off the classic-only event_listing view.

    plone.app.event's event_listing is not a pagelet-covered view, so it falls
    back to the classic main_template and renders outside the theme. The
    covered summary_view presents the same collection inside the layout.
    """
    events = portal.get("events")
    aggregator = events.get("aggregator") if events is not None else None
    if aggregator is not None and aggregator.getLayout() == "event_listing":
        aggregator.setLayout("summary_view")
        logger.info("Clara: events aggregator switched to summary_view")


def post_install(context):
    """Create the minimal Clara homepage and demo navigation on first install."""
    portal = api.portal.get()
    created = []

    _install_home(portal, created)
    _install_demo(portal, created)
    _install_contact(portal, created)
    _cover_event_listing(portal)

    if portal.getDefaultPage() in {None, "", "front-page"}:
        portal.setDefaultPage("front-page")
    _publish(created)


@implementer(INonInstallable)
class HiddenProfiles:
    """Hidden profiles/products from the Plone add-ons control panel."""

    def getNonInstallableProducts(self):
        """Products that should not appear as installable add-ons."""
        return [
            "plonetheme.clara.upgrades",
        ]

    def getNonInstallableProfiles(self):
        """Profiles that should not be available for install.

        The upgrade profiles (plonetheme.clara.upgrades:1001…) are applied
        by their genericsetup:upgradeDepends steps, never installed by hand.
        """
        return [
            "plonetheme.clara:uninstall",
            "plonetheme.clara.upgrades:1001",
            "plonetheme.clara.upgrades:1002",
            "plonetheme.clara.upgrades:1003",
            "plonetheme.clara.upgrades:1004",
            "plonetheme.clara.upgrades:1005",
            "plonetheme.clara.upgrades:1006",
            "plonetheme.clara.upgrades:1007",
        ]


def uninstall(context):
    """Uninstall script."""
    pass
