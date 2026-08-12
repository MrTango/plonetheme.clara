"""Dark mode must actually win over light mode in the SHIPPED bundle.

A plain `[data-bs-theme="dark"]` selector scores 0,1,0 — exactly what `:root`
scores. Both token partials live in the same `tokens` layer, and
`_clara-brand.scss` is imported *after* `_clara-tokens-defaults.scss`, so its
`:root` block used to beat the defaults' dark block on source order alone.
Every role the brand re-states and the dark block moves — background, surface,
text, muted, border, on-primary — silently snapped back to its light value the
moment the switch was flipped.

`tests/test_color_contrast.py` did not catch it: `_dark_props()` overlays the
partials in import order, which models a cascade the browser never runs. Both
dark blocks now carry a doubled attribute selector (0,2,0), so dark always wins
over light regardless of import order — and `[data-bs-theme]` stays usable on
any element, so scoped dark regions keep working.

This test reads the compiled bundle, not the Sass, because the defect only
exists in the assembled cascade.
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

pytestmark = pytest.mark.skipif(
    not BUNDLE.is_file(),
    reason="clara.min.css is gitignored; run `npm run build` first",
)

#: Roles the dark block moves that a later `:root` would otherwise undo.
DARK_ONLY_ROLES = [
    "--plone-color-bg",
    "--plone-color-surface",
    "--plone-color-text",
    "--plone-color-muted",
    "--plone-color-border",
]


def _css():
    return BUNDLE.read_text()


def _token_layer(css):
    """Concatenate every `@layer tokens { … }` region of the bundle.

    Scoped deliberately: Bootstrap's own `[data-bs-theme=dark]` block (in the
    later `bootstrap` layer) and the toolbar's (in `components`, ordered after
    its light sibling) are both correct where they sit. The defect was specific
    to the `tokens` layer, where two partials both write `:root`.
    """
    regions = []
    for match in re.finditer(r"@layer tokens\s*\{", css):
        depth, start = 0, match.end() - 1
        for index in range(start, len(css)):
            if css[index] == "{":
                depth += 1
            elif css[index] == "}":
                depth -= 1
                if depth == 0:
                    regions.append(css[start + 1 : index])
                    break
    assert regions, "no @layer tokens region in the bundle"
    return "\n".join(regions)


def test_no_dark_block_in_the_token_layer_is_left_at_root_specificity():
    """Every dark token block must outscore `:root`, not merely follow it."""
    weak = re.findall(
        r"(?<![\]\w])\[data-bs-theme=[\"']?dark[\"']?\]\s*\{", _token_layer(_css())
    )
    assert not weak, (
        f"{len(weak)} dark block(s) in @layer tokens still score 0,1,0 and can "
        "be undone by a later :root in the same layer — double the attribute "
        "selector"
    )


def test_dark_blocks_keep_element_level_scoping():
    """`:root[data-bs-theme=dark]` would fix specificity and break scoping.

    Bootstrap allows `data-bs-theme` on any element; a scoped dark region has
    to keep receiving the token flips.
    """
    assert ":root[data-bs-theme" not in _css()


@pytest.mark.parametrize("role", DARK_ONLY_ROLES)
def test_dark_mode_actually_moves_the_neutral_roles(role):
    """The regression itself: these must survive to the end of the cascade."""
    css = _css()
    dark_blocks = re.findall(
        r"\[data-bs-theme=[\"']?dark[\"']?\]\[data-bs-theme=[\"']?dark[\"']?\]\s*\{([^}]*)\}",
        css,
    )
    assert dark_blocks, "no doubled dark block found in the bundle"
    declared = [
        block for block in dark_blocks if re.search(rf"{re.escape(role)}\s*:", block)
    ]
    assert declared, f"{role} is never re-declared for dark mode"


def test_light_and_dark_disagree_on_the_page_ground():
    """A sanity check that the two modes are not the same stylesheet twice."""
    css = _css()
    light = re.search(r":root\s*\{[^}]*--plone-color-bg\s*:\s*([^;}]+)", css)
    dark = re.search(
        r"\[data-bs-theme=[\"']?dark[\"']?\]\[data-bs-theme=[\"']?dark[\"']?\]\s*\{"
        r"[^}]*--plone-color-bg\s*:\s*([^;}]+)",
        css,
    )
    assert light and dark
    assert light.group(1).strip() != dark.group(1).strip()
