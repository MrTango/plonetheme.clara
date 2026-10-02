/* Geometry of the published aurora-blocks-view, for theme-parity.e2e.js.
 *
 * `measureBlocksView` runs in the page: playwright serialises its source, so
 * it must not close over anything.
 *
 *   contentWidth  the column the theme hands the blocks: the view's client box
 *                 minus its own gutters (--aurora-view-gutter, 0 on a phone).
 *                 The theme owns this number, so it is normalised for, never
 *                 failed on.
 *   expected      min(contentWidth, blockWidth token), with the tokens read
 *                 off the view rather than hardcoded; `full` is the 100vw
 *                 breakout, so the viewport.
 *   parts         the inner boxes a theme can move on their own: figure,
 *                 picture, img, iframe, teaser card, listing items, table,
 *                 columns. A theme that leaves images inline gives `picture` a
 *                 line box, and the descender space pads every figure.
 */

function measureBlocksView() {
  const view = document.querySelector(".aurora-blocks-view");
  if (!view) throw new Error("no .aurora-blocks-view on the page");

  const round = (value) => Math.round(value * 100) / 100;
  const box = (element) => {
    const rect = element.getBoundingClientRect();
    return { w: round(rect.width), h: round(rect.height) };
  };
  const boxOf = (root, selector) => {
    const found = root.querySelector(selector);
    return found ? box(found) : null;
  };

  const viewStyle = getComputedStyle(view);
  const contentWidth = round(
    view.clientWidth -
      parseFloat(viewStyle.paddingLeft) -
      parseFloat(viewStyle.paddingRight),
  );
  // An in-flow probe: the tokens are percentages of the content column, which
  // an absolutely positioned probe would resolve against the window instead.
  const token = (name) => {
    const probe = document.createElement("div");
    probe.style.cssText = `position:relative;visibility:hidden;height:0;width:var(${name})`;
    view.appendChild(probe);
    const width = probe.getBoundingClientRect().width;
    probe.remove();
    return round(width);
  };
  const tokens = {
    narrow: token("--narrow-container-width"),
    default: token("--default-container-width"),
    layout: token("--layout-container-width"),
  };

  const blocks = [...view.children].map((element, index) => {
    const widthToken = (element.className.match(/has--block-width--(\w+)/) || [])[1];
    const expected =
      widthToken === "full"
        ? round(window.innerWidth)
        : Math.min(contentWidth, tokens[widthToken] ?? Infinity);
    return {
      index,
      type: element.dataset.blockType || element.tagName.toLowerCase(),
      widthToken,
      expected: round(expected),
      box: box(element),
      parts: {
        figure: boxOf(element, "figure"),
        picture: boxOf(element, "picture"),
        img: boxOf(element, "img"),
        iframe: boxOf(element, "iframe"),
        teaserItem: boxOf(element, ".teaser-item"),
        teaserImage: boxOf(element, ".teaser-image-wrapper"),
        teaserContent: boxOf(element, ".teaser-content"),
        listingItems: [...element.querySelectorAll(".listing-items > .item")].map(box),
        table: boxOf(element, "table"),
        columns: [...element.querySelectorAll(".column")].map(box),
      },
    };
  });

  return {
    viewport: { w: window.innerWidth, h: window.innerHeight },
    contentWidth,
    blocks,
    // what the page is themed with, so a run names the pair it compared
    stylesheets: [...document.querySelectorAll('link[rel="stylesheet"]')]
      .map((link) => link.getAttribute("href") || "")
      .map((href) => href.replace(/^.*\//, "").replace(/\?.*$/, ""))
      .sort(),
  };
}

/** Open a published fixture page at one viewport width and measure it.
 * The page stays open for a screenshot; the caller closes it. */
async function measureAt(browser, url, viewportWidth) {
  const page = await browser.newPage({
    viewport: { width: viewportWidth, height: 900 },
  });
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  // domcontentloaded: `load` would wait on the YouTube embeds
  await page.goto(url, { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".aurora-blocks-view .block-listing .item", {
    timeout: 30000,
  });
  // Load every lazy image first: an unloaded one keeps the box its
  // width/height attributes reserve, a loaded one the served scale's ratio,
  // and the two differ in the last decimal.
  await page.evaluate(
    () =>
      new Promise((resolve) => {
        const images = [...document.images];
        let pending = images.length;
        if (!pending) return resolve();
        const done = () => --pending || resolve();
        for (const image of images) {
          image.loading = "eager";
          if (image.complete) done();
          else {
            image.addEventListener("load", done, { once: true });
            image.addEventListener("error", done, { once: true });
          }
        }
      }),
  );
  // then wait for the layout to stop moving
  await page.waitForFunction(
    () => {
      const height = document.querySelector(".aurora-blocks-view").scrollHeight;
      const settled = window.__auroraLastHeight === height;
      window.__auroraLastHeight = height;
      return settled;
    },
    null,
    { polling: 250, timeout: 15000 },
  );
  const measured = await page.evaluate(measureBlocksView);
  measured.pageErrors = errors;
  return { page, measured };
}

// sub-pixel: layout is fractional, a theme's differences are not
const APPROX = 0.5;

const near = (a, b) => Math.abs(a - b) <= APPROX;

/** `940x568.3`, or `-` for a part the block does not have. */
function fmt(value) {
  if (!value) return "-";
  if (typeof value === "number") return String(Math.round(value * 10) / 10);
  return `${Math.round(value.w * 10) / 10}x${Math.round(value.h * 10) / 10}`;
}

const pad = (value, width) => String(value).padEnd(width);

/** `image/default`: enough to name a block in a message. */
const label = (block) => `${block.type}/${block.widthToken}`;

module.exports = { measureAt, near, fmt, pad, label };
