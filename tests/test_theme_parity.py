"""Clara must not reach into the Aurora editor's blocks (e2e/theme-parity.e2e.js).

Skipped unless AURORA_E2E_SMOKE=1 and plone.blicca.auroraeditor is installed:
it needs node, `pnpm install` in e2e/ and a Chromium. See e2e/README.md.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser
from pytest_plone import fixtures_factory

from .theme_parity_testing import PLAIN_SITE_ID
from .theme_parity_testing import THEME_PARITY_TESTING


pytestmark = pytest.mark.skipif(
    os.environ.get("AURORA_E2E_SMOKE") != "1",
    reason="browser test: set AURORA_E2E_SMOKE=1 (needs node and Chromium)",
)

E2E_DIR = Path(__file__).resolve().parent.parent / "e2e"
SCRIPT_TIMEOUT = 600

globals().update(fixtures_factory(((THEME_PARITY_TESTING, "theme_parity"),), keep_session=False))


def stylesheets(app, url):
    browser = Browser(app)
    browser.open(url)
    links = re.findall(r"<link\b[^>]*>", browser.contents)
    return " ".join(link for link in links if 'rel="stylesheet"' in link)


class TestThemeParity:
    layer = THEME_PARITY_TESTING

    @pytest.fixture(autouse=True)
    def _setup(self, theme_parity):
        self.app = theme_parity["app"]
        self.themed = theme_parity["portal"]
        self.plain = self.app[PLAIN_SITE_ID]

    def test_one_site_runs_barceloneta_and_the_other_clara(self):
        plain = stylesheets(self.app, self.plain.absolute_url())
        themed = stylesheets(self.app, self.themed.absolute_url())
        assert "barceloneta" in plain
        assert "clara" not in plain
        assert "clara.min.css" in themed
        assert "barceloneta" not in themed

    def test_blocks_measure_the_same_under_barceloneta_and_clara(self):
        self.run_script("theme-parity.e2e.js")

    def run_script(self, script):
        env = dict(
            os.environ,
            AURORA_E2E_BASE=self.plain.absolute_url(),
            AURORA_E2E_BASE_THEMED=self.themed.absolute_url(),
            AURORA_E2E_USER=SITE_OWNER_NAME,
            AURORA_E2E_PASSWORD=SITE_OWNER_PASSWORD,
        )
        result = subprocess.run(
            ["node", script],
            cwd=E2E_DIR,
            env=env,
            capture_output=True,
            text=True,
            timeout=SCRIPT_TIMEOUT,
        )
        output = f"{result.stdout}\n{result.stderr}"
        print(output)  # shown by `pytest -rP`
        assert result.returncode == 0, f"{script} failed:\n{output}"
        lines = result.stdout.splitlines()
        if not any(line.startswith("PASS") for line in lines):
            skipped = [line for line in lines if line.startswith("SKIP: ")]
            if skipped:
                pytest.skip(skipped[0][len("SKIP: ") :])
            pytest.fail(f"{script} did not pass:\n{output}")
