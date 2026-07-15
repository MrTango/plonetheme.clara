"""§6.2 literals-drift guard (wayfinder ticket 03 §4, implemented by ticket 04).

Bootstrap's Sass math (color functions, the $theme-colors map, shade/tint of
$primary) needs COMPILE-TIME literals — a var() cannot enter `shade-color()`.
So theme/scss/_clara-tokens.scss duplicates a handful of --plone-* default
values as `$clara-*` literals. Sass cannot read a CSS custom property at build
time, which is *why* the duplication exists — and also why a pure-Sass @error
guard is impossible. This pytest is that guard: a text-parsing check, no
Sass/node, that runs in the normal harness on every commit (+ pre-commit).

Basis = base ⊕ brand, RESOLVED (ticket 03 §4): the literal must equal Clara's
*effective* light-mode default, i.e. _clara-tokens-defaults.scss overlaid by
_clara-brand.scss (brand wins, source order), with the one-level role→primitive
var() indirection resolved. So `$clara-primary #1e6f8e` tracks the BRAND value
(base is #2c7bb6), and `$clara-radius 0.625rem` tracks brand (base 0.5rem).

Exempt (ticket 03 §4): $clara-success/danger/warning/info are compile-only
$theme-colors seeds with NO runtime --plone-* token to compare against — the
guard neither can nor should cover them (see test_state_seeds_are_exempt).
"""
import re
from pathlib import Path

import pytest


SCSS = Path(__file__).resolve().parent.parent / "theme" / "scss"

#: literal $clara-*  ↔  effective runtime --plone-* it must mirror. The Sass
#: literals stay theme-namespaced ($clara-*, Clara's own brand values feeding
#: Bootstrap's compile-time math, never emitted); the runtime tokens they guard
#: are the Plone contract (--plone-*, ticket 09).
OVERLAP = {
    "clara-primary": "plone-color-primary",
    "clara-text": "plone-color-text",
    "clara-bg": "plone-color-bg",
    "clara-border": "plone-color-border",
    "clara-radius": "plone-radius-m",
}

#: compile-only $theme-colors seeds with no runtime token — never compared.
#: Maps each $clara-* seed to the --plone-* contract token it would gain if it
#: ever became runtime-tunable (ticket 10 fog); the guard asserts that token is
#: still absent.
EXEMPT = {
    "clara-success": "plone-color-success",
    "clara-danger": "plone-color-danger",
    "clara-warning": "plone-color-warning",
    "clara-info": "plone-color-info",
}


def _strip_comments(text):
    """Drop /* … */ and // … comments so selectors/props in prose (e.g. the
    header comment that mentions `:root {}`) never get parsed as CSS."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", "", text)
    return text


def _norm(value):
    """Normalise for comparison: trim, collapse whitespace, lowercase hex."""
    value = re.sub(r"\s+", " ", value.strip())
    return value.lower() if value.startswith("#") else value


def _parse_scss_literals(text):
    """`$name: value;` → {name: value}."""
    out = {}
    for name, value in re.findall(r"\$([\w-]+)\s*:\s*([^;]+);", _strip_comments(text)):
        out[name] = value.strip()
    return out


def _root_block(text):
    text = _strip_comments(text)
    """Return the body of the FIRST `:root { … }` block (light mode only,
    excluding any later [data-bs-theme="dark"] block)."""
    start = text.index(":root")
    brace = text.index("{", start)
    depth = 0
    for i in range(brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[brace + 1:i]
    raise AssertionError(":root block not closed")


def _parse_custom_props(text):
    """`--name: value;` inside the :root block → {name: value}."""
    body = _root_block(text)
    out = {}
    for name, value in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", body):
        out[name] = value.strip()
    return out


def _effective_runtime_props():
    """base defaults ⊕ brand override (brand wins), light mode."""
    props = _parse_custom_props((SCSS / "_clara-tokens-defaults.scss").read_text())
    props.update(_parse_custom_props((SCSS / "_clara-brand.scss").read_text()))
    return props


def _resolve(name, props, _seen=None):
    """Resolve a --name to a concrete value, following var(--x[, fallback])
    indirection within the merged prop map."""
    _seen = _seen or set()
    assert name not in _seen, f"cyclic var() reference at --{name}"
    _seen.add(name)
    value = props[name]
    m = re.fullmatch(r"var\(\s*--([\w-]+)\s*(?:,[^)]*)?\)", value.strip())
    if m:
        return _resolve(m.group(1), props, _seen)
    return value


@pytest.fixture(scope="module")
def literals():
    return _parse_scss_literals((SCSS / "_clara-tokens.scss").read_text())


@pytest.fixture(scope="module")
def runtime():
    return _effective_runtime_props()


@pytest.mark.parametrize("literal_name,prop_name", OVERLAP.items())
def test_literal_matches_effective_runtime_default(
    literals, runtime, literal_name, prop_name
):
    """Each guarded $clara-* literal equals the resolved base⊕brand default."""
    assert literal_name in literals, f"missing literal ${literal_name}"
    assert prop_name in runtime, f"missing runtime token --{prop_name}"
    literal = _norm(literals[literal_name])
    effective = _norm(_resolve(prop_name, runtime))
    assert literal == effective, (
        f"DRIFT: ${literal_name} = {literal!r} but effective "
        f"--{prop_name} = {effective!r}. Update theme/scss/_clara-tokens.scss "
        f"to match the runtime default (or vice versa) and rebuild."
    )


def test_state_seeds_are_exempt(literals):
    """The four state seeds exist as literals but have no runtime --plone-*
    token to guard against (documented exemption, ticket 03 §4)."""
    runtime = _effective_runtime_props()
    for name, runtime_name in EXEMPT.items():
        assert name in literals, f"missing state seed ${name}"
        assert runtime_name not in runtime, (
            f"--{runtime_name} now exists as a runtime token; fold ${name} into "
            f"OVERLAP and drop the exemption (ticket 10 fog: runtime state-color "
            f"tokens)."
        )
