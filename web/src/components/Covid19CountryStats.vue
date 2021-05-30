<template>
  <!-- Begin page content -->
  <main id="main-block" class="flex-shrink-0">
  <div class="container">
    <h1 class="mt-5">{{ title }}</h1>
    <form>
      <div class="mb-3">
          <VueMultiselect
            v-model="filter"
            :options="countries"
            :multiple="true"
            :close-on-select="true"
            placeholder="請選擇國家">
          </VueMultiselect>
      </div>
    </form>
    <div class="row">
        <div class="col">
          <a class="btn btn-primary" v-on:click="collapseButton($event)" data-bs-toggle="collapse" href="#collapseLabTable" role="button" aria-expanded="false" aria-controls="collapseExample">
            {{ labTableButton }}
          </a>
        </div>
    </div>
    <div class="row">
      <div class="collapse" id="collapseLabTable">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">國家名稱</th>
              <th scope="col">國家名稱(英文)</th>
              <th scope="col">確診總人數</th>
              <th scope="col">死亡總人數</th>
            </tr>
          </thead>
          <tbody id="covid19-data-rows">
            <tr v-for="data in filteredTable" :key="data">
              <template v-if="data[0].indexOf('country_ch') === -1">
                <td>{{ data[0] }}</td>
                <td>{{ data[1] }}</td>
                <td>{{ data[2] }}</td>
                <td>{{ data[3] }}</td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="row">
      <vue3-chart-js
        v-bind="{ ...barChart }"
        :id="barChart.id"
        ref="chartRef"
        :type="barChart.type"
        :data="barChart.data"
        :options="barChart.options"
      />
    </div>
  </div>
  </main>
</template>

<script>
import { ref } from 'vue';
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs'
import globalCasesDeaths from '../assets/covid19_global_cases_and_deaths.json'
import VueMultiselect from 'vue-multiselect'

var numeral = require('numeral');

function findCountriesByKeyword(globalCasesDeaths, filteredKeyword) {
  let index = 1;
  let countryName = '';
  let countryEnName = '';
  let results = {};
  for (index in globalCasesDeaths) {
    if (globalCasesDeaths[index][0] === 'country_ch') {
      continue;
    }
    countryName = globalCasesDeaths[String(index)][0];
    countryEnName = globalCasesDeaths[String(index)][1];
    if (filteredKeyword.indexOf(countryName) !== -1) {
      results[String(index)] = globalCasesDeaths[String(index)];
    }
    if (filteredKeyword.indexOf(countryEnName) !== -1) {
      results[String(index)] = globalCasesDeaths[String(index)];
    }
  }

  return results;
}

function getDatasets(globalCasesDeaths) {
  let countries = getCountries(globalCasesDeaths)['countries_ch'];
  let labels = new Array(countries.length);
  let secondLabels = new Array(countries.length);
  let cases = 0;
  let deaths = 0;
  labels.fill('#1abc9c');
  secondLabels.fill('#e67e22');
  let datasets = [
    {
      label: ['確診總人數'],
      backgroundColor: labels,
      data: [],
    },
    {
      label: ['死亡總人數'],
      backgroundColor: secondLabels,
      data: [],
    },
  ];
  let index = 1;
  for (index in globalCasesDeaths) {
    if (globalCasesDeaths[index][0] === 'country_ch') {
      continue;
    }
    cases = globalCasesDeaths[index][2].replace(/,/g, '');
    deaths = globalCasesDeaths[index][3].replace(/,/g, '');
    datasets[0].data.push(cases);
    datasets[1].data.push(deaths);
  }

  return datasets;
}

function getMaxValue(globalCasesDeaths) {
  let index = 1;
  let cases = 0;
  let deaths = 0;
  let maxCases = 0;
  let maxDeaths = 0;
  for (index in globalCasesDeaths) {
    if (globalCasesDeaths[index][0] === 'country_ch') {
      continue;
    }
    cases = Number(globalCasesDeaths[String(index)][2].replace(/,/g, ''));
    deaths = Number(globalCasesDeaths[String(index)][3].replace(/,/g, ''));
    if (maxCases < cases) {
      maxCases = cases;
    }
    if (maxDeaths < deaths) {
      maxDeaths = deaths;
    }
  }

  return {
    'max_cases': maxCases,
    'max_deaths': maxDeaths,
  };
}

function getCountries(globalCasesDeaths) {
  let index = 1;
  let countries = {
    'countries_ch': [],
    'countries_en': [],
  };
  let country = '';
  let countryEn = '';
  for (index in globalCasesDeaths) {
    if (globalCasesDeaths[index][0] === 'country_ch') {
      continue;
    }
    country = globalCasesDeaths[index][0];
    countryEn = globalCasesDeaths[index][1];
    countries['countries_ch'].push(country);
    countries['countries_en'].push(countryEn);
  }

  return countries;
}

export default {
  name: 'AgstableWeeklyCov19',
  components: {
      Vue3ChartJs,
      VueMultiselect,
  },
  setup() {
    let maxValues = getMaxValue(globalCasesDeaths);
    let maxCases = maxValues['max_cases'];
    let maxDeaths = maxValues['max_deaths'];
    let maxValue = (maxCases > maxDeaths ? maxCases : maxDeaths);

    const barChart = {
      type: 'bar',
      options: {
          min: 0,
          max: maxValue,
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
          },
          scales: {
            y: {
              min: 0,
              max: maxValue,
              ticks: {
                callback: function (value) {
                  return numeral(value).format('0,0');
                }
              },
            },
          },
      },
      data: {
        labels: getCountries(globalCasesDeaths)['countries_ch'],
        datasets: getDatasets(globalCasesDeaths),
      },
    };
    let chartRef = ref(barChart);

    const updateBarChart = (filteredResults) => {
      barChart.options.plugins.title = {
        display: true
      };
      barChart.options.max = getMaxValue(filteredResults);
      barChart.options.scales.y.max = getMaxValue(filteredResults);
      barChart.data.labels = getCountries(filteredResults)['countries_ch'];
      barChart.data.datasets = getDatasets(filteredResults);
      if (typeof chartRef.value.update !== 'undefined') {
        chartRef.value.update();
      }
    };

    return {
      globalCasesDeaths,
      barChart,
      updateBarChart,
      chartRef,
    };
  },
  data() {
    return {
      title: 'COVID-19各國家地區累積病例數與死亡數',
      filter: [],
      checked: false,
      countries: getCountries(globalCasesDeaths)['countries_ch'],
      countriesEn: getCountries(globalCasesDeaths)['countries_en'],
      maxCases: 0,
      maxDeaths: 0,
      selected: null,
      labTableButton: '顯示篩檢所列表',
    };
  },
  mounted() {
  },
  methods: {
    collapseButton(event) {
      if (event.target.text === '顯示篩檢所列表') {
        this.labTableButton = '關閉篩檢所列表';
      } else {
        this.labTableButton = '顯示篩檢所列表';
      }
    },
  },
  computed: {
    filteredTable() {
      if (this.filter.length === 0) {
        this.updateBarChart(this.globalCasesDeaths);

        return this.globalCasesDeaths;
      }

      let filteredResults = findCountriesByKeyword(this.globalCasesDeaths, this.filter);
      this.updateBarChart(filteredResults);

      return filteredResults;
    },
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
