"""Editor-toolbar chrome folded into the compiled bundle (wayfinder ticket 15).

Ticket 14 ruled the editor-toolbar CSS a THEME responsibility (as stock Plone
ships ``barceloneta-toolbar.min.css`` inside the Barceloneta *theme*, not a
theme-independent layer); ticket 15 moves its ``#edit-zone`` chrome out of the
now-zero-CSS ``plone.pageletlayout`` base into Clara's one compiled
``clara.min.css`` (``_clara-toolbar.scss``, ``@layer components``).

Only the TOOLBAR DELTA moved — its own ``--plone-toolbar-*`` / ``--plone-state-*``
tokens + the ``#edit-zone`` / ``body.plone-toolbar-*`` rules. The vendored
sheet's first ~723 lines (a full Bootstrap 5.3 ``:root{--bs-*}`` dump + Reboot +
``.nav`` base) and its trailing ``.flex-*`` utilities were DROPPED: Clara already
compiles that exact Bootstrap into ``@layer bootstrap``, so folding them in would
duplicate it and — worse — the un-layered ``:root`` ``--bs-*`` dump would shadow
Clara's own ``:root`` bridge. This is the no-browser structural guard; the
sibling fixture ``tests/fixtures/toolbar-proof.html`` is the live-render proof a
text check can't do.
"""
import re
from pathlib import Path

import pytest


BUNDLE = (
    Path(__file__).resolve().parent.parent
    / "src" / "plonetheme" / "clara" / "static" / "clara.min.css"
)


def _strip_block_comments(text):
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


@pytest.fixture(scope="module")
def bundle():
    assert BUNDLE.exists(), (
        f"compiled bundle missing at {BUNDLE} — run `npm run build` in "
        f"plonetheme.clara first."
    )
    return _strip_block_comments(BUNDLE.read_text())


@pytest.fixture(scope="module")
def flat(bundle):
    """Whitespace-collapsed copy for robust membership checks."""
    return re.sub(r"\s+", "", bundle)


# ── the chrome landed ─────────────────────────────────────────────────────────

def test_edit_zone_chrome_present(flat):
    """The #edit-zone chrome the base used to ship now lives in the bundle."""
    assert "#edit-zone{" in flat
    # a descendant override of Bootstrap's .nav-link that only the toolbar
    # sheet carries (whitespace-collapsed, so the descendant space is gone)
    assert "#edit-zone.nav-link" in flat


def test_body_toolbar_layout_variants_present(flat):
    """The left/top toolbar layout chrome moved too, not just the base rule."""
    assert "body.plone-toolbar-left" in flat
    assert "body.plone-toolbar-top" in flat


def test_toolbar_tokens_present(flat):
    """The toolbar's OWN knobs ship — the theme now owns them."""
    for token in (
        "--plone-toolbar-bg:",
        "--plone-toolbar-text-color:",
        "--plone-toolbar-width:",
        "--plone-toolbar-font:",
        "--plone-state-draft:",
    ):
        assert token in flat, f"missing toolbar token {token}"


# ── the redundant Bootstrap was NOT folded in ────────────────────────────────

def test_toolbar_background_uses_clara_semantic_dark(flat):
    """The toolbar now uses Clara's same-hue dark surface directly instead of
    reviving Bootstrap's stock --bs-dark token at :root."""
    assert "--plone-toolbar-bg:var(--clara-brand-deep)" in flat
    assert "--bs-dark:#212529" not in flat


def test_bootstrap_dump_not_duplicated(flat):
    """The toolbar sheet's redundant :root{--bs-*} dump was dropped, not folded.

    ``--bs-blue`` is defined once by Bootstrap's own :root; if the toolbar sheet
    had been imported verbatim we'd see it a second time (and that second,
    un-bridged dump would shadow Clara's --bs-*→--plone-* bridge at :root).
    """
    assert flat.count("--bs-blue:#0d6efd") == 1


def test_no_toolbar_body_reboot_leaked(bundle):
    """The toolbar sheet's global Reboot was dropped, not folded in.

    A bare ``body{...}`` (no class / descendant) legitimately appears TWICE in
    the bundle: once in Clara's own ``@layer reset`` and once in Bootstrap's
    Reboot (``@layer bootstrap``). The vendored toolbar sheet carries a THIRD —
    if it had been imported verbatim the count would be 3. The toolbar's own
    body rules that DID move are all class-qualified (``body.plone-toolbar-*``),
    so they don't count here.
    """
    bare_body = re.findall(r"(?:^|[{};,])\s*body\s*\{", bundle)
    assert len(bare_body) == 2, (
        f"expected 2 bare body{{}} rules (Clara reset + Bootstrap reboot), got "
        f"{len(bare_body)} — the toolbar sheet's redundant Reboot leaked in"
    )


# ── the chrome sits where it can win ─────────────────────────────────────────

def test_toolbar_chrome_in_components_layer(bundle):
    """#edit-zone overrides of Bootstrap's .nav-link must sit in @layer
    components (which beats @layer bootstrap) — else Bootstrap's global
    .nav-link would win over the toolbar's scoped one despite lower specificity.
    """
    first_edit = bundle.index("#edit-zone")
    head = bundle[:first_edit]
    opens = re.findall(r"@layer\s+([a-z]+)\s*\{", head)
    assert opens, "no @layer block opened before #edit-zone"
    assert opens[-1] == "components", (
        f"#edit-zone chrome is under @layer {opens[-1]}, not components — it "
        f"would lose to Bootstrap's global .nav-link"
    )
