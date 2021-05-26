import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
require('@/css/sticky-footer.css');

createApp(App).use(router).mount('body')
