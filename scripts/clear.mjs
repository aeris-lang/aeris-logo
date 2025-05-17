import fs from "fs/promises";

await fs.rm("build", { recursive: true, force: true });
