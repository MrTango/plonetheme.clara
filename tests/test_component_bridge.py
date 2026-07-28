"""Component-scope `--bs-*`→`--plone-*` bridge (wayfinder ticket 13).

Bootstrap 5.3 pins a component's spacing tokens ON THE COMPONENT ROOT
(`.btn{--bs-btn-padding-x:.75rem}`, `.card{--bs-card-spacer-x:1rem}`, `.nav`,
`.alert`, `.breadcrumb`, `.table` striped fill). An element-level declaration
SHADOWS any `:root` value for its descendants, so the `:root` half of
_clara-bridge.scss is DEAD for those tokens — the component keeps Bootstrap's
flat rem, not a Clara token. Ticket 10 caught this on `.card`; ticket 13 fixes
the rest by rebinding at COMPONENT scope (still in the `components` @layer, which
beats `bootstrap`).

This is the permanent, no-browser guard (same harness as
test_content_components.py / test_spacers_remap.py); the live-compute proof is
tests/fixtures/component-bridge-proof.html (a bare `.btn`/`.nav`/`.alert`/…
whose computed padding a real engine resolves to the token, with the `.btn` size
hierarchy intact). It pins two things a `:root`-only bridge silently got wrong:

  * every literal-pinned component token is rebound onto a `--plone-*` token at
    COMPONENT scope (not merely at `:root`), so it actually wins; and
  * the `.btn` size variants keep their OWN distinct padding tokens — because
    the `components` layer beats `bootstrap` regardless of specificity, a lone
    `.btn` rebind would otherwise override `.btn-lg`/`.btn-sm` too and collapse
    every button to one size.
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


def _rules(bundle, selector):
    """All declaration bodies of an exact single-selector `selector{...}` rule
    (the token may be split across Bootstrap's copy and our rebind copy)."""
    return re.findall(re.escape(selector) + r"\s*\{([^}]*)\}", bundle)


def _binds_to_plone(bundle, selector, bs_token):
    """True iff SOME `selector{...}` rule rebinds `bs_token` onto a var(--plone-*)."""
    joined = "".join(_rules(bundle, selector))
    return bool(re.search(re.escape(bs_token) + r"\s*:\s*var\(--plone-[\w-]+\)", joined))


def _plone_token_for(bundle, selector, bs_token):
    """The --plone-* token `selector` rebinds `bs_token` onto, or None."""
    joined = "".join(_rules(bundle, selector))
    m = re.search(re.escape(bs_token) + r"\s*:\s*var\((--plone-[\w-]+)\)", joined)
    return m.group(1) if m else None


# --------------------------------------------------------------------------- #
# 1. Each literal-pinned component token is rebound onto --plone-* at COMPONENT
#    scope. (A :root-only rebind of these is shadowed by Bootstrap's own
#    component-root declaration — the defect this ticket fixes.)
# --------------------------------------------------------------------------- #

#: selector  →  the --bs-* tokens Bootstrap pins as a LITERAL on that root and
#: which therefore MUST be rebound at component scope (not :root) to take effect.
COMPONENT_SCOPED = {
    ".btn": ["--bs-btn-padding-x", "--bs-btn-padding-y"],
    ".card": ["--bs-card-spacer-x", "--bs-card-spacer-y"],
    ".nav": ["--bs-nav-link-padding-x", "--bs-nav-link-padding-y"],
    ".alert": ["--bs-alert-padding-x", "--bs-alert-padding-y"],
    ".breadcrumb": ["--bs-breadcrumb-item-padding-x"],
    ".table": ["--bs-table-striped-bg"],
}


@pytest.mark.parametrize(
    "selector,token",
    [(sel, tok) for sel, toks in COMPONENT_SCOPED.items() for tok in toks],
)
def test_component_token_rebound_at_component_scope(bundle, selector, token):
    """`selector{ token: var(--plone-*) }` exists — the rebind lives on the
    component root where it can beat Bootstrap's shadowing literal, not only at
    :root where it would be dead."""
    assert _binds_to_plone(bundle, selector, token), (
        f"{token} is not rebound onto a --plone-* token at the {selector} "
        f"component scope — a :root-only bridge for it is shadowed by "
        f"Bootstrap's own {selector} declaration and does nothing."
    )


def test_shadowed_tokens_are_not_left_only_at_root(bundle):
    """Guard against a regression to the dead :root pattern: for every
    literal-pinned token, the ONLY place it is declared must not be `:root`.
    (Belt-and-braces over test 1 — proves the fix, not just presence.)"""
    root_bodies = "".join(_rules(bundle, ":root"))
    for selector, tokens in COMPONENT_SCOPED.items():
        for token in tokens:
            in_component = _binds_to_plone(bundle, selector, token)
            in_root = bool(re.search(re.escape(token) + r"\s*:\s*var\(--plone", root_bodies))
            assert in_component, f"{token} missing at {selector} scope"
            # It's fine if it's ALSO at :root, but it must not be ONLY there.
            assert not (in_root and not in_component), (
                f"{token} is rebound only at :root — shadowed, dead."
            )


# --------------------------------------------------------------------------- #
# 2. The .btn size variants survive: because `components` beats `bootstrap`
#    regardless of specificity, the base `.btn` rebind would override .btn-lg/
#    .btn-sm too unless they are re-mapped. Assert each keeps its OWN token and
#    the three are DISTINCT (sm ≠ base ≠ lg → the hierarchy can't collapse).
# --------------------------------------------------------------------------- #

BTN_BASE = ".btn"
BTN_LG = ".btn-lg,.btn-group-lg>.btn"
BTN_SM = ".btn-sm,.btn-group-sm>.btn"


@pytest.mark.parametrize("selector", [BTN_BASE, BTN_LG, BTN_SM])
def test_btn_size_variant_keeps_own_padding_token(bundle, selector):
    """base / lg / sm each rebind --bs-btn-padding-x onto a --plone-space-*
    token of their own (not inheriting the base, which the layer override would
    otherwise force)."""
    token = _plone_token_for(bundle, selector, "--bs-btn-padding-x")
    assert token is not None, (
        f"{selector} does not rebind --bs-btn-padding-x onto a --plone-* token; "
        f"the components-layer base rebind will collapse this size."
    )
    assert "space" in token, f"{selector} button padding should map to the space ramp, got {token}"


def test_btn_size_hierarchy_uses_distinct_tokens(bundle):
    """sm, base and lg map to THREE DIFFERENT space tokens, so the size
    hierarchy cannot be flattened by the component-scope override."""
    tokens = {
        sel: _plone_token_for(bundle, sel, "--bs-btn-padding-x")
        for sel in (BTN_SM, BTN_BASE, BTN_LG)
    }
    assert all(tokens.values()), f"a button size lacks a padding token: {tokens}"
    assert len(set(tokens.values())) == 3, (
        f"button sizes must use distinct space tokens (sm/base/lg), got {tokens}"
    )


def test_btn_border_radius_not_rebound_at_component_scope(bundle):
    """`--bs-btn-border-radius` is deliberately NOT rebound here: `.btn`/`.btn-lg`
    /`.btn-sm` set it to var(--bs-border-radius[-lg|-sm]), which already flows
    from the :root bridge — rebinding it at component scope would be dead
    duplication AND would force the size variants to be re-mapped for radius
    too. Pin that decision so it isn't 'helpfully' re-added."""
    for selector in (BTN_BASE, BTN_LG, BTN_SM):
        assert not _binds_to_plone(bundle, selector, "--bs-btn-border-radius"), (
            f"{selector} rebinds --bs-btn-border-radius onto --plone-* — drop it; "
            f"it already flows through the :root --bs-border-radius bridge."
        )


# --------------------------------------------------------------------------- #
# 3. The `components` layer is declared AFTER `bootstrap`, which is the WHOLE
#    reason a component-scope rebind wins over Bootstrap's own literal.
# --------------------------------------------------------------------------- #

def test_components_layer_beats_bootstrap(bundle):
    """The single `@layer …;` statement orders `components` after `bootstrap`,
    so a same-specificity component rule in `components` wins. Without this the
    whole fix is void."""
    m = re.search(r"@layer\s+([^;{]+);", bundle)
    assert m, "no @layer order declaration found in the bundle"
    order = [name.strip() for name in m.group(1).split(",")]
    assert "bootstrap" in order and "components" in order, order
    assert order.index("components") > order.index("bootstrap"), (
        f"`components` must be declared after `bootstrap`; got {order}"
    )


# --------------------------------------------------------------------------- #
# 4. The genuinely-global tokens stay at :root (they are NOT re-scoped by any
#    component, so :root — in the winning `components` layer — is correct).
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("token", [
    "--bs-body-bg", "--bs-body-color", "--bs-border-color", "--bs-link-color",
    "--bs-table-cell-padding-x",
])
def test_global_tokens_stay_at_root(bundle, token):
    """Body/border/link and the (non-re-scoped) table cell padding are bridged
    once at :root — moving them to component scope would be needless."""
    assert _binds_to_plone(bundle, ":root", token), (
        f"{token} should be bridged onto --plone-* at :root"
    )


# --------------------------------------------------------------------------- #
# 5. Namespace / mechanism hygiene (mirrors test_content_components.py): the
#    bridge introduces ONLY --plone-* and reaches for no container queries.
# --------------------------------------------------------------------------- #

def test_no_container_queries(bundle):
    assert "@container" not in bundle and "container-type" not in bundle, (
        "container query found — §5 stays deferred"
    )


def test_clara_tokens_read_are_declared(bundle):
    """Namespace hygiene, updated for the Klarsicht brand layer: --clara-* is
    Clara's own non-contract vocabulary (the colour ladder, type tiers, named
    component hooks) and is DELIBERATE in the bundle — sub-themes override it
    at runtime exactly like --plone-*. What must never happen is a *dangling*
    read: a fallback-less var(--clara-…) whose token no rule declares (a typo,
    or a renamed ladder step). Reads that carry a fallback (integrator knobs
    like --clara-megamenu-col) are exempt — they resolve by design."""
    declared = set(re.findall(r"(--clara-[\w-]+)\s*:", bundle))
    fallbackless_reads = set(re.findall(r"var\(\s*(--clara-[\w-]+)\s*\)", bundle))
    dangling = fallbackless_reads - declared
    assert not dangling, f"dangling --clara-* reads in the bundle: {sorted(dangling)}"
