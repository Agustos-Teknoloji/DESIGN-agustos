#!/usr/bin/env node
/** Generate the v3 editable PowerPoint / Google Slides import template.
 *
 * Uses the public pptxgenjs package so a clean checkout can reproduce the
 * checked-in templates. All text, rules, and fields remain native objects.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import PptxGenJS from "pptxgenjs";

const BRAND_DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(BRAND_DIR);
const SLIDE = { width: 13.333, height: 7.5 };

function args(argv) {
  const result = {};
  for (let index = 0; index < argv.length; index += 2) {
    result[argv[index].replace(/^--/, "")] = argv[index + 1];
  }
  if (!result.brand || !result.output) {
    throw new Error("usage: node brand/build_presentation.mjs --brand <slug> --output <file>");
  }
  return result;
}

function inches(value) {
  return Number.parseFloat(String(value).replace("in", ""));
}

function pt(value) {
  return Number.parseFloat(String(value).replace("pt", ""));
}

function hex(value) {
  return value.replace(/^#/, "").toUpperCase();
}

function addText(slide, name, text, options) {
  slide.addText(text, {
    objectName: name,
    margin: 0,
    breakLine: false,
    valign: "mid",
    ...options,
  });
}

function addRule(slide, name, x, y, w, color, h = 0.012) {
  slide.addShape("rect", {
    objectName: name, x, y, w, h,
    fill: { color: hex(color) },
    line: { color: hex(color), transparency: 100 },
  });
}

function addLabel(slide, text, x, y, w, tokens, signal) {
  addText(slide, `${text.toLowerCase().replaceAll(" ", "-")}-label`, text, {
    x, y, w, h: 0.3,
    fontFace: tokens.foundations.fontFamily.display,
    fontSize: pt(tokens.recipes.presentation.captionSize),
    color: hex(signal),
    bold: true,
    charSpacing: 1.4,
  });
}

async function addLogo(slide, filename, x, y, w, maxHeight = 0.75) {
  const bytes = await fs.readFile(filename);
  const widthPx = bytes.readUInt32BE(16);
  const heightPx = bytes.readUInt32BE(20);
  const h = Math.min(maxHeight, w * (heightPx / widthPx));
  const fittedWidth = h * (widthPx / heightPx);
  slide.addImage({ path: filename, objectName: "brand-lockup", altText: "Brand lockup", x, y, w: fittedWidth, h });
}

async function build() {
  const options = args(process.argv.slice(2));
  const tokens = JSON.parse(await fs.readFile(path.join(ROOT, "tokens", "resolved.json"), "utf8"));
  const brand = tokens.brands[options.brand];
  if (!brand) throw new Error(`unknown brand: ${options.brand}`);

  const recipe = tokens.recipes.presentation;
  const colors = tokens.foundations.color;
  const fonts = tokens.foundations.fontFamily;
  const signal = tokens.semantic.color.signal;
  const margin = inches(recipe.margin);
  const contentWidth = SLIDE.width - (2 * margin);
  const logoDir = path.join(BRAND_DIR, "exports", options.brand, "lockup");
  const positive = path.join(logoDir, `${options.brand}-lockup__positive.png`);
  const negative = path.join(logoDir, `${options.brand}-lockup__negative.png`);

  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: "AGUSTOS_WIDE", width: SLIDE.width, height: SLIDE.height });
  pptx.layout = "AGUSTOS_WIDE";
  pptx.author = "Ağustos Design System";
  pptx.subject = `${brand.title} editable presentation template`;
  pptx.title = `${brand.title} Template`;
  pptx.company = brand.title;
  pptx.lang = "tr-TR";
  pptx.theme = {
    headFontFace: fonts.display,
    bodyFontFace: fonts.body,
    lang: "tr-TR",
  };

  // 1 — Title: a generous editorial opening.
  {
    const slide = pptx.addSlide();
    slide.background = { color: hex(colors.paperCream) };
    await addLogo(slide, positive, margin, 0.68, 3.15);
    addLabel(slide, "PRESENTATION", margin, 2.48, 2.7, tokens, signal);
    addText(slide, "presentation-title", "Presentation title", { x: margin, y: 2.92, w: contentWidth, h: 1.1, fontFace: fonts.display, fontSize: pt(recipe.titleSize), color: hex(colors.ink), bold: true });
    addText(slide, "presentation-subtitle", "A concise subtitle, author, or date", { x: margin, y: 4.28, w: 7.8, h: 0.5, fontFace: fonts.body, fontSize: pt(recipe.bodySize), color: hex(colors.inkSoft) });
    addRule(slide, "title-signal-rule", margin, 6.08, contentWidth, colors.ruleCream);
    addText(slide, "title-domain", brand.domain, { x: margin, y: 6.25, w: 3.5, h: 0.3, fontFace: fonts.body, fontSize: pt(recipe.captionSize), color: hex(colors.inkFaint) });
  }

  // 2 — Section: identity ink becomes a field only for a decisive divider.
  {
    const slide = pptx.addSlide();
    slide.background = { color: hex(brand.color) };
    await addLogo(slide, negative, margin, 0.68, 3.0);
    addText(slide, "section-number", "01", { x: margin, y: 2.55, w: 1.0, h: 0.4, fontFace: fonts.display, fontSize: pt(recipe.captionSize), color: hex(colors.paperCream), bold: true });
    addText(slide, "section-title", "Section title", { x: margin, y: 3.02, w: contentWidth, h: 1.0, fontFace: fonts.display, fontSize: pt(recipe.sectionTitleSize), color: hex(colors.paperCream), bold: true });
    addRule(slide, "section-rule", margin, 6.08, contentWidth, colors.paperCream);
  }

  // 3 — Content: flat hierarchy, shared red signal.
  {
    const slide = pptx.addSlide();
    slide.background = { color: hex(colors.paperCream) };
    addLabel(slide, "SECTION", margin, 0.62, 2.2, tokens, signal);
    addText(slide, "content-title", "Content slide", { x: margin, y: 1.02, w: contentWidth, h: 0.72, fontFace: fonts.display, fontSize: pt(recipe.slideTitleSize), color: hex(colors.ink), bold: true });
    addRule(slide, "content-rule", margin, 1.92, contentWidth, colors.ruleCream);
    addText(slide, "content-lead", "Lead with one clear point.", { x: margin, y: 2.35, w: 4.75, h: 1.15, fontFace: fonts.display, fontSize: 32, color: hex(colors.ink), bold: true });
    addText(slide, "content-body", "Support it with concise evidence. Keep the composition aligned to the shared frame and reserve red for links, markers, and small signals.", { x: margin + 5.6, y: 2.35, w: contentWidth - 5.6, h: 1.35, fontFace: fonts.body, fontSize: pt(recipe.bodySize), color: hex(colors.inkSoft) });
    ["01  First supporting point", "02  Second supporting point", "03  Third supporting point"].forEach((text, index) => {
      addText(slide, `content-point-${index + 1}`, text, { x: margin + 5.6, y: 4.1 + (index * 0.6), w: 5.0, h: 0.35, fontFace: fonts.body, fontSize: pt(recipe.bodySize), color: hex(colors.ink), bold: true });
    });
  }

  // 4 — Data: native text and rules keep the table editable.
  {
    const slide = pptx.addSlide();
    slide.background = { color: hex(colors.paperWhite) };
    addLabel(slide, "DATA", margin, 0.62, 2.2, tokens, signal);
    addText(slide, "data-title", "Structured information", { x: margin, y: 1.02, w: contentWidth, h: 0.72, fontFace: fonts.display, fontSize: pt(recipe.slideTitleSize), color: hex(colors.ink), bold: true });
    const columns = [margin, margin + 4.45, margin + 8.05];
    const widths = [4.1, 3.25, 3.45];
    ["Measure", "Current", "Direction"].forEach((text, index) => addText(slide, `data-header-${index}`, text, { x: columns[index], y: 2.12, w: widths[index], h: 0.32, fontFace: fonts.display, fontSize: pt(recipe.captionSize), color: hex(signal), bold: true }));
    const rows = [
      ["Shared content frame", "920 px", "Hold"],
      ["Micro interaction", "120 ms", "Keep short"],
      ["Shared red", "Signal", "Use selectively"],
    ];
    rows.forEach((row, rowIndex) => {
      const y = 2.7 + (rowIndex * 0.88);
      addRule(slide, `data-rule-${rowIndex}`, margin, y - 0.18, contentWidth, colors.ruleWhite);
      row.forEach((text, colIndex) => addText(slide, `data-${rowIndex}-${colIndex}`, text, { x: columns[colIndex], y, w: widths[colIndex], h: 0.4, fontFace: colIndex === 1 ? fonts.mono : fonts.body, fontSize: pt(recipe.bodySize), color: hex(colors.ink), bold: colIndex === 0 }));
    });
    addRule(slide, "data-final-rule", margin, 5.18, contentWidth, colors.ruleWhite);
    addText(slide, "data-caption", "Source or explanatory note", { x: margin, y: 5.48, w: contentWidth, h: 0.3, fontFace: fonts.body, fontSize: pt(recipe.captionSize), color: hex(colors.inkFaint) });
  }

  // 5 — Closing: identity and destination, nothing more.
  {
    const slide = pptx.addSlide();
    slide.background = { color: hex(colors.paperCream) };
    await addLogo(slide, positive, margin, 2.62, 3.2);
    addText(slide, "closing-domain", brand.domain, { x: margin, y: 3.84, w: 4.2, h: 0.4, fontFace: fonts.display, fontSize: pt(recipe.bodySize), color: hex(signal), bold: true });
    addRule(slide, "closing-rule", margin, 6.08, contentWidth, colors.ruleCream);
  }

  await fs.mkdir(path.dirname(options.output), { recursive: true });
  await pptx.writeFile({ fileName: options.output });
}

build().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
