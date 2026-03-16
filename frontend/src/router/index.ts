import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
// import HomeView from '../views/home/Index.vue';
import { storageData } from "@/utils/stored-data";

const baseRoutes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    meta: { auth: true },
    component: () => import("../views/home/index.vue"),
    redirect: "/welcome",
    children: [
      {
        path: "/welcome",
        name: "Welcome",
        meta: { auth: true },
        component: () => import("../views/welcome/index.vue"),
      },
      {
        path: "main",
        name: "Main",
        meta: { auth: true },
        component: () => import("../views/main/index.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/login/index.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: baseRoutes,
});

router.beforeEach((to, _from, next) => {
  //是否需要登录
  if (to.meta.auth && !storageData.get("access_token")) {
    router.push({ name: "Login" });
    next();
  } else {
    next();
  }
});

export default router;
