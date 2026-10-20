import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { Presentation, PresentationFile } from "@oai/artifact-tool";


const SKILL_DIR = process.env.SKILL_DIR;
const WORKSPACE = process.env.WORKSPACE_DIR;
const BUILD_DIR = process.env.TMP_DIR;
const FINAL_PPTX = process.env.FINAL_PPTX;
const NODE_MODULES = process.env.RUNTIME_NODE_MODULES;

if (!SKILL_DIR || !WORKSPACE || !BUILD_DIR || !FINAL_PPTX || !NODE_MODULES) {
  throw new Error("Missing absolute presentation environment paths");
}

const { finalizePresentation } = await import(
  pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href,
);

const FONT = "Arial";
const INK = "#0B1220";
const NAVY = "#10243E";
const PAPER = "#F7F9FC";
const WHITE = "#FFFFFF";
const BLUE = "#1F5A94";
const SKY = "#7DD3FC";
const TEAL = "#0F766E";
const ORANGE = "#B45309";
const RED = "#991B1B";
const MUTED = "#526071";
const LINE = "#D7DEE8";
const PANEL = "#132A42";
const DARK2 = "#111D2F";

const presentation = Presentation.create({
  slideSize: { width: 1280, height: 720 },
});


function addText(
  slide,
  text,
  {
    x, y, w, h, size = 20, bold = false, color = INK,
    align = "left", valign = "top", name = "text", lineSpacing = 1.0,
  } = {},
) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: FONT,
    fontSize: size,
    bold,
    color,
    alignment: align,
    verticalAlignment: valign,
    autoFit: "none",
    wrap: "square",
    lineSpacing,
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
  };
  return shape;
}


function addRule(slide, x, y, w, color = LINE, thickness = 1) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left: x, top: y, width: w, height: thickness },
    fill: color,
    line: { style: "solid", fill: color, width: 0 },
  });
}


function addPanel(slide, x, y, w, h, fill, line = fill, radius = "rounded-xl") {
  return slide.shapes.add({
    geometry: "roundRect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: 1.2 },
    borderRadius: radius,
  });
}


function addArrow(slide, from, to, color = MUTED, width = 2) {
  return slide.shapes.connect(from, to, {
    kind: "straight",
    fromSide: "right",
    toSide: "left",
    line: { style: "solid", fill: color, width },
    head: { type: "triangle", width: "sm", length: "sm" },
  });
}


function slideNumber(slide, number, dark = false) {
  addText(slide, String(number).padStart(2, "0"), {
    x: 1168, y: 676, w: 48, h: 22, size: 11,
    color: dark ? "#8BA6BD" : "#7A8998", align: "right", name: "slide-number",
  });
}


function notes(slide, text) {
  slide.speakerNotes.textFrame.setText(text);
}


function title(slide, text, dark = false, size = 40) {
  return addText(slide, text, {
    x: 64, y: 44, w: 1120, h: 64, size, bold: true,
    color: dark ? WHITE : NAVY, name: "title",
  });
}


function addTable(slide, values, x, y, w, h, widths, { headerFill = NAVY, font = 17 } = {}) {
  const table = slide.tables.add({
    rows: values.length,
    columns: values[0].length,
    left: x, top: y, width: w, height: h,
    columnWidths: widths,
    values,
  });
  table.styleOptions = { headerRow: false, bandedRows: false };
  table.borders.assign({ style: "solid", fill: LINE, width: 1 });
  for (let row = 0; row < values.length; row += 1) {
    for (let col = 0; col < values[row].length; col += 1) {
      const cell = table.getCell(row, col);
      cell.fill = row === 0 ? headerFill : WHITE;
      cell.text.style = {
        typeface: FONT, fontSize: font, bold: row === 0,
        color: row === 0 ? WHITE : INK,
        verticalAlignment: "middle",
        insets: { top: 7, right: 10, bottom: 7, left: 10 },
      };
    }
  }
  return table;
}


{
  const slide = presentation.slides.add();
  slide.background.fill = INK;
  for (let x = 120; x < 1280; x += 150) {
    addRule(slide, x, 0, 1, "#17324B", 720);
  }
  addText(slide, "WORK 3  /  COMPUTER ATTACKS", {
    x: 72, y: 62, w: 520, h: 24, size: 13, bold: true, color: SKY,
  });
  addText(slide, "Padding Oracle Attack", {
    x: 70, y: 184, w: 1040, h: 80, size: 64, bold: true, color: WHITE,
  });
  addText(slide, "One valid-padding bit is enough to read and rewrite encrypted state.", {
    x: 72, y: 300, w: 1000, h: 70, size: 24, color: "#D9E7F3",
  });
  addRule(slide, 72, 394, 210, TEAL, 4);
  const bytes = ["72", "6F", "6C", "65", "3D", "75", "73", "65", "72"];
  bytes.forEach((value, index) => {
    const active = index === 7;
    const cell = slide.shapes.add({
      geometry: "roundRect",
      position: { left: 72 + index * 74, top: 458, width: 58, height: 48 },
      fill: active ? "#7C2D12" : PANEL,
      line: { style: "solid", fill: active ? ORANGE : "#2B526E", width: 1.2 },
      borderRadius: "rounded-lg",
    });
    cell.text = value;
    cell.text.style = {
      typeface: FONT, fontSize: 17, bold: true,
      color: active ? "#FED7AA" : "#BFD8EC", alignment: "center", verticalAlignment: "middle",
    };
  });
  addText(slide, "CBC ciphertext block  /  16 bytes", {
    x: 72, y: 520, w: 420, h: 24, size: 13, color: "#7F9BB2",
  });
  addText(slide, "zhuhe  ·  HDU 23320116  ·  20 October 2026", {
    x: 72, y: 632, w: 600, h: 28, size: 15, color: "#AFC4D5",
  });
  addText(slide, "REPORT + PUBLIC PRESENTATION", {
    x: 860, y: 632, w: 350, h: 28, size: 12, bold: true, color: SKY, align: "right",
  });
  notes(slide, "Good morning. I chose the padding oracle attack because it turns a small error-handling difference into both plaintext disclosure and ciphertext forgery. The key never has to be recovered. The report models the exploit as a directed graph from an idle system to three loss states. I will cover the mechanism, the local demonstration, the graph, and the controls that break it.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = PAPER;
  title(slide, "Encryption without integrity");
  addText(slide, "CBC hides the plaintext. It does not prove that the ciphertext was created by the server.", {
    x: 64, y: 122, w: 1120, h: 44, size: 21, color: MUTED,
  });
  const columns = [
    { x: 64, color: TEAL, head: "CONFIDENTIALITY", body: "AES-CBC protects the bytes from being read directly." },
    { x: 472, color: ORANGE, head: "INTEGRITY", body: "No MAC or tag detects a changed predecessor block." },
    { x: 880, color: RED, head: "AUTHORITY", body: "The server decrypts and trusts the resulting role." },
  ];
  columns.forEach((column, index) => {
    addRule(slide, column.x, 230, 320, column.color, 4);
    addText(slide, column.head, {
      x: column.x, y: 252, w: 320, h: 24, size: 13, bold: true, color: column.color,
    });
    addText(slide, column.body, {
      x: column.x, y: 290, w: 300, h: 120, size: 24, bold: true, color: NAVY, lineSpacing: 1.05,
    });
    if (index < columns.length - 1) {
      slide.shapes.add({
        geometry: "rightArrow",
        position: { left: column.x + 342, top: 336, width: 44, height: 22 },
        fill: "#9AA8B6",
        line: { style: "solid", fill: "#9AA8B6", width: 0 },
      });
    }
  });
  addRule(slide, 64, 492, 1152, LINE, 1);
  addText(slide, "The cipher is not broken. The construction is.", {
    x: 64, y: 532, w: 1080, h: 68, size: 36, bold: true, color: NAVY,
  });
  slideNumber(slide, 2);
  notes(slide, "CBC supplies confidentiality, not authenticity. If the application accepts a modified ciphertext, the change flows straight into the decrypted state. The third box is the critical design mistake: the plaintext becomes authority without a separate integrity decision.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = WHITE;
  title(slide, "How CBC decryption chains");
  const bytes = await fs.readFile(path.join(WORKSPACE, "assets", "cbc-decryption.png"));
  slide.images.add({
    blob: bytes,
    contentType: "image/png",
    alt: "CBC decryption diagram with IV, ciphertext blocks, decryption and XOR",
    fit: "contain",
    position: { left: 65, top: 104, width: 1150, height: 508 },
  });
  addText(slide, "The attacker controls the previous block. The key stays secret.", {
    x: 64, y: 642, w: 1080, h: 30, size: 20, bold: true, color: NAVY,
  });
  slideNumber(slide, 3);
  notes(slide, "CBC decryption gives P-i equals D-K of C-i xor the previous ciphertext block. For the first block, the previous value is the IV. The attacker does not need D-K; changing the preceding block changes the plaintext in a predictable way.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = INK;
  title(slide, "The padding oracle", true);
  addText(slide, "A modified predecessor block produces one of two observable outcomes.", {
    x: 64, y: 116, w: 1000, h: 34, size: 20, color: "#C9D9E6",
  });
  const left = addPanel(slide, 64, 212, 330, 142, DARK2, "#294967");
  const middle = addPanel(slide, 474, 212, 300, 142, DARK2, "#294967");
  const right = addPanel(slide, 854, 212, 362, 142, DARK2, "#294967");
  addText(slide, "MODIFIED CIPHERTEXT", { x: 86, y: 234, w: 280, h: 20, size: 12, bold: true, color: SKY });
  addText(slide, "C' || C", { x: 86, y: 268, w: 280, h: 36, size: 30, bold: true, color: WHITE });
  addText(slide, "PADDING CHECK", { x: 496, y: 234, w: 250, h: 20, size: 12, bold: true, color: SKY });
  addText(slide, "valid / invalid", { x: 496, y: 268, w: 250, h: 36, size: 27, bold: true, color: WHITE });
  addText(slide, "OBSERVABLE RESULT", { x: 876, y: 234, w: 310, h: 20, size: 12, bold: true, color: SKY });
  addText(slide, "one bit", { x: 876, y: 268, w: 310, h: 36, size: 30, bold: true, color: "#FCA5A5" });
  addArrow(slide, left, middle, "#8DB2CF", 2);
  addArrow(slide, middle, right, "#8DB2CF", 2);
  addText(slide, "The channel can be a message, status code, redirect, response length, or timing.", {
    x: 64, y: 396, w: 1120, h: 32, size: 20, color: "#D9E7F3",
  });
  addText(slide, "PKCS#7:   01   ·   02 02   ·   03 03 03   ·   ...   ·   10 × 16", {
    x: 64, y: 468, w: 1120, h: 44, size: 24, bold: true, color: SKY,
  });
  addRule(slide, 64, 542, 1152, "#294967", 1);
  addText(slide, "The application reveals which branch was taken.", {
    x: 64, y: 574, w: 1000, h: 44, size: 26, bold: true, color: WHITE,
  });
  slideNumber(slide, 4, true);
  notes(slide, "PKCS-seven padding must end in a consistent pattern. The server only needs to reveal whether the pattern was valid. That can be an explicit error, a different status, a redirect, response length, or timing. The exact channel matters less than the reliable distinction.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = PAPER;
  title(slide, "Recover one byte");
  addText(slide, "MODIFIED PREDECESSOR  C'", {
    x: 64, y: 126, w: 500, h: 20, size: 12, bold: true, color: MUTED,
  });
  for (let index = 0; index < 16; index += 1) {
    const active = index === 15;
    const cell = slide.shapes.add({
      geometry: "roundRect",
      position: { left: 64 + index * 34, top: 158, width: 28, height: 44 },
      fill: active ? "#FFF1E8" : WHITE,
      line: { style: "solid", fill: active ? ORANGE : "#AFC0CF", width: 1.2 },
      borderRadius: "rounded-md",
    });
    cell.text = active ? "g" : "";
    cell.text.style = {
      typeface: FONT, fontSize: active ? 20 : 10, bold: active,
      color: active ? ORANGE : MUTED, alignment: "center", verticalAlignment: "middle",
    };
  }
  addText(slide, "UNCHANGED TARGET  C_i", {
    x: 64, y: 238, w: 500, h: 20, size: 12, bold: true, color: MUTED,
  });
  for (let index = 0; index < 16; index += 1) {
    slide.shapes.add({
      geometry: "roundRect",
      position: { left: 64 + index * 34, top: 270, width: 28, height: 44 },
      fill: "#EAF1F7",
      line: { style: "solid", fill: BLUE, width: 1 },
      borderRadius: "rounded-md",
    });
  }
  addPanel(slide, 64, 360, 510, 82, "#EAF1F7", "#AFC0CF");
  addText(slide, "The last plaintext byte must become 01.", {
    x: 86, y: 382, w: 460, h: 36, size: 22, bold: true, color: NAVY,
  });
  addRule(slide, 640, 128, 1, LINE, 440);
  addText(slide, "01", { x: 680, y: 132, w: 60, h: 24, size: 13, bold: true, color: ORANGE });
  addText(slide, "I[15] = g xor 0x01", { x: 680, y: 166, w: 500, h: 36, size: 28, bold: true, color: NAVY });
  addText(slide, "02 02", { x: 680, y: 234, w: 90, h: 24, size: 13, bold: true, color: ORANGE });
  addText(slide, "I[14] = g xor 0x02", { x: 680, y: 268, w: 500, h: 36, size: 28, bold: true, color: NAVY });
  addText(slide, "03 03 03", { x: 680, y: 336, w: 110, h: 24, size: 13, bold: true, color: ORANGE });
  addText(slide, "I[13] = g xor 0x03", { x: 680, y: 370, w: 500, h: 36, size: 28, bold: true, color: NAVY });
  addText(slide, "Repeat for all 16 positions.", { x: 680, y: 438, w: 500, h: 30, size: 19, color: MUTED });
  addRule(slide, 64, 482, 1152, LINE, 1);
  addText(slide, "P[i] = I[i] xor C[i-1]", { x: 64, y: 512, w: 820, h: 52, size: 36, bold: true, color: TEAL });
  addText(slide, "≤ 256 guesses / byte", { x: 896, y: 518, w: 300, h: 36, size: 24, bold: true, color: ORANGE, align: "right" });
  addText(slide, "4,713 requests recovered two blocks in the lab.", {
    x: 64, y: 590, w: 1000, h: 30, size: 18, color: MUTED,
  });
  slideNumber(slide, 5);
  notes(slide, "For each position, try candidate bytes until the block ends in the desired padding. The successful guess reveals the intermediate byte, not the key. Set the next target to two bytes of 02, then three bytes of 03, and repeat. The demonstration used 4,713 requests for two blocks, consistent with the expected random search cost.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = WHITE;
  title(slide, "Forge the first block");
  addText(slide, "ORIGINAL", { x: 64, y: 136, w: 150, h: 22, size: 12, bold: true, color: MUTED });
  addText(slide, "role=user;uid=10", { x: 64, y: 168, w: 660, h: 48, size: 30, bold: true, color: NAVY });
  addText(slide, "TARGET", { x: 64, y: 250, w: 150, h: 22, size: 12, bold: true, color: ORANGE });
  addText(slide, "role=root;uid=10", { x: 64, y: 282, w: 660, h: 48, size: 30, bold: true, color: ORANGE });
  addRule(slide, 64, 368, 640, LINE, 1);
  addText(slide, "IV* = I[0] xor P*[0]", { x: 64, y: 404, w: 720, h: 56, size: 36, bold: true, color: TEAL });
  addText(slide, "Keep every ciphertext block unchanged.", { x: 64, y: 476, w: 640, h: 30, size: 19, color: MUTED });
  addPanel(slide, 794, 150, 420, 330, "#FEF2F2", "#F0B4B4");
  addText(slide, "HTTP 200", { x: 826, y: 180, w: 350, h: 34, size: 22, bold: true, color: RED });
  addText(slide, "role=root", { x: 826, y: 236, w: 350, h: 46, size: 34, bold: true, color: INK });
  addText(slide, "admin console", { x: 826, y: 302, w: 350, h: 40, size: 28, bold: true, color: NAVY });
  addText(slide, "The application authorizes the altered state.", { x: 826, y: 382, w: 350, h: 60, size: 17, color: MUTED });
  addText(slide, "Changing an inner block also corrupts its predecessor - a real attack constraint.", {
    x: 64, y: 574, w: 1120, h: 30, size: 18, color: MUTED,
  });
  slideNumber(slide, 6);
  notes(slide, "Once the intermediate value is known, a new predecessor produces chosen plaintext. The demonstration targets the first block through the IV, so later plaintext remains intact. Changing an inner block would also corrupt the previous plaintext block, a constraint a real exploit has to handle.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = WHITE;
  title(slide, "Attack graph", false, 34);
  addText(slide, "S0  →  K1 / K2 / K3", {
    x: 900, y: 50, w: 316, h: 24, size: 13, bold: true, color: MUTED, align: "right",
  });
  const bytes = await fs.readFile(path.join(WORKSPACE, "assets", "attack-digraph.png"));
  slide.images.add({
    blob: bytes,
    contentType: "image/png",
    alt: "Directed graph of the padding oracle attack from idle state to theft, privilege change and denial states",
    fit: "contain",
    position: { left: 120, top: 102, width: 1040, height: 594 },
  });
  slideNumber(slide, 7);
  notes(slide, "This is the main model. S0 is the idle system. The attacker captures a cookie, detects the oracle, and enters the probing loop at S3. A successful response reveals one byte; sixteen bytes recover a block. The upper path assembles plaintext and reaches K1. The lower path builds a forged predecessor, gets it accepted, and reaches K2. K3 is conditional: high-volume probing can trigger lockout or resource pressure, but the graph does not claim that every attack reaches denial of service.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = INK;
  title(slide, "Observed result", true);
  addText(slide, "Synthetic localhost session  /  no real user data", {
    x: 64, y: 116, w: 900, h: 28, size: 17, color: "#AFC4D5",
  });
  const rows = [
    { y: 190, label: "RECOVERED", value: "role=user;uid=1001;ok=1", color: WHITE },
    { y: 304, label: "FORGED BLOCK", value: "role=root;uid=10", color: "#FDBA74" },
    { y: 418, label: "RESPONSE", value: "HTTP 200  ·  role=root  ·  admin console", color: "#86EFAC" },
  ];
  rows.forEach((row) => {
    addText(slide, row.label, {
      x: 64, y: row.y, w: 210, h: 24, size: 12, bold: true, color: SKY,
    });
    addText(slide, row.value, {
      x: 288, y: row.y - 8, w: 620, h: 44, size: 24, bold: true, color: row.color,
    });
    addRule(slide, 64, row.y + 66, 820, "#294967", 1);
  });
  for (let index = 0; index < 3; index += 1) {
    const item = [
      ["2", "CBC blocks recovered"],
      ["4,713", "oracle queries"],
      ["0", "key bytes"],
    ][index];
    addText(slide, item[0], {
      x: 960, y: 190 + index * 132, w: 240, h: 58, size: 42, bold: true,
      color: index === 2 ? "#86EFAC" : WHITE, align: "right",
    });
    addText(slide, item[1], {
      x: 960, y: 246 + index * 132, w: 240, h: 24, size: 13, bold: true,
      color: "#8BA6BD", align: "right",
    });
  }
  addText(slide, "The forgery changes state without decrypting or re-encrypting the remaining blocks.", {
    x: 64, y: 606, w: 1050, h: 30, size: 18, color: "#D9E7F3",
  });
  slideNumber(slide, 8, true);
  notes(slide, "The run recovered the complete synthetic session and then changed only the first block. Before the forgery the response was a user dashboard. After the new IV, the same service returned role equals root and the admin console. Zero key bytes were recovered; the attack abuses predictions and validity, not key recovery.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = PAPER;
  title(slide, "Root cause");
  addText(slide, "The failure is a chain of three missing controls.", {
    x: 64, y: 122, w: 1000, h: 34, size: 20, color: MUTED,
  });
  const stages = [
    { x: 64, color: BLUE, number: "01", head: "Ciphertext is modifiable", body: "The client controls the IV and encrypted state." },
    { x: 472, color: ORANGE, number: "02", head: "Padding is observable", body: "The server separates invalid padding from other failures." },
    { x: 880, color: RED, number: "03", head: "Plaintext becomes authority", body: "The role is parsed and accepted without integrity verification." },
  ];
  stages.forEach((stage, index) => {
    addRule(slide, stage.x, 218, 270, stage.color, 4);
    addText(slide, stage.number, {
      x: stage.x, y: 238, w: 60, h: 30, size: 13, bold: true, color: stage.color,
    });
    addText(slide, stage.head, {
      x: stage.x, y: 278, w: 300, h: 70, size: 24, bold: true, color: NAVY,
    });
    addText(slide, stage.body, {
      x: stage.x, y: 364, w: 300, h: 100, size: 18, color: MUTED,
    });
    if (index < stages.length - 1) {
      slide.shapes.add({
        geometry: "rightArrow",
        position: { left: stage.x + 342, top: 336, width: 44, height: 22 },
        fill: "#9AA8B6",
        line: { style: "solid", fill: "#9AA8B6", width: 0 },
      });
    }
  });
  addPanel(slide, 64, 504, 1120, 70, "#FEF2F2", "#F0B4B4");
  addText(slide, "CWE-353  ·  Missing Support for Integrity Check", {
    x: 92, y: 526, w: 900, h: 26, size: 18, bold: true, color: RED,
  });
  addText(slide, "AES is not the failing component.", {
    x: 64, y: 604, w: 900, h: 38, size: 28, bold: true, color: NAVY,
  });
  slideNumber(slide, 9);
  notes(slide, "The root cause is not a weak block cipher. The client can modify ciphertext, the application exposes padding validity, and the decrypted role is treated as authority. CWE-353 captures the missing integrity check. The parser is on the attack surface because only one valid-padding bit is needed.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = WHITE;
  title(slide, "Three terminal losses");
  const table = addTable(
    slide,
    [
      ["STATE", "LOSS", "EVIDENCE"],
      ["K1", "Information theft", "The complete plaintext is recovered without the key."],
      ["K2", "Modification or unauthorized access", "The role is forged from user to root and accepted."],
      ["K3", "Denial of service or access", "Conditional: probing may trigger lockout or resource pressure."],
    ],
    64, 168, 1152, 330, [125, 355, 672], { font: 18 },
  );
  for (let row = 1; row <= 3; row += 1) {
    const cell = table.getCell(row, 0);
    cell.fill = "#FEF2F2";
    cell.text.style = {
      typeface: FONT, fontSize: 26, bold: true, color: RED,
      verticalAlignment: "middle", insets: { top: 8, right: 10, bottom: 8, left: 14 },
    };
  }
  addText(slide, "K1 and K2 are demonstrated. K3 remains in the graph because the query loop can change availability, not because every target will experience it.", {
    x: 64, y: 544, w: 1120, h: 60, size: 18, color: MUTED,
  });
  slideNumber(slide, 10);
  notes(slide, "The graph has three terminal loss classes. K1 is information theft. K2 is modification and unauthorized access, demonstrated by the role change. K3 is conditional availability loss. Keeping the difference explicit makes the model defensible and prevents overclaiming.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = PAPER;
  title(slide, "Countermeasures");
  addText(slide, "Break the oracle edge, then remove the trust decision.", {
    x: 64, y: 120, w: 1000, h: 34, size: 20, color: MUTED,
  });
  addTable(
    slide,
    [
      ["LAYER", "CONTROL", "EFFECT"],
      ["Primary", "AES-GCM or ChaCha20-Poly1305; verify the tag before parsing.", "Modification becomes a hard authentication failure."],
      ["Compatibility", "If CBC must stay: Encrypt-then-MAC with constant-time comparison.", "Forged predecessors are rejected before the padding check."],
      ["Behavior", "One generic failure path; avoid secret-dependent branches and timing.", "The valid-padding distinction is no longer observable."],
      ["Operations", "Rate limits, alerting, key rotation, and tamper regression tests.", "Probing is contained and old captured tokens are invalidated."],
    ],
    64, 176, 1152, 344, [150, 545, 457], { font: 17 },
  );
  addPanel(slide, 64, 552, 1152, 66, NAVY, NAVY);
  addText(slide, "verify_tag  →  decrypt  →  validate  →  parse", {
    x: 94, y: 571, w: 1000, h: 28, size: 24, bold: true, color: SKY,
  });
  slideNumber(slide, 11);
  notes(slide, "The primary fix is authenticated encryption with the tag checked before any parsing. If CBC must remain, use Encrypt-then-MAC and compare in constant time. Uniform failures shrink the side channel, while rate limits and key rotation reduce the practical value of probing and previously captured cookies.");
}


{
  const slide = presentation.slides.add();
  slide.background.fill = INK;
  title(slide, "Authenticate before parsing", true, 48);
  addText(slide, "Three rules close the demonstrated path.", {
    x: 64, y: 128, w: 850, h: 34, size: 21, color: "#C9D9E6",
  });
  const principles = [
    ["01", "Verify authenticity before decrypting."],
    ["02", "Never expose a padding-validity distinction."],
    ["03", "Treat decrypted state as untrusted until revalidated."],
  ];
  principles.forEach((principle, index) => {
    addText(slide, principle[0], {
      x: 64, y: 218 + index * 92, w: 60, h: 26, size: 13, bold: true, color: SKY,
    });
    addText(slide, principle[1], {
      x: 142, y: 206 + index * 92, w: 700, h: 44, size: 25, bold: true, color: WHITE,
    });
  });
  addRule(slide, 900, 206, 1, "#294967", 290);
  addText(slide, "The attack did not break AES.", {
    x: 938, y: 236, w: 280, h: 72, size: 27, bold: true, color: "#FDBA74",
  });
  addText(slide, "It broke the system's decision to trust unauthenticated state.", {
    x: 938, y: 330, w: 280, h: 120, size: 20, color: "#D9E7F3",
  });
  addText(slide, "Sources: Vaudenay 2002 · NVD CVE-2010-3332 · NVD CVE-2014-3566 · OWASP Cryptographic Storage Cheat Sheet", {
    x: 64, y: 632, w: 1080, h: 22, size: 10, color: "#7F9BB2",
  });
  slideNumber(slide, 12, true);
  notes(slide, "To close, the attack did not break AES. It broke the system's trust decision. Verify authenticity first, never expose padding validity, and treat decrypted state as untrusted. The graph turns those principles into testable controls: remove the oracle edge, and reject the forged state before it becomes authority.");
}


await fs.mkdir(BUILD_DIR, { recursive: true });
await fs.mkdir(path.dirname(FINAL_PPTX), { recursive: true });
const previewDir = path.join(BUILD_DIR, "previews");
await fs.mkdir(previewDir, { recursive: true });
for (let index = 0; index < presentation.slides.count; index += 1) {
  const slide = presentation.slides.getItem(index);
  const preview = await presentation.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(
    path.join(previewDir, `slide-${String(index + 1).padStart(2, "0")}.png`),
    new Uint8Array(await preview.arrayBuffer()),
  );
}

const candidatePath = path.join(BUILD_DIR, "candidate.pptx");
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
const expectedSlideSizeEmu = "12192000,6858000";
const result = await finalizePresentation({
  explicitTotalSlideCount: 12,
  requiredNativeTableOwnerSlides: [10, 11],
  requiredNativeChartOwnerSlides: [],
  workspaceDir: WORKSPACE,
  candidatePath,
  finalPath: FINAL_PPTX,
  pythonExecutable: process.env.RUNTIME_PYTHON,
  integrityValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: [
    "--expected-slide-size-emu", expectedSlideSizeEmu,
    "--validate-bullet-geometry",
    "--validate-heading-fit",
    "--require-native-table-slide", "10",
    "--require-native-table-slide", "11",
  ],
  fontPolicy: { basis: "design", families: [FONT] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(BUILD_DIR, "presentation.validation.json"),
});
console.log(JSON.stringify(result, null, 2));
console.log(`Wrote ${FINAL_PPTX}`);
