"""Content-view component styling in the compiled bundle.

Listing, summary, tabular and album views reuse Plone's own hooks, expose
`--plone-*` custom properties and lay out elastically.
"""
import re

import pytest


@pytest.fixture(scope="module")
def flat(bundle):
    """Whitespace-collapsed copy for robust *selector-presence* membership,
    independent of how Sass grouped/ordered the compiled selectors."""
    return re.sub(r"\s+", "", bundle)


def _rule(bundle, selector):
    """Declaration body of an exact single-selector `selector{...}` rule."""
    return re.findall(re.escape(selector) + r"\s*\{([^}]*)\}", bundle)


# --------------------------------------------------------------------------- #
# 1. The listing container: ONE elastic grid, a --plone-* column API, no query.
# --------------------------------------------------------------------------- #

def test_entries_is_an_elastic_grid_with_plone_api(bundle):
    """`.entries` lays out as a grid whose column behaviour is driven by a
    `--plone-entries-*` knob and `minmax()` — the elastic wide-column-vs-rail
    mechanism (§5 container queries deferred). No hardcoded column count."""
    bodies = _rule(bundle, ".entries")
    assert bodies, ".entries is not styled in the compiled bundle"
    body = bodies[0]
    assert "display:grid" in body, f".entries must be a grid; got {body!r}"
    assert "minmax(" in body, ".entries columns must be elastic (minmax())"
    assert "--plone-entries-min" in body, (
        ".entries must expose a --plone-entries-min column knob (the API)"
    )
    assert "--plone-entries-gap" in body or "--plone-space" in body, (
        ".entries gap must come from a --plone-* token, not a hardcoded length"
    )


def test_no_container_queries_anywhere(bundle):
    """The elastic layout needs no container queries."""
    assert "@container" not in bundle, "container query found — §5 is deferred"
    assert "container-type" not in bundle, "container-type found — §5 is deferred"


# --------------------------------------------------------------------------- #
# 2. The item / summary hooks are Plone's own, reused verbatim (not invented).
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("selector", [".entries>.item", ".entries>.summary"])
def test_listing_item_hooks_present(flat, selector):
    """Each listing row is styled through Plone's own `.item` / `.summary`
    hook under `.entries`, never a bespoke wrapper class."""
    assert selector in flat, f"expected reused hook {selector!r} to be styled"


def test_description_hook_is_muted(flat):
    """`.description` (stock listing/summary field) reads as secondary text."""
    assert ".description" in flat, ".description hook is not styled"


# --------------------------------------------------------------------------- #
# 3. Album: a flexbin-style justified grid on Plone's `.card.album`, elastic.
# --------------------------------------------------------------------------- #

def test_album_card_is_a_flexbin_item(bundle, flat):
    """`.card.album` justifies flexbin-style: it `flex-grow`s to fill each row
    (variable width, equal height) instead of stock's fixed equal-width cols.
    A `--plone-album-*` knob tunes the row — elastic, no query context."""
    assert ".card.album" in flat, ".card.album is not styled"
    bodies = _rule(bundle, ".card.album")
    assert bodies, ".card.album has no own rule"
    assert "flex-grow" in bodies[0], (
        ".card.album must flex-grow (flexbin justification); got "
        f"{bodies[0]!r}"
    )
    assert "--plone-album" in "".join(bodies) + flat, (
        "album layout must expose a --plone-album-* tuning knob"
    )


def test_album_container_is_flex(bundle):
    """The album container is the REUSED `.entries` hook with an `.album`
    modifier (no new structural class), laid out with flexbox (wrap + gap) —
    the justified row model flexbin needs, which `.entries`' grid can't give."""
    bodies = _rule(bundle, ".entries.album")
    assert bodies, ".entries.album album container is not styled"
    body = bodies[0]
    assert "display:flex" in body and "flex-wrap:wrap" in body, (
        f".entries.album must be a wrapping flexbox; got {body!r}"
    )
    assert "--plone-album" in body, "album container must expose a --plone-album-* knob"


# --------------------------------------------------------------------------- #
# 4. Reuse over invent: the Bootstrap card/table are restyled through the
#    bridge; NO parallel .plone-card / .plone-listing is minted.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("invented", [".plone-card", ".plone-listing", ".plone-entries"])
def test_does_not_invent_parallel_hooks(flat, invented):
    """The card/listing hooks are Plone's own, never a parallel `.plone-card`."""
    assert invented not in flat, f"invented hook {invented!r} — reuse Plone's own"


def test_card_restyled_through_the_bridge(bundle):
    """The `.card` spacers are rebound at `.card` scope, where Bootstrap pins
    them; a :root-only rebind would be shadowed."""
    bodies = _rule(bundle, ".card")
    assert bodies, ".card has no own rule"
    joined = "".join(bodies)
    assert re.search(r"--bs-card-spacer-x\s*:\s*var\(--plone-space[\w-]*\)", joined), (
        ".card must rebind --bs-card-spacer-x onto --plone-space at COMPONENT "
        "scope (a :root-only bridge is shadowed by Bootstrap's own .card scope)"
    )


# --------------------------------------------------------------------------- #
# 5. Namespace: --plone-* is the shared contract; --clara-* is Clara's own
#    non-contract vocabulary (the Klarsicht ladder, type tiers, component
#    knobs), deliberately in the bundle since the clara-base redesign. The
#    guard is against DANGLING reads, not against the namespace itself.
# --------------------------------------------------------------------------- #

def test_clara_tokens_read_are_declared(bundle):
    """Every fallback-less var(--clara-…) read must be declared somewhere in
    the bundle — a dangling read is a typo or a renamed ladder step. Reads
    carrying a fallback (integrator knobs like --clara-megamenu-col) resolve
    by design and are exempt."""
    declared = set(re.findall(r"(--clara-[\w-]+)\s*:", bundle))
    fallbackless_reads = set(re.findall(r"var\(\s*(--clara-[\w-]+)\s*\)", bundle))
    dangling = fallbackless_reads - declared
    assert not dangling, f"dangling --clara-* reads in the bundle: {sorted(dangling)}"
