<template>
<header>
  <!-- Fixed navbar -->
  <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">{{ message }}</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="/">{{ home }}</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</header>
<!-- Begin page content -->
<main id="main-block" class="flex-shrink-0">
  <div class="container">
    <h1 class="mt-5">{{ title }}</h1>
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
            <tr v-for="data in covid19Data" :key="data">
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
  <div v-for="data in covid19Data" :key="data" class="modal fade" v-bind:id="data.modal_id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
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

export default {
  name: 'COVID-19 Taiwan News',
  props: {
    message: String,
    title: String,
    filter: String,
    home: String,
    covid19Data: Object,
  },
  mounted() {
  },
}
</script>
