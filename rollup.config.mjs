import { nodeResolve } from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";

export default {
  input: "js_src/problem_editor/main.mjs",
  output: {
    file: "static/compiled/problem_editor.js",
    format: "iife",
    sourcemap: true,
  },
  plugins: [
    nodeResolve(),
    // terser({
    //   compress: {
    //     dead_code: false,
    //     unused: true,
    //     warnings: false,
    //   },
    // }),
  ],
};
