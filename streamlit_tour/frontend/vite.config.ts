import { defineConfig } from "vite";
import { resolve } from "path";
import cssInjectedByJs from "vite-plugin-css-injected-by-js";

export default defineConfig({
  // ─── Build as a library, not a web app ──────────────────────────────────────
  // Vite has two modes: "app" (produces index.html + chunks) and "lib"
  // (produces a single JS module). Streamlit v2 expects a lib-mode build.
  plugins: [
    cssInjectedByJs(),
  ],
  build: {
    lib: {
      // Your component's entry point
      entry: resolve(__dirname, "src/index.ts"),

      // Output as an ES module (.js), NOT CommonJS (.cjs)
      // Streamlit v2 loads your file as a native ES module in the browser
      formats: ["es"],

      // The output filename — Vite will append a content hash automatically,
      // producing e.g. "index-a1b2c3d4.js"
      // This is why __init__.py uses the glob "index-*.js"
      fileName: () => "index.js",
    },

    // Where the compiled assets land — must match `asset_dir` in the
    // inner pyproject.toml (streamlit_tour/pyproject.toml)
    outDir: "build",

    // Wipe the build/ folder before each build to avoid stale hashed files
    emptyOutDir: true,

    rollupOptions: {
      // driver.js CSS is imported in index.ts ("import 'driver.js/dist/driver.css'")
      // Vite will inline it into the JS bundle as a <style> injection —
      // no separate .css file needed. This is the correct behavior for
      // Streamlit components since there is no index.html to link a stylesheet.
      output: {
        // Ensure the hashed filename is applied correctly
        entryFileNames: "index-[hash].js",

        // Inline all CSS into the JS bundle (no separate .css output file)
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith(".css")) {
            // Absorbed into the JS bundle, this path is never written to disk
            return "assets/[name]-[hash][extname]";
          }
          return "assets/[name]-[hash][extname]";
        },
      },
    },

    // Minify for production. Use false during debugging if you need readable output.
    minify: true,

    // Generate sourcemaps so browser devtools can show you original TS line numbers
    sourcemap: true,
  },

  // ─── Dev mode (npm run dev = vite build --watch) ────────────────────────────
  // There is no dev server here (unlike a React app).
  // Streamlit itself serves the files from build/ — Vite just watches and rebuilds.
});