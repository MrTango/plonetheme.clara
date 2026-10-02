/* Clara must not reach into the Aurora editor's blocks.
 *
 * Builds the same Article (theme-fixture.js) on two Plone sites, one on
 * Barceloneta and one on Clara, and measures its published blocks
 * anonymously at four viewport widths.
 *
 * The one legitimate difference is the content column the theme hands the
 * blocks view: Clara caps it, Barceloneta does not, so a `layout` block is
 * narrower under Clara. Each block's expected width is therefore
 * min(content column, blockWidth token). Where that agrees on both sites,
 * the block box and every inner box must match to half a pixel; where it
 * does not, the block is reported with the column that explains it and not
 * failed on (text rewraps, nothing else is comparable).
 *
 * The side-by-side table prints on every run. The script refuses to run when
 * both sites load the same stylesheets: a theme compared with itself passes.
 *
 * Run by tests/test_theme_parity.py; by hand:
 *
 *   AURORA_E2E_BASE=<plain site URL> AURORA_E2E_BASE_THEMED=<Clara site URL> \
 *   node theme-parity.e2e.js
 */
const path = require("node:path");
const { chromium } = require("playwright-core");
const { createFixture, removeFixture } = require("./theme-fixture");
const { measureAt, near, fmt, pad, label } = require("./theme-measure");

const BASE = process.env.AURORA_E2E_BASE;
const THEMED = process.env.AURORA_E2E_BASE_THEMED;
const EXECUTABLE = process.env.AURORA_E2E_CHROMIUM;
// where a failing viewport leaves full-page screenshots of both sites
const ARTIFACTS = process.env.AURORA_E2E_ARTIFACTS;
const VIEWPORTS = [1400, 1200, 992, 768];

// A block box can match while the media inside it does not.
const PARTS = [
  "figure",
  "picture",
  "img",
  "iframe",
  "teaserItem",
  "teaserImage",
  "teaserContent",
  "table",
];
const PART_LISTS = ["listingItems", "columns"];

/** Every inner-box difference between the same block on the two sites. */
function diffParts(a, b) {
  const differences = [];
  for (const part of PARTS) {
    const one = a.parts[part];
    const other = b.parts[part];
    if (!one && !other) continue;
    if (!one || !other) {
      differences.push(`${part} ${fmt(one)} vs ${fmt(other)} (missing on one site)`);
      continue;
    }
    if (!near(one.w, other.w) || !near(one.h, other.h)) {
      differences.push(`${part} ${fmt(one)} vs ${fmt(other)}`);
    }
  }
  for (const part of PART_LISTS) {
    const one = a.parts[part];
    const other = b.parts[part];
    if (one.length !== other.length) {
      differences.push(`${part}: ${one.length} vs ${other.length}`);
      continue;
    }
    one.forEach((box, index) => {
      if (!near(box.w, other[index].w) || !near(box.h, other[index].h)) {
        differences.push(`${part}[${index}] ${fmt(box)} vs ${fmt(other[index])}`);
      }
    });
  }
  return differences;
}

/** Both sites must render the same document before it is compared. */
function assertSameDocument(a, b) {
  if (a.blocks.length !== b.blocks.length) {
    throw new Error(
      `the two sites render ${a.blocks.length} and ${b.blocks.length} blocks — ` +
        `the fixture is not identical, so nothing below is comparable`,
    );
  }
  a.blocks.forEach((block, index) => {
    const other = b.blocks[index];
    if (block.type !== other.type || block.widthToken !== other.widthToken) {
      throw new Error(
        `block ${index} is ${label(block)} on one site and ${label(other)} on ` +
          `the other — the fixture is not identical`,
      );
    }
  });
}

function compareViewport(base, themed) {
  assertSameDocument(base, themed);
  console.log(
    `\nviewport ${base.viewport.w}px — content column: ` +
      `base ${fmt(base.contentWidth)}px, themed ${fmt(themed.contentWidth)}px` +
      (near(base.contentWidth, themed.contentWidth)
        ? ""
        : ` (${fmt(themed.contentWidth - base.contentWidth)}px)`),
  );
  console.log(`  ${pad("#", 3)}${pad("block", 22)}${pad("base", 16)}${pad("themed", 16)}verdict`);

  const mismatches = [];
  const explained = [];
  for (const [index, block] of base.blocks.entries()) {
    const other = themed.blocks[index];
    let verdict;
    if (!near(block.expected, other.expected)) {
      // the columns clamp this block differently: text rewraps, so neither
      // its height nor its inner boxes mean anything here
      verdict =
        `content column (${fmt(block.expected)} vs ${fmt(other.expected)} = ` +
        `min(column, ${block.widthToken}))`;
      explained.push(label(block));
    } else {
      const differences = [];
      if (!near(block.box.w, other.box.w) || !near(block.box.h, other.box.h)) {
        differences.push(`block box ${fmt(block.box)} vs ${fmt(other.box)}`);
      }
      differences.push(...diffParts(block, other));
      if (differences.length) {
        verdict = `THEME DIFFERENCE: ${differences.join("; ")}`;
        mismatches.push(
          `@${base.viewport.w}px ${label(block)} (both ${fmt(block.expected)}px ` +
            `wide): ${differences.join("; ")}`,
        );
      } else {
        verdict = "equal";
      }
    }
    console.log(
      `  ${pad(index, 3)}${pad(label(block), 22)}${pad(fmt(block.box), 16)}` +
        `${pad(fmt(other.box), 16)}${verdict}`,
    );
  }
  if (explained.length) {
    console.log(
      `  ${explained.length} block(s) differ only because the content ` +
        `columns differ: ${[...new Set(explained)].join(", ")}`,
    );
  }
  return mismatches;
}

/** A run that compares a theme with itself passes for the wrong reason. */
function assertDifferentThemes(base, themed) {
  const one = base.stylesheets.join(" ");
  const other = themed.stylesheets.join(" ");
  if (one === other) {
    throw new Error(
      `both sites load the same stylesheets (${one || "none"}) — they are ` +
        `running the same theme, so this comparison would prove nothing`,
    );
  }
  console.log(`base stylesheets:   ${one}`);
  console.log(`themed stylesheets: ${other}`);
}

async function screenshot(page, width, name) {
  await page.screenshot({
    path: path.join(ARTIFACTS, `theme-parity-${width}-${name}.png`),
    fullPage: true,
  });
}

async function main() {
  if (!BASE || !THEMED) {
    throw new Error(
      "AURORA_E2E_BASE (the plain site) and AURORA_E2E_BASE_THEMED (the Clara " +
        "site) are both required: run the script through tests/test_theme_parity.py",
    );
  }
  const urls = {
    base: await createFixture(BASE),
    themed: await createFixture(THEMED),
  };
  console.log(`base:   ${urls.base}`);
  console.log(`themed: ${urls.themed}`);

  // full Chromium in new headless mode, as CI installs it (--no-shell)
  const browser = await chromium.launch(
    EXECUTABLE ? { executablePath: EXECUTABLE } : { channel: "chromium" },
  );
  const mismatches = [];
  try {
    for (const [viewportIndex, width] of VIEWPORTS.entries()) {
      const base = await measureAt(browser, urls.base, width);
      const themed = await measureAt(browser, urls.themed, width);
      if (viewportIndex === 0) assertDifferentThemes(base.measured, themed.measured);
      const found = [];
      for (const [name, { measured }] of [
        ["base", base],
        ["themed", themed],
      ]) {
        for (const error of measured.pageErrors) {
          found.push(`@${width}px ${name}: uncaught page error: ${error}`);
        }
      }
      found.push(...compareViewport(base.measured, themed.measured));
      if (found.length && ARTIFACTS) {
        await screenshot(base.page, width, "base");
        await screenshot(themed.page, width, "themed");
      }
      await base.page.close();
      await themed.page.close();
      mismatches.push(...found);
    }
  } finally {
    await browser.close();
    await removeFixture(BASE);
    await removeFixture(THEMED);
  }

  if (mismatches.length) {
    console.error(`\n${mismatches.length} block(s) measure differently at the same width:`);
    for (const mismatch of mismatches) console.error(`  - ${mismatch}`);
    throw new Error(`${mismatches.length} theme-dependent block size(s)`);
  }
  console.log("\nPASS");
}

main().catch((error) => {
  console.error("FAIL:", error.message || error);
  process.exit(1);
});
