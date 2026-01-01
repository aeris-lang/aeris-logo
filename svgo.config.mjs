/** @type {import("svgo").Config} */
export default {
  multipass: true,
  plugins: ["cleanupAttrs", "convertShapeToPath"],
};
