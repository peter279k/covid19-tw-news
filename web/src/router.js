import { createRouter, createWebHistory } from "vue-router";
import Index from "@/components/Index.vue";
import MohwRSS from "@/components/MohwRSS.vue";
import Labs from "@/components/Labs.vue";

const routes = [
  { path: "/", name: "Index", component: Index, props: true, },
  { path: "/mohwRSS", name: "mohwRSS", component: MohwRSS, props: true, },
  { path: "/labs", name: "Labs", component: Labs, props: true, },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
