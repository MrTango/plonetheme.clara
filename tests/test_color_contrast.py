"""WCAG contrast guard for Clara's effective runtime colour roles.

The Quanta research notes contained several optimistic ratios calculated from
incorrect RGB approximations. This test resolves the actual shipped hex values
from base ⊕ brand tokens and measures the browser colours directly.
"""
import re
from pathlib import Path

import pytest


SCSS = Path(__file__).resolve().parent.parent / "theme" / "scss"
BASE = (SCSS / "_clara-tokens-defaults.scss").read_text()
BRAND = (SCSS / "_clara-brand.scss").read_text()


def _strip_comments(text):
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.DOTALL)


def _block(text, selector, occurrence=0):
    text = _strip_comments(text)
    matches = list(re.finditer(re.escape(selector) + r"\s*\{", text))
    assert len(matches) > occurrence, f"missing {selector} block"
    brace = text.index("{", matches[occurrence].start())
    depth = 0
    for index in range(brace, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[brace + 1 : index]
    raise AssertionError(f"unclosed {selector} block")


def _props(text, selector, occurrence=0):
    return dict(
        re.findall(r"--([\w-]+)\s*:\s*([^;]+);", _block(text, selector, occurrence))
    )


def _light_props():
    props = _props(BASE, ":root")
    props.update(_props(BRAND, ":root"))
    return props


def _dark_props():
    props = _light_props()
    props.update(_props(BASE, '[data-bs-theme="dark"]'))
    props.update(_props(BRAND, '[data-bs-theme="dark"]'))
    return props


def _resolve(name, props, seen=None):
    seen = set() if seen is None else seen
    assert name not in seen, f"cyclic token at --{name}"
    seen.add(name)
    value = props[name].strip()
    match = re.fullmatch(r"var\(\s*--([\w-]+)\s*(?:,[^)]*)?\)", value)
    return _resolve(match.group(1), props, seen) if match else value.lower()


def _luminance(hex_color):
    assert re.fullmatch(r"#[0-9a-f]{6}", hex_color), hex_color
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        value / 12.92
        if value <= 0.04045
        else ((value + 0.055) / 1.055) ** 2.4
        for value in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(first, second):
    lighter, darker = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def _assert_ratio(props, foreground, background, minimum):
    fg = _resolve(foreground, props)
    bg = _resolve(background, props)
    ratio = _contrast(fg, bg)
    assert ratio >= minimum, (
        f"--{foreground} {fg} on --{background} {bg} is {ratio:.2f}:1; "
        f"needs {minimum}:1"
    )


@pytest.mark.parametrize(
    "foreground,background",
    [
        ("plone-color-text", "clara-ground"),
        ("plone-color-text", "clara-surface"),
        ("plone-color-text", "clara-band"),
        ("plone-color-muted", "clara-ground"),
        ("plone-color-muted", "clara-surface"),
        ("plone-color-muted", "clara-band"),
        ("plone-color-link", "clara-ground"),
        ("plone-color-link", "clara-surface"),
        ("plone-color-link", "clara-band"),
        ("plone-color-link", "clara-band-soft"),
        ("clara-amber-text", "clara-ground"),
        ("clara-amber-text", "clara-band"),
    ],
)
def test_light_text_roles_clear_aa(foreground, background):
    _assert_ratio(_light_props(), foreground, background, 4.5)


def test_exact_logo_blue_has_accessible_control_roles():
    props = _light_props()
    _assert_ratio(props, "plone-color-primary", "clara-ground", 3.0)
    _assert_ratio(props, "plone-color-on-primary", "plone-color-primary", 4.5)


@pytest.mark.parametrize("state", ["success", "warning", "danger", "info"])
def test_semantic_state_family_is_complete_and_accessible(state):
    props = _light_props()
    _assert_ratio(props, f"plone-color-{state}-text", f"plone-color-{state}-surface", 4.5)
    _assert_ratio(props, f"plone-color-{state}-border", f"plone-color-{state}-surface", 3.0)
    _assert_ratio(props, f"plone-color-on-{state}", f"plone-color-{state}", 4.5)


@pytest.mark.parametrize(
    "foreground,background",
    [
        ("plone-color-text", "plone-color-bg"),
        ("plone-color-muted", "plone-color-bg"),
        ("plone-color-link", "plone-color-bg"),
        ("plone-color-link", "plone-color-surface"),
        ("plone-color-success-text", "plone-color-success-surface"),
        ("plone-color-warning-text", "plone-color-warning-surface"),
        ("plone-color-danger-text", "plone-color-danger-surface"),
        ("plone-color-info-text", "plone-color-info-surface"),
    ],
)
def test_dark_text_roles_clear_aa(foreground, background):
    _assert_ratio(_dark_props(), foreground, background, 4.5)


@pytest.mark.parametrize("state", ["success", "warning", "danger", "info"])
def test_dark_state_fills_have_readable_foregrounds(state):
    _assert_ratio(
        _dark_props(),
        f"plone-color-on-{state}",
        f"plone-color-{state}",
        4.5,
    )
