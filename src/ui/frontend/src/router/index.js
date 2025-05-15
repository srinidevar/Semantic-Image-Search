import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: () => import("../views/IndexInventory.vue"),
    },
    {
      path: "/team",
      component: () => import("../views/SearchImages.vue"),
    },
    {
      path: "/about",
      component: () => import("../views/About.vue"),
    },
    {
      path: "/licenses",
      component: () => import("../views/License.vue"),
    },
  ],
});

export default router;
