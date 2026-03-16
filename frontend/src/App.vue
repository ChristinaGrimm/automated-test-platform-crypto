<template>
  <n-config-provider :theme="themeStore.darkMode ? darkTheme : undefined">
    <n-dialog-provider>
      <n-notification-provider>
        <n-message-provider>
          <router-view></router-view>
        </n-message-provider>
      </n-notification-provider>
    </n-dialog-provider>
  </n-config-provider>
</template>
<script setup lang="ts">
import {
  NNotificationProvider,
  NConfigProvider,
  NMessageProvider,
  NDialogProvider,
  darkTheme,
} from "naive-ui"
import { useThemeStore } from "@/stores/theme-store"

const themeStore = useThemeStore()
</script>
<style scoped>
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial,
    "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol",
    "Noto Color Emoji";
}
</style>
