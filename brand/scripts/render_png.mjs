// Batch SVG -> transparent PNG renderer for the Ağustos brand kit.
// Used by build.py: reads a JSON array of jobs from the file path in argv[2].
// Each job: { "svg": "<path>", "out": "<path>", "width": <px> }
// resvg ships a prebuilt binary — no system Cairo/Inkscape dependency.
import { Resvg } from "@resvg/resvg-js";
import fs from "node:fs";

const jobsPath = process.argv[2];
if (!jobsPath) {
  console.error("usage: node render_png.mjs <jobs.json>");
  process.exit(1);
}

const jobs = JSON.parse(fs.readFileSync(jobsPath, "utf8"));
let ok = 0;
for (const job of jobs) {
  const svg = fs.readFileSync(job.svg, "utf8");
  const resvg = new Resvg(svg, {
    fitTo: { mode: "width", value: job.width },
    background: "rgba(0,0,0,0)", // transparent; SVG paints its own tile when needed
  });
  fs.writeFileSync(job.out, resvg.render().asPng());
  ok++;
}
console.log(`rendered ${ok} png(s)`);
