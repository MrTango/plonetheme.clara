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


# ── focus mode: the rail steps aside for data entry on a phone ───────────────
#
# Below 768px the toolbar is a 60px icon rail whose expand toggle is hidden, so
# it costs an eighth of a 390px screen and cannot show a label in return. On a
# form holding unsaved data that is the worst trade on the site. What makes
# hiding a navigation landmark safe is that the trigger IS the escape hatch:
# the rule only fires where the page carries a Cancel button.

FOCUS_SELECTOR = "body:has(#content-coreform.pat-formunloadalert#form-buttons-cancel)"


def _phone_blocks(bundle):
    """Bodies of every `@media (max-width: 767.98px)` block in the bundle."""
    return re.findall(
        r"@media\s*\(max-width:\s*767\.98px\)\s*\{(.*?)\}\s*(?=@|$)",
        bundle,
        flags=re.DOTALL,
    )


def test_form_focus_mode_hides_the_rail_on_a_phone(flat):
    assert f"{FOCUS_SELECTOR}#edit-zone{{display:none}}" in flat, (
        "no rule hides #edit-zone on a phone-sized data-entry form"
    )
    assert f"{FOCUS_SELECTOR}{{padding-left:0}}" in flat, (
        "hiding the rail without releasing body's padding-left leaves the "
        "60px gap the rail used to fill"
    )


def test_form_focus_mode_is_gated_on_an_escape_hatch(flat):
    """`#form-buttons-cancel` in the selector is not decoration: it is the
    only reason hiding the toolbar is safe. A form with no way out keeps its
    rail, so the condition must never be loosened to a body class."""
    hides = re.findall(r"([^{}]*)#edit-zone\{display:none\}", flat)
    for selector in hides:
        assert "#form-buttons-cancel" in selector, (
            f"{selector!r} hides the toolbar without requiring a Cancel "
            f"button — that can strand a phone user inside a form"
        )


def test_form_focus_mode_is_phone_only(bundle):
    """Desktop keeps the toolbar: the rule lives inside the same 767.98px
    band the rest of the toolbar's mobile chrome uses."""
    assert any(
        "#form-buttons-cancel" in block for block in _phone_blocks(bundle)
    ), "the focus-mode rule is not inside a (max-width: 767.98px) block"


# ── Clara's own: the pin/unpin toggle is findable ────────────────────────────

def _media_blocks(css, condition):
    """Bodies of every ``@media`` block whose prelude carries `condition`,
    brace-balanced so a compressed one-line bundle reads the same as a
    pretty-printed one."""
    blocks = []
    for match in re.finditer(r"@media([^{]*)\{", css):
        if condition.replace(" ", "") not in match.group(1).replace(" ", ""):
            continue
        index, depth = match.end(), 1
        while depth and index < len(css):
            depth += {"{": 1, "}": -1}.get(css[index], 0)
            index += 1
        blocks.append(css[match.end():index - 1])
    return blocks


def test_the_toggle_has_a_real_hit_area(bundle):
    """The viewlet ships each toggle as a bare 16px glyph. Without a target
    around it the control is a pixel hunt, which is the whole reason people
    conclude the rail cannot be collapsed."""
    rules = re.findall(r"#edit-zone \.toolbar-header a\{([^}]*)\}", bundle)
    assert rules, "no rule styles the toolbar-header links at all"
    sized = [r for r in rules if "min-height" in r]
    assert sized, f"the toggle is still just the glyph: {rules!r}"
    for declaration in ("padding-inline:", "gap:"):
        assert declaration in sized[0], (
            f"the toggle has no {declaration.rstrip(':')}: {sized[0]!r}"
        )
    assert "width:1.25rem" in bundle, "the toggle's icon was not enlarged"


def test_the_toggle_answers_the_pointer_and_the_keyboard(bundle):
    """Feedback is half of an affordance: something has to happen on hover,
    and the same thing on focus, or the strip still reads as decoration."""
    match = re.search(
        r"([^{}]*\.toolbar-header a:hover[^{}]*)\{([^}]*)\}", bundle
    )
    assert match, "nothing paints a hover state on the toolbar header"
    assert ":focus-visible" in match.group(1), (
        f"the hover state is not shared with the keyboard: {match.group(1)!r}"
    )
    assert "background" in match.group(2), (
        f"the hover state paints nothing: {match.group(2)!r}"
    )


def test_the_expanded_rail_names_the_control(bundle):
    """The name comes from the aria-label the viewlet already renders and
    Plone already translates ("Unpin" -> "Abkoppeln"), so the visible label
    can never drift from what a screen reader announces."""
    labels = re.findall(r"([^{}]*)\{content:attr\(aria-label\)", bundle)
    assert labels, "the toggle is still unlabelled in the expanded rail"
    for selector in labels:
        assert ".plone-toolbar-left-expanded" in selector, (
            f"{selector!r} writes the label into a rail with no room for it"
        )


def test_the_label_is_desktop_only(bundle):
    """The 60px icon rail cannot show a word, and below 768px the toggles are
    hidden outright — a label there would be a label on nothing."""
    desktop = _media_blocks(bundle, "(min-width:768px)")
    assert desktop, "no (min-width: 768px) block in the bundle at all"
    assert any("attr(aria-label)" in block for block in desktop), (
        "the label rule is not inside a (min-width: 768px) block"
    )


def test_the_state_switch_still_decides_which_toggle_shows(bundle):
    """These rules re-declare `display` for the toggle that is showing, so
    the icon and its label share a line. Re-declaring it unconditionally
    would reveal BOTH toggles at once; every such rule has to carry the body
    class that names the state."""
    switches = re.findall(
        r"([^{}]*\.toolbar-(?:expand|collapse))\{display:flex\}", bundle
    )
    assert switches, "no toggle is laid out as a row — the label cannot sit "
    for selector in switches:
        assert "body.plone-toolbar-left" in selector, (
            f"{selector!r} shows a toggle regardless of the toolbar's state"
        )


def test_the_phone_rule_still_hides_both_toggles(bundle):
    """Below 768px the toolbar is a 60px rail whose expanded state does not
    exist, so a visible toggle there would be a no-op — except on the Aurora
    edit page, whose own sheet reveals it deliberately and gives it something
    to do (plone.blicca.auroraeditor, blocks_view.css)."""
    phone = "".join(_media_blocks(bundle, "(max-width:767.98px)"))
    assert "#edit-zone .toolbar-header a{display:none}" in phone, (
        "the phone rule that hides both toggles is gone — the 60px rail now "
        "carries a control that cannot change anything"
    )
