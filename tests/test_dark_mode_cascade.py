"""Dark mode in the compiled bundle: explicit `data-bs-theme="dark"` and the OS
preference both win over the light `:root`, and `data-bs-theme="light"` opts out."""

import re

import pytest

from tests.conftest import BUNDLE


pytestmark = pytest.mark.skipif(
    not BUNDLE.is_file(),
    reason="clara.min.css is missing; run `pnpm run build` first",
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


def _regions(css, opener):
    """The bodies of every `opener { … }` block, braces balanced."""
    regions = []
    for match in re.finditer(opener, css):
        depth, start = 0, match.end() - 1
        for index in range(start, len(css)):
            if css[index] == "{":
                depth += 1
            elif css[index] == "}":
                depth -= 1
                if depth == 0:
                    regions.append(css[start + 1 : index])
                    break
    return regions


def _os_dark_rules(css):
    """`(selector, body)` pairs applied by the OS dark preference."""
    media = "\n".join(_regions(css, r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{"))
    return re.findall(r"([^{}]+)\{([^{}]*)\}", media)


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


@pytest.mark.parametrize("role", DARK_ONLY_ROLES)
def test_os_dark_preference_moves_the_neutral_roles(role):
    """Without an explicit `data-bs-theme`, the OS preference picks dark."""
    declared = [
        body
        for selector, body in _os_dark_rules(_token_layer(_css()))
        if selector.strip() == ":root:not([data-bs-theme=light])"
        and re.search(rf"{re.escape(role)}\s*:", body)
    ]
    assert declared, f"{role} does not follow prefers-color-scheme: dark"


EXPLICIT_DARK = re.compile(r"^(?:\[data-bs-theme=[\"']?dark[\"']?\])+")


def test_every_explicit_dark_rule_also_follows_the_os_preference():
    """Tokens, toolbar and Bootstrap: each dark rule has an OS twin."""
    css = _css()
    os_rules = {
        (selector.strip(), body) for selector, body in _os_dark_rules(css)
    }
    missing = []
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        for selector in selectors.split(","):
            selector = selector.strip()
            if not EXPLICIT_DARK.match(selector):
                continue
            twin = ":root:not([data-bs-theme=light])" + EXPLICIT_DARK.sub("", selector)
            if (twin, body) not in os_rules:
                missing.append(selector)
    assert not missing, f"dark rules without a prefers-color-scheme twin: {missing}"
