<template>
  <input id="covid19_data" type="hidden" value="">
  <Index message="COVID-19 台灣消息" title="這是台灣COVID-19 訊息" filter="送出" home="首頁" v-bind:covid19Data="covid19Data"/>
</template>

<script>
import Index from './components/Index.vue'
import covid19Data from './assets/covid19_data.json'

export default {
  name: 'App',
  components: {
    Index
  },
  data() {
    return {
      'covid19Data': covid19Data,
    };
  },
  mounted() {
    this.covid19Data = covid19Data;
  },
}
</script>
