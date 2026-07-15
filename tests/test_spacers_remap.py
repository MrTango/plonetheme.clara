"""§7 `$spacers` remap: the end-to-end runtime proof (wayfinder ticket 05).

The spec's §7 promise: *any* third-party `.mb-3` / `.p-2` resolves to a
`--plone-space-*` value — fluid and on-scale — instead of Bootstrap's flat
hardcoded rem. Ticket 04 already grep-verified the remapped rule is *present*
in the compiled bundle. This module is the ticket-05 job: prove the whole
`.mb-3 → var(--plone-space-s) → clamp(...)` chain is actually *wired* end to
end, so a browser has a real length to compute — and prove the documented
§7 tradeoff (utilities shipped, never used in Clara's own markup) holds.

It is deliberately a text-parsing check on the *compiled* `clara.min.css`, in
the same no-Sass/no-browser harness as test_token_drift.py, because every real
failure mode here is an *authoring* failure the cascade can't paper over:

  * a typo'd token name (`.mb-3 → var(--plone-spaces-s)`) → dangling var,
  * the `--plone-space-*` token missing from the shipped `:root`,
  * a later rule in the cascade redefining `.mb-3` back to a flat rem,
  * `$spacers` accidentally `map-remove`d, so the utilities never generate.

Each is caught below. The one thing a text check cannot do — watch a browser
resolve `clamp()` to px at a given viewport — is covered by the sibling
fixture `tests/fixtures/spacers-proof.html`, which reads back
`getComputedStyle` live in any real engine (see the module docstring there and
the ticket answer for the measured values).
"""
import re
from pathlib import Path

import pytest


BUNDLE = (
    Path(__file__).resolve().parent.parent
    / "src" / "plonetheme" / "clara" / "static" / "clara.min.css"
)
SCSS = Path(__file__).resolve().parent.parent / "theme" / "scss"

#: The §7 map authored in clara-bootstrap.scss: Bootstrap spacer step → the
#: --plone-space-* token it must remap onto. Step 0 is the literal `0`.
SPACERS = {
    0: "0",
    1: "var(--plone-space-3xs)",
    2: "var(--plone-space-2xs)",
    3: "var(--plone-space-s)",
    4: "var(--plone-space-m)",
    5: "var(--plone-space-xl)",
}

#: The spec's named guarantee, called out verbatim in the ticket.
HEADLINE = (".mb-3", "var(--plone-space-s)")


def _strip_block_comments(text):
    """CSS `/* … */` only. NOT `//` — the compiled bundle has no `//`
    line-comments (compressed Sass strips them), but it does carry `http://`
    inside SVG data URIs, so a `//`-to-EOL strip would eat half the file."""
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


def _strip_scss_comments(text):
    """SCSS source: drop both `/* … */` blocks and `//` line comments."""
    text = _strip_block_comments(text)
    return re.sub(r"//[^\n]*", "", text)


@pytest.fixture(scope="module")
def bundle():
    assert BUNDLE.exists(), (
        f"compiled bundle missing at {BUNDLE} — run `npm install` (or "
        f"`npm run build`) in plonetheme.clara first."
    )
    return _strip_block_comments(BUNDLE.read_text())


def _rule(bundle, selector):
    """Return every declaration body compiled for an exact `.selector{...}`."""
    return re.findall(re.escape(selector) + r"\{([^}]*)\}", bundle)


# --------------------------------------------------------------------------- #
# 1. The remap: every $spacers step lands on its Clara token, foreign markup.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("step,token", SPACERS.items())
def test_margin_utility_remaps_to_clara_token(bundle, step, token):
    """A foreign Bootstrap `.mb-N` compiles to the Clara space token, not a
    hardcoded rem. `.mb-*` is markup Clara never authors (see the tradeoff
    test) — this is precisely the third-party-utility case §7 promises."""
    bodies = _rule(bundle, f".mb-{step}")
    assert bodies, f".mb-{step} is not in the compiled bundle at all"
    expected = "0" if step == 0 else token
    assert bodies[0] == f"margin-bottom:{expected} !important", (
        f".mb-{step} compiled to {bodies[0]!r}; expected the §7 remap onto "
        f"{expected!r}. Check the $spacers map in clara-bootstrap.scss."
    )


def test_padding_utility_also_remaps(bundle):
    """The remap is $spacers-wide, not margin-only: a foreign `.p-2` lands on
    the same fluid token (the ticket names `.p-2` explicitly)."""
    bodies = _rule(bundle, ".p-2")
    assert bodies, ".p-2 is not in the compiled bundle"
    assert bodies[0] == "padding:var(--plone-space-2xs) !important", bodies[0]


def test_headline_guarantee(bundle):
    """The spec's flagship line: a third-party `.mb-3` → var(--plone-space-s)."""
    selector, token = HEADLINE
    assert _rule(bundle, selector)[0] == f"margin-bottom:{token} !important"


# --------------------------------------------------------------------------- #
# 2. The chain lands: each referenced token is really defined and resolves to
#    a concrete fluid clamp() — no dangling var(), the true runtime failure.
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "token",
    sorted({v for v in SPACERS.values() if v != "0"}),
)
def test_referenced_token_is_defined_and_fluid(bundle, token):
    """Every `--plone-space-*` a utility points at is actually declared in the
    shipped bundle and resolves to a `clamp(...)` — so the browser has a real,
    fluid length to compute. A missing token here = a `.mb-3` that silently
    computes to `0` at runtime; that is the bug this test exists to catch."""
    name = re.fullmatch(r"var\(--([\w-]+)\)", token).group(1)
    decls = re.findall(rf"--{re.escape(name)}\s*:\s*([^;]+);", bundle)
    assert decls, f"utility references --{name} but it is never defined in the bundle"
    value = decls[0].strip()
    assert value.startswith("clamp("), (
        f"--{name} = {value!r}; §7 space tokens must be fluid clamp() values"
    )


# --------------------------------------------------------------------------- #
# 3. Utility API stays ENABLED (the defended compat tradeoff): the full step
#    set generates — $spacers was not map-remove'd — and nothing shadows it.
# --------------------------------------------------------------------------- #

def test_utility_api_not_removed(bundle):
    """All six margin-bottom steps exist. If §7 had `map-remove`d the utilities
    to force use of the raw tokens, the higher steps would vanish; the ticket's
    tradeoff is the opposite choice — ship the whole utility API, remapped."""
    for step in SPACERS:
        assert _rule(bundle, f".mb-{step}"), f".mb-{step} missing — utilities trimmed?"


def test_remap_not_shadowed(bundle):
    """`.mb-3` is defined exactly once, so no later rule in the cascade quietly
    restores a flat rem after the remap."""
    assert len(_rule(bundle, ".mb-3")) == 1


# --------------------------------------------------------------------------- #
# 4. The §7 tradeoff holds: utilities are shipped for foreign markup but Clara
#    never authors them itself (declarative hooks + tokens, not utility soup).
# --------------------------------------------------------------------------- #

def test_clara_markup_never_uses_spacing_utilities():
    """Clara's own SCSS authors zero Bootstrap spacing-utility selectors
    (`.m*-N` / `.p*-N`). The utilities exist only for third-party markup; Clara
    styles itself through named hooks and `--plone-*` tokens. This is the §7
    tradeoff made checkable — and the reason the remap is safe to ship."""
    offenders = []
    utility = re.compile(r"\.[mp][tbsexy]?-[0-9]")
    for scss in sorted(SCSS.glob("_clara-*.scss")) + [SCSS / "clara.scss"]:
        for lineno, line in enumerate(_strip_scss_comments(scss.read_text()).splitlines(), 1):
            if utility.search(line):
                offenders.append(f"{scss.name}:{lineno}: {line.strip()}")
    assert not offenders, (
        "Clara authors Bootstrap spacing utilities in its own SCSS (violates "
        "the §7 tradeoff — use named hooks + --plone-* tokens instead):\n"
        + "\n".join(offenders)
    )
