import { createRouter, createWebHistory } from "vue-router";
import Index from "@/components/Index.vue";
import MohwRSS from "@/components/MohwRSS.vue";
import Labs from "@/components/Labs.vue";
import Covid19CountryStats from "@/components/Covid19CountryStats.vue";
import AgstableWeeklyCov19 from "@/components/AgstableDailyCov19.vue";

const routes = [
  { path: "/", name: "Index", component: Index, props: true, },
  { path: "/mohwRSS", name: "mohwRSS", component: MohwRSS, props: true, },
  { path: "/labs", name: "Labs", component: Labs, props: true, },
  { path: "/covid19CountryStats", name: "Covid19CountryStats", component: Covid19CountryStats, props: true, },
  { path: "/agstableDailyCov19", name: "AgstableDailyCov19", component: AgstableWeeklyCov19, props: true, },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
