"""Runtime semantic-state mappings in Clara's compiled bundle."""
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


@pytest.fixture(scope="module")
def bundle():
    assert BUNDLE.exists(), "run `npm run build` before pytest"
    return re.sub(r"/\*.*?\*/", "", BUNDLE.read_text(), flags=re.DOTALL)


def _bodies(bundle, selector):
    return re.findall(re.escape(selector) + r"\s*\{([^}]*)\}", bundle)


def _has_mapping(bundle, selector, component_token, semantic_token):
    body = "".join(_bodies(bundle, selector))
    return bool(
        re.search(
            re.escape(component_token)
            + r"\s*:\s*var\("
            + re.escape(semantic_token)
            + r"\)",
            body,
        )
    )


@pytest.mark.parametrize("state", ["primary", "success", "warning", "danger", "info"])
def test_button_variants_use_runtime_semantic_roles(bundle, state):
    selector = f".btn-{state}"
    semantic = "--plone-color-on-primary" if state == "primary" else f"--plone-color-on-{state}"
    assert _has_mapping(bundle, selector, "--bs-btn-color", semantic)


@pytest.mark.parametrize("state", ["success", "warning", "danger", "info"])
def test_alert_variants_use_runtime_semantic_surfaces(bundle, state):
    selector = ".alert-info,.alert-primary" if state == "info" else f".alert-{state}"
    assert _has_mapping(
        bundle,
        selector,
        "--bs-alert-bg",
        f"--plone-color-{state}-surface",
    )
    assert _has_mapping(
        bundle,
        selector,
        "--bs-alert-color",
        f"--plone-color-{state}-text",
    )


def test_form_validation_uses_semantic_boundaries(bundle):
    assert "--plone-color-success-border" in bundle
    assert "--plone-color-danger-border" in bundle
    assert ".valid-feedback" in bundle
    assert ".invalid-feedback" in bundle


def test_busy_button_has_reduced_motion_alternative(bundle):
    assert ".btn[aria-busy=true]::after" in bundle
    reduced = re.findall(
        r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(.*)",
        bundle,
    )
    assert reduced and "animation:none" in reduced[0]


def test_compiled_bundle_exposes_no_quanta_namespace(bundle):
    assert "--quanta-" not in bundle
