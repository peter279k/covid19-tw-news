<template>
<!-- Begin page content -->
<main id="main-block" class="flex-shrink-0">
  <div class="container">
    <h1 class="mt-5" v-html="title"></h1>
    <h1 v-html="subTitle"></h1>
    <input v-model="filter" type="search" class="form-control" id="input_keywords" placeholder="請輸入關鍵字"/>
    <div class="row">
      <div id="covid-19-table" class="col">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">日期</th>
              <th scope="col">標題</th>
              <th scope="col">當日本土確診</th>
              <th scope="col">當日各縣市確診</th>
              <th scope="col">相關連結</th>
            </tr>
          </thead>
          <tbody id="covid19-data-rows">
            <tr v-for="data in filteredTable" :key="data">
              <th scope="row">{{ data.index }}</th>
              <td>{{ data.date }}</td>
              <td>{{ data.title }}</td>
              <td>{{ data.confirmed_total_counts }}</td>
              <td><button type="button" class="btn btn-primary" data-bs-toggle="modal" v-bind:data-bs-target="data.modal">點我</button></td>
              <td><a target="_blank" v-bind:href="data.link" class="link-info">點我</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div v-for="data in filteredTable" :key="data" class="modal fade" v-bind:id="data.modal_id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">當日各縣市確診總人數</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
      <div class="modal-body">
        <ol class="list-group list-group-numbered">
          <li v-for="(confirmedCounts, index) in data.confirmed_counts" :key="confirmedCounts" class="list-group-item d-flex justify-content-between align-items-start">
            <div class="ms-2 me-auto"><div class="fw-bold">{{ data.confirmed_case_texts[index].substring(0, 3) }}</div></div><span class="badge bg-primary rounded-pill">{{ confirmedCounts }}</span>
          </li>
        </ol>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
    </div>
  </div>
</main>
</template>

<script>
import covid19Data from '../assets/covid19_data.json'

export default {
  name: 'Index',
  setup() {
    return {
      covid19Data,
    };
  },
  data() {
    return {
      title: '這是台灣COVID-19 訊息<span class="text-danger">(暫停更新)</span>',
      subTitle: '<a href="/mohwRSS">請使用衛生福利部RSS訊息</a>',
      filter: '',
    };
  },
  computed: {
    filteredTable() {
      if (this.filter === '') {
        return this.covid19Data;
      }
      let results = {};
      for (var dateIndex in this.covid19Data) {
        if (dateIndex.includes(this.filter)) {
          results[dateIndex] = this.covid19Data[dateIndex];
          continue;
        }
        if (this.covid19Data[dateIndex].title.includes(this.filter)) {
          results[dateIndex] = this.covid19Data[dateIndex];
          continue;
        }
      }
      return results;
    },
  },
}
</script>
