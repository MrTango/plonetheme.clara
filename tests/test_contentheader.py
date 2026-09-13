"""The content header's layout API in the SHIPPED bundle (architecture §1.7).

Title and description lay out on one elastic grid read from three
``--plone-contentheader-*`` tokens. Clara's own defaults must keep the classic
stack, and a site must be able to put the description beside the title by
moving one token — with no media query in the way. Read from the compiled
bundle, like the other component proofs, because the cascade is what a site
inherits.
"""

import re
from pathlib import Path

import pytest


BUNDLE = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "plonetheme"
    / "clara"
    / "static"
    / "clara.min.css"
)

TOKENS = {
    "--plone-contentheader-threshold": "100vw",
    "--plone-contentheader-gap": "var(--plone-space-m)",
    "--plone-contentheader-align": "start",
    "--plone-contentheader-justify": "start",
    "--plone-contentheader-title-grow": "1",
    "--plone-contentheader-description-grow": "1",
}
SWITCH = "calc((var(--plone-contentheader-threshold) - 100%)*999)".replace(" ", "")


@pytest.fixture(scope="module")
def bundle():
    assert BUNDLE.exists(), f"compiled bundle missing at {BUNDLE}"
    return re.sub(r"/\*.*?\*/", "", BUNDLE.read_text(), flags=re.DOTALL)


def _rule(bundle, selector):
    """The declaration body of `selector`, whitespace-free for literal checks."""
    flat = re.sub(r"\s+", "", bundle)
    bodies = re.findall(re.escape(selector) + r"\{([^}]*)\}", flat)
    assert bodies, f"no rule for {selector!r} in the bundle"
    return re.sub(r"\s+", "", bodies[0])


def _at_rule_bodies(bundle, name):
    """The balanced body of every `@<name>` block in the bundle."""
    for match in re.finditer(rf"@{name}[^{{]*\{{", bundle):
        depth, start = 1, match.end()
        for position in range(start, len(bundle)):
            depth += {"{": 1, "}": -1}.get(bundle[position], 0)
            if depth == 0:
                yield bundle[start:position]
                break


@pytest.mark.parametrize("name,default", sorted(TOKENS.items()))
def test_token_is_declared_with_the_classic_default(bundle, name, default):
    declared = re.findall(rf"{re.escape(name)}\s*:\s*([^;}}]+)", bundle)
    assert declared, f"{name} is not declared on the root"
    assert declared[0].strip() == default


def test_header_is_a_switcher_read_from_the_tokens(bundle):
    """The §3 switcher idiom: the pair goes two-up from `threshold`, and each
    half's share of the row is its grow token."""
    body = _rule(bundle, ".element-contentheader")
    assert "display:flex" in body
    assert "flex-wrap:wrap" in body
    assert "var(--plone-contentheader-gap)" in body
    assert "align-items:var(--plone-contentheader-align)" in body
    assert "justify-content:var(--plone-contentheader-justify)" in body
    assert f"flex:var(--plone-contentheader-title-grow)1{SWITCH}" in _rule(bundle, TITLE)
    assert f"flex:var(--plone-contentheader-description-grow)1{SWITCH}" in _rule(
        bundle, DESCRIPTION
    )


def test_header_reaches_two_columns_without_a_media_query(bundle):
    for body in _at_rule_bodies(bundle, "media"):
        assert ".element-contentheader" not in body, (
            "the content header's layout must be elastic, not breakpointed"
        )


TITLE = ".element-contentheader>:is(h1,.h1,.documentFirstHeading)"
DESCRIPTION = ".element-contentheader>:is(.lead,.documentDescription)"


def test_managers_take_a_full_row(bundle):
    """Both markups are matched: the pagelet chrome's hooks and the classic
    frame's `context/@@title` (a bare h1) and `@@description` (Plone's
    p.lead). Everything else in the element is a manager's output."""
    assert "flex-basis:100%" in _rule(bundle, ".element-contentheader>*")
    assert "h1," in TITLE and ".lead," in DESCRIPTION


def test_stacked_spacing_is_the_row_gap_alone(bundle):
    """The pair's vertical space is the grid's, not a margin's: the title's
    Bootstrap bottom margin is zeroed and the description carries no top
    margin, so the row gap is the one number that sets it."""
    assert "margin-block-end:0" in _rule(bundle, TITLE)
    assert "margin-block-end:0" in _rule(bundle, DESCRIPTION)
    assert "margin-block-start" not in _rule(bundle, DESCRIPTION)
    assert "gap:var(--plone-space-s)var(--plone-contentheader-gap)" in _rule(
        bundle, ".element-contentheader"
    )
