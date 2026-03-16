import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./stores";
const app = createApp(App);
app.directive("title", {
  mounted(el) {
    document.title = el.dataset.title;
  },
});
app.use(router);
app.use(store);

app.mount("#app");
