import { defineStore } from "pinia"

export const useThemeStore = defineStore("theme", {
  state: () => ({
    darkMode: true,
  }),
  actions: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
    },
  },
})
