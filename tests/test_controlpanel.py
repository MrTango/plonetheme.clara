"""Site Setup (`@@overview-controlpanel`) chrome in the compiled bundle.

Plone core owns the control-panel markup: `.configlets` is a grid of
`<a class="d-block text-center py-4 rounded btn btn-light h-100">` tiles, each
an `.overview-icon` SVG above its label (Products/CMFPlone/controlpanel/browser/
overview.pt). Barceloneta ships the handful of rules that make that markup read
as a tile grid; Clara shipped none of them, and two Clara decisions actively
broke the page:

  * `$theme-colors` is slimmed to five roles (clara-bootstrap.scss §6.2), so
    Bootstrap never emits `.btn-light` — every tile rendered transparent and
    edgeless; and
  * the base reset sets `svg { display: block }` (_clara-layers.scss), which
    takes the icon out of the tile's `text-align: center` flow and pins it to
    the inline start.

Same no-Sass/no-browser harness as test_component_bridge.py: a structural proof
on the COMPILED `clara.min.css`, because that file — not the Sass — is what a
site loads. The rules live in _clara-controlpanel.scss (layout) and
_clara-bridge.scss (the `.btn-light` compat variant).
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
        f"compiled bundle missing at {BUNDLE} — run `pnpm run build` in "
        f"plonetheme.clara first."
    )
    return _strip_block_comments(BUNDLE.read_text())


def _rules(bundle, selector):
    """All declaration bodies of an exact single-selector `selector{...}` rule."""
    return re.findall(re.escape(selector) + r"\s*\{([^}]*)\}", bundle)


def _body(bundle, selector):
    bodies = _rules(bundle, selector)
    assert bodies, f"{selector} is not styled in the compiled bundle"
    return "".join(bodies)


def _neutral_body(bundle, variant):
    """Declarations reaching `variant` from any rule that lists it as one of a
    comma-separated selector group — Sass compiles the shared neutral family
    into a single `.btn-light,.btn-secondary{…}` rule."""
    return "".join(
        body
        for group, body in re.findall(r"([^{}]+)\{([^}]*)\}", bundle)
        if variant in [part.strip() for part in group.split(",")]
    )


# --------------------------------------------------------------------------- #
# 1. The neutral button family exists again, and is token-driven.
# --------------------------------------------------------------------------- #

BTN_LIGHT_TOKENS = (
    "--bs-btn-color",
    "--bs-btn-bg",
    "--bs-btn-border-color",
    "--bs-btn-hover-color",
    "--bs-btn-hover-bg",
    "--bs-btn-hover-border-color",
    "--bs-btn-active-color",
    "--bs-btn-active-bg",
    "--bs-btn-active-border-color",
    "--bs-btn-disabled-color",
    "--bs-btn-disabled-bg",
    "--bs-btn-disabled-border-color",
)


# `.btn-light` is core's configlet tile; `.btn-secondary` is the Cancel button
# on every control-panel form. Clara's slimmed $theme-colors emits neither.
NEUTRAL_VARIANTS = (".btn-light", ".btn-secondary")


@pytest.mark.parametrize("variant", NEUTRAL_VARIANTS)
def test_neutral_button_variant_is_emitted(bundle, variant):
    """Without the variant the element has neither fill nor edge: a configlet
    tile is an invisible rectangle and Cancel is invisible text."""
    assert _neutral_body(bundle, variant), (
        f"{variant} is missing from the bundle — core markup that asks for it "
        f"renders transparent and edgeless"
    )


@pytest.mark.parametrize("variant", NEUTRAL_VARIANTS)
@pytest.mark.parametrize("token", BTN_LIGHT_TOKENS)
def test_neutral_button_states_are_complete_and_token_driven(bundle, variant, token):
    """Every one of the button's fill/ink/edge states across rest, hover, active
    and disabled resolves through a `--plone-*` role — never a grey literal — so
    a runtime token override moves them with the rest of the site, and the
    dark-mode role swap reaches them for free."""
    body = _neutral_body(bundle, variant)
    assert re.search(
        re.escape(token) + r"\s*:\s*var\(--plone-[\w-]+\)", body
    ), f"{variant} must bind {token} to a --plone-* role; got {body!r}"


# --------------------------------------------------------------------------- #
# 2. The tile icon: a 3rem box, re-centred against the reset's block SVGs.
# --------------------------------------------------------------------------- #

def test_overview_icon_has_an_icon_sized_box(bundle):
    """A configlet icon is geometry, not rhythm: Barceloneta pins 3rem, and the
    16px SVG intrinsic size is far too small to read as a tile. The size stays
    tunable through a `--plone-configlet-icon-size` knob (§ every hook carries a
    --plone-* API), but its default must be the 3rem box."""
    body = _body(bundle, ".configlets .overview-icon")
    assert "--plone-configlet-icon-size" in body, (
        "the configlet icon box must expose a --plone-* knob, not hardcode 3rem"
    )
    assert body.count("3rem") >= 2, (
        f"both inline-size and block-size must default to 3rem; got {body!r}"
    )
    assert "inline-size" in body and "block-size" in body, (
        f"the icon box must be sized on both axes; got {body!r}"
    )


def test_overview_icon_is_recentred_against_the_block_svg_reset(bundle):
    """_clara-layers.scss sets `svg { display: block }` for the whole site. A
    block-level 3rem icon ignores the tile's `text-align: center` and sticks to
    the inline start; `margin-inline: auto` re-centres it WITHOUT reverting the
    reset (core's markup must not be overridden to fix this)."""
    body = _body(bundle, ".configlets .overview-icon")
    assert re.search(r"margin-inline\s*:\s*auto", body), (
        "the configlet icon must be re-centred with margin-inline:auto — the "
        f"base reset's block SVGs otherwise pin it left; got {body!r}"
    )


def test_reset_still_makes_svgs_block(bundle):
    """Guard the premise of the rule above: if the reset ever stops forcing
    block SVGs, `margin-inline: auto` becomes dead weight and this pair of rules
    should be revisited rather than silently kept."""
    assert re.search(r"img,\s*picture,\s*svg\s*\{[^}]*display\s*:\s*block", bundle), (
        "the reset no longer forces `svg{display:block}` — recheck whether the "
        "configlet icon still needs margin-inline:auto"
    )


# --------------------------------------------------------------------------- #
# 3. Panel rhythm on the Clara space ramp, not Barceloneta's flat rem.
# --------------------------------------------------------------------------- #

def test_control_panel_header_uses_the_space_ramp(bundle):
    """Barceloneta separates the panel heading from the tiles with a flat 2rem.
    Clara keeps the same visual break but takes it from the fluid ramp, so the
    panel breathes with the rest of the theme."""
    # Sass drops the attribute-value quotes when compressing, so match either.
    selector = r'body\[class\*="?-controlpanel"?\]\s*\.controlPanel\s*>\s*header'
    assert re.search(selector, bundle), (
        "the control-panel header rule is missing from the bundle"
    )
    body = "".join(re.findall(selector + r"[^{]*\{([^}]*)\}", bundle))
    assert re.search(r"margin-block-end\s*:\s*var\(--plone-space-[\w-]+\)", body), (
        f"the panel header break must come from a --plone-space-* step; got {body!r}"
    )
