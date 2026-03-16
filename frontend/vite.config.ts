// import { defineConfig } from "vite"
// import vue from "@vitejs/plugin-vue"
// import { fileURLToPath, URL } from "node:url"

// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [vue()],
//   build: {
//     chunkSizeWarningLimit: 2048,
//     outDir: "web", //指定输出路径
//     minify: "terser", // 混淆器，terser构建后文件体积更小
//   },
//   resolve: {
//     alias: {
//       "@": fileURLToPath(new URL("./src", import.meta.url)),
//     },
//   },
// })

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { fileURLToPath, URL } from "node:url"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    chunkSizeWarningLimit: 2048,
    outDir: "web", // 指定输出路径
    minify: "terser", // 混淆器，terser构建后文件体积更小
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000", // ⚠️ 这里换成你 FastAPI 的地址
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "/api"),
      },
    },
  },
})
