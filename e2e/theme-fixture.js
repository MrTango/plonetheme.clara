/* The fixture theme-parity.e2e.js builds on each site: one Article holding
 * every block whose size a theme can move (image, video, teaser and listing at
 * several block widths, the text, list and container blocks), the Image and
 * three News Items they point at. All published, so the page is measured
 * anonymously, without the toolbar. The listing query is scoped to the
 * fixture folder, so both sites render the same three cards.
 *
 * Needs plone.restapi and the `article` profile of plone.blicca.auroraeditor
 * (Article's default view is aurora-blocks-view).
 */
const zlib = require("node:zlib");

const USER = process.env.AURORA_E2E_USER || "admin";
const PASSWORD = process.env.AURORA_E2E_PASSWORD || "admin";
const AUTH = "Basic " + Buffer.from(`${USER}:${PASSWORD}`).toString("base64");

const FOLDER_ID = "clara-e2e-theme-parity";
const PAGE_ID = "parity-page";
const PAGE_PATH = `/${FOLDER_ID}/${PAGE_ID}`;

const VIDEO_URL = "https://www.youtube.com/watch?v=zNzZ1PfUDNk";
const TARGETS = [
  ["target-alpha", "Parity Target Alpha", "First teaser and listing target."],
  ["target-bravo", "Parity Target Bravo", "Second teaser and listing target."],
  ["target-charlie", "Parity Target Charlie", "Third teaser and listing target."],
];
// wraps at every tested viewport, so a block's height follows its width
const PARAGRAPH =
  "Ein Absatz mit genug Text, damit der Zeilenumbruch und die Blockhoehe " +
  "aussagekraeftig sind und beide Themes dieselbe Menge Text umbrechen " +
  "muessen, bevor die Hoehen verglichen werden.";

// --- PNG: written by hand, so both sites get byte-identical uploads ---

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(buffer) {
  let crc = 0xffffffff;
  for (const byte of buffer) crc = CRC_TABLE[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function pngChunk(type, data) {
  const length = Buffer.alloc(4);
  length.writeUInt32BE(data.length);
  const body = Buffer.concat([Buffer.from(type, "ascii"), data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(body));
  return Buffer.concat([length, body, crc]);
}

/** A solid-colour PNG of the given size. */
function png(width, height, [r, g, b]) {
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 2; // truecolour
  const row = Buffer.alloc(1 + width * 3);
  for (let x = 0; x < width; x++) {
    row[1 + x * 3] = r;
    row[2 + x * 3] = g;
    row[3 + x * 3] = b;
  }
  const raw = Buffer.concat(Array.from({ length: height }, () => row));
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    pngChunk("IHDR", ihdr),
    pngChunk("IDAT", zlib.deflateSync(raw)),
    pngChunk("IEND", Buffer.alloc(0)),
  ]);
}

function upload(width, height, colour, filename) {
  return {
    data: png(width, height, colour).toString("base64"),
    encoding: "base64",
    filename,
    "content-type": "image/png",
  };
}

// --- blocks ---

function text(value) {
  return [{ text: value }];
}

/* The somersault tree. Media blocks come at several block widths: `narrow`
 * and `default` clamp below any tested content column and stay comparable,
 * `layout` follows the theme's own column. */
function blocks(imageUrl, targetUrls, folderUid) {
  const value = [];
  const push = (node) => value.push({ id: `b${value.length}`, children: text(""), ...node });

  push({ type: "title", blockWidth: "default" });
  push({ type: "p", blockWidth: "narrow", children: text(PARAGRAPH) });

  // Flat Plate lists, regrouped into ul/ol by the renderer. Clara lays out
  // `ul` itself, and a todo marker is a checkbox with a fixed pixel size.
  ["disc", "decimal", "todo"].forEach((listStyleType) => {
    for (const index of [1, 2]) {
      push({
        type: "p",
        blockWidth: "narrow",
        indent: 1,
        listStyleType,
        ...(index > 1 ? { listStart: index } : {}),
        ...(listStyleType === "todo" ? { checked: index === 1 } : {}),
        children: text(`${listStyleType} ${index}`),
      });
    }
  });

  push({ type: "h2", blockWidth: "narrow", children: text("Bilder") });
  for (const [blockWidth, size, alt] of [
    ["full", "l", "Volle Breite"],
    ["default", "l", "Standardbreite"],
    ["narrow", "m", "Schmal"],
  ]) {
    push({
      type: "ploneBlock",
      "@type": "image",
      blockWidth,
      size,
      alt,
      url: imageUrl,
      image_field: "image",
    });
  }

  push({ type: "h2", blockWidth: "narrow", children: text("Videos") });
  for (const blockWidth of ["default", "layout"]) {
    push({ type: "ploneBlock", "@type": "video", blockWidth, url: VIDEO_URL });
  }

  push({ type: "h2", blockWidth: "narrow", children: text("Teaser") });
  ["narrow", "default", "layout"].forEach((blockWidth, index) => {
    push({
      type: "ploneBlock",
      "@type": "teaser",
      blockWidth,
      // explicit: plone.restapi turns a missing `overwrite` into true, and the
      // renderer then stops pulling title and description off the target
      overwrite: false,
      href: [{ "@id": targetUrls[index] }],
    });
  });

  push({ type: "h2", blockWidth: "narrow", children: text("Listings") });
  for (const [variation, blockWidth] of [
    ["summary", "default"],
    ["listing", "default"],
    ["summary", "layout"],
  ]) {
    push({
      type: "ploneBlock",
      "@type": "listing",
      blockWidth,
      variation,
      headline: `Listing ${variation} ${blockWidth}`,
      headlineTag: "h3",
      querystring: {
        query: [
          {
            i: "portal_type",
            o: "plone.app.querystring.operation.selection.any",
            v: ["News Item"],
          },
          { i: "path", o: "plone.app.querystring.operation.string.path", v: folderUid },
        ],
        sort_on: "sortable_title",
        b_size: 3,
      },
    });
  }

  push({ type: "h2", blockWidth: "narrow", children: text("Weitere Bloecke") });
  push({ type: "blockquote", blockWidth: "default", children: text(PARAGRAPH) });
  push({
    type: "code_block",
    blockWidth: "default",
    children: [{ type: "code_line", children: text("const parity = true;") }],
  });
  push({
    type: "callout",
    blockWidth: "default",
    icon: "💡",
    children: text("Ein Hinweis in einem Callout."),
  });
  push({ type: "toggle", blockWidth: "default", children: text("Aufklappbarer Titel") });
  push({ type: "toc", blockWidth: "default" });
  push({
    type: "table",
    blockWidth: "default",
    children: [
      {
        type: "tr",
        children: ["Spalte A", "Spalte B"].map((label) => ({
          type: "th",
          children: [{ type: "p", children: text(label) }],
        })),
      },
      {
        type: "tr",
        children: ["1", "2"].map((label) => ({
          type: "td",
          children: [{ type: "p", children: text(label) }],
        })),
      },
    ],
  });
  push({
    type: "column_group",
    blockWidth: "default",
    children: [0, 1].map(() => ({
      type: "column",
      width: "50%",
      children: [{ type: "p", blockWidth: "narrow", children: text(PARAGRAPH) }],
    })),
  });
  return value;
}

// --- site ---

class Site {
  constructor(base) {
    this.base = base.replace(/\/+$/, "");
  }

  async request(method, path, body) {
    const response = await fetch(`${this.base}${path}`, {
      method,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: AUTH,
      },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    if (!response.ok && ![404, 423].includes(response.status)) {
      const detail = (await response.text()).replace(/\s+/g, " ").slice(0, 300);
      throw new Error(`${method} ${this.base}${path} -> ${response.status} ${detail}`);
    }
    return response;
  }

  async json(method, path, body) {
    const response = await this.request(method, path, body);
    return response.status === 204 ? null : response.json();
  }

  // Not every type has a `publish` transition (an Image may have no
  // workflow), so ask what is on offer.
  async publish(path) {
    const workflow = await this.json("GET", `${path}/@workflow`);
    const transitions = (workflow.transitions || []).map((transition) =>
      transition["@id"].replace(/^.*\//, ""),
    );
    if (transitions.includes("publish")) {
      await this.json("POST", `${path}/@workflow/publish`);
    }
  }
}

async function removeFixture(base) {
  const site = new Site(base);
  const response = await site.request("DELETE", `/${FOLDER_ID}`);
  if (response.status === 423) {
    // an aborted @@aurora-edit session leaves a lock behind
    await site.request("DELETE", `/${FOLDER_ID}/@lock`, { force: true });
    await site.request("DELETE", `/${FOLDER_ID}`);
  }
}

/** Build the fixture on one site; resolves to the page's URL. */
async function createFixture(base) {
  const site = new Site(base);
  await removeFixture(base);

  const folder = await site.json("POST", "/", {
    "@type": "Folder",
    id: FOLDER_ID,
    title: "Clara theme parity e2e",
  });
  const image = await site.json("POST", `/${FOLDER_ID}`, {
    "@type": "Image",
    id: "parity-image",
    title: "Parity image",
    image: upload(1600, 900, [40, 90, 160], "parity.png"),
  });
  const targets = [];
  for (const [id, title, description] of TARGETS) {
    const target = await site.json("POST", `/${FOLDER_ID}`, {
      "@type": "News Item",
      id,
      title,
      description,
      image: upload(1200, 800, [160, 60, 40], `${id}.png`),
    });
    targets.push(target["@id"]);
  }
  await site.json("POST", `/${FOLDER_ID}`, {
    "@type": "Article",
    id: PAGE_ID,
    title: "Clara theme parity page",
    description: "Fixture for the cross-theme block size comparison.",
    blocks: {
      __somersault__: {
        "@type": "__somersault__",
        value: blocks(image["@id"], targets, folder.UID),
      },
    },
    blocks_layout: { items: ["__somersault__"] },
  });

  // Teaser and listing data are enriched on the way out: store what the
  // serializers produce, as the editor does when it saves.
  const enriched = await site.json("GET", PAGE_PATH);
  await site.request("PATCH", PAGE_PATH, { blocks: enriched.blocks });

  await site.publish(`/${FOLDER_ID}`);
  await site.publish(`/${FOLDER_ID}/parity-image`);
  for (const [id] of TARGETS) await site.publish(`/${FOLDER_ID}/${id}`);
  await site.publish(PAGE_PATH);

  // fail here rather than as a selector timeout in the browser
  const anonymous = await fetch(`${site.base}${PAGE_PATH}`);
  if (!anonymous.ok) {
    throw new Error(
      `published fixture is not anonymously readable: ` +
        `GET ${site.base}${PAGE_PATH} -> ${anonymous.status}`,
    );
  }
  return `${site.base}${PAGE_PATH}`;
}

module.exports = { createFixture, removeFixture };
