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
          <tbody id="covid19-data-rows"></tbody>
        </table>
      </div>
    </div>
  </div>
  <span id="Modal20210530"></span>
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
    let covid19DataArray = this.covid19Data;
    let addDaySecond = 86400000;
    let tmpMonth = 0;
    let date = new Date();
    tmpMonth = date.getMonth() + 1;
    if (String(tmpMonth).length === 1) {
      tmpMonthStr = '0' + tmpMonth;
    }
    let startDateStr = date.getFullYear() + '-' + tmpMonthStr + '-' + date.getDate();
    let startDate = new Date(startDateStr);
    let currentDate = startDate.getTime();
    if (covid19DataArray[startDateStr] === undefined) {
      currentDate -= addDaySecond;
      startDate = new Date(currentDate);
      tmpMonth = startDate.getMonth() + 1;
      if (String(tmpMonth).length === 1) {
        tmpMonthStr = '0' + tmpMonth;
      }
      startDateStr = startDate.getFullYear() + '-' + tmpMonthStr + '-' + startDate.getDate();
    }
    let tmpMonthStr = '';
    let counter = 1;
    let rowEle = '<tr>';
    let rowModalEle = '';
    let rowModalTemplate = `
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">當日各縣市確診總人數</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">modal_body</div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
          </div>
          </div>
        </div>`;

    rowModalEle = rowModalTemplate;
    let rowListGropus = '<ol class="list-group list-group-numbered">';
    let county = '';
    let countyCounter = 0;
    while(covid19DataArray[startDateStr] !== undefined) {
      rowEle += '<th scope="row">' + counter + '</th>';
      rowEle += '<td>' + startDateStr + '</td>';
      rowEle += '<td>' + covid19DataArray[startDateStr]['title'] + '</td>';
      rowEle += '<td>' + covid19DataArray[startDateStr]['confirmed_total_counts'] + '</td>';
      rowEle += '<td><button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#' + 'Modal'+ startDateStr.replace(/-/g, '') + '">' + '點我' + '</button></td>';
      rowEle += '<td><a target="_blank" href="' + covid19DataArray[startDateStr]['link'] + '" class="link-info">' + '點我' + '</a></td>';

      for (var index=0;index<covid19DataArray[startDateStr]['confirmed_case_texts'].length; index++) {
        county = covid19DataArray[startDateStr]['confirmed_case_texts'][index].substring(0, 3);
        countyCounter = covid19DataArray[startDateStr]['confirmed_counts'][index];
        rowListGropus += '<li class="list-group-item d-flex justify-content-between align-items-start">';
        rowListGropus += '<div class="ms-2 me-auto"><div class="fw-bold">'+ county + '</div></div><span class="badge bg-primary rounded-pill">' + countyCounter + '</span>';
        rowListGropus += '</li>';
      }

      rowModalEle = rowModalEle.replace('exampleModal', 'Modal' + startDateStr.replace(/-/g, ''));
      rowModalEle = rowModalEle.replace(/exampleModalLabel/g, 'ModalLabel' + startDateStr.replace(/-/g, ''));
      rowModalEle = rowModalEle.replace('modal_body', rowListGropus + '</ol>');
      document.getElementById('main-block').insertAdjacentHTML('beforeend', rowModalEle);

      currentDate -= addDaySecond;
      startDate = new Date(currentDate);

      tmpMonth = startDate.getMonth() + 1;
      if (String(tmpMonth).length === 1) {
        tmpMonthStr = '0' + tmpMonth;
      }
      counter += 1;
      rowEle += '<tr>';
      rowListGropus = '<ol class="list-group list-group-numbered">';
      rowModalEle = rowModalTemplate;
      startDateStr = startDate.getFullYear() + '-' + tmpMonthStr + '-' + startDate.getDate();
    }

    document.getElementById('covid19-data-rows').innerHTML = rowEle;
  },
}
</script>
