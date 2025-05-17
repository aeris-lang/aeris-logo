import fs from "fs/promises";
import path from "path";
import Sharp from "sharp";

const outputPath = path.resolve("build");

const rendermap = JSON.parse(
  await fs.readFile(path.resolve("rendermap.json"), "utf-8")
);
Sharp.cache(false);
for (const item of rendermap) {
  const svgInputPath = path.resolve(outputPath, item.input);
  const svgOutputPath = path.resolve(outputPath, item.output);
  await Sharp(svgInputPath)
    .resize({
      width: item.width,
      height: item.height,
    })
    .png()
    .toFile(svgOutputPath);
}
