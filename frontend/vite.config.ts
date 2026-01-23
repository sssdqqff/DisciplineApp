import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/tasks": "http://localhost:8000",
      "/categories": "http://localhost:8000"
    }
  }
});
