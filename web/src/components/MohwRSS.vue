<template>
  <!-- Begin page content -->
  <main id="main-block" class="flex-shrink-0">
  <div class="container">
    <h1 class="mt-5">{{ title }}</h1>
    <form class="row g-1">
        <div class="col">
          <input v-model="filter" type="search" class="form-control" id="input_keywords" placeholder="請輸入關鍵字"/>
        </div>
        <div class="col">
          <div class="form-check">
            <input v-model="checked" class="form-check-input" type="checkbox" value="" id="flexCheckDefault">
            <label class="form-check-label text-primary" for="flexCheckDefault">
              篩選本土案例新聞
            </label>
          </div>
        </div>
    </form>
    <div class="row">
      <div id="covid-19-table" class="col">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">發布時間</th>
              <th scope="col">發布單位</th>
              <th scope="col">標題</th>
              <th scope="col">描述</th>
              <th scope="col">連結</th>
            </tr>
          </thead>
          <tbody id="covid19-data-rows">
            <tr v-for="data in filteredTable" :key="data">
              <template v-if="data.title.indexOf('指揮中心公布新增') !== -1">
                <td class="table-primary">{{ new Date(data.pub_date).toJSON().split('T')[0] }}</td>
                <td class="table-primary">{{ data.department_name }}</td>
                <td class="table-primary">{{ data.title.length > 38 ? data.title.substring(0, 35) + '...' : data.title }}</td>
                <td class="table-primary"><button type="button" class="btn btn-primary" data-bs-toggle="modal" v-bind:data-bs-target="data.modal_news_id">點我</button></td>
                <td class="table-primary"><a target="_blank" v-bind:href="data.link" class="link-info">點我</a></td>
              </template>
              <template v-else-if="data.title.substring(0, 2) === '新增'">
                <td class="table-primary">{{ new Date(data.pub_date).toJSON().split('T')[0] }}</td>
                <td class="table-primary">{{ data.department_name }}</td>
                <td class="table-primary">{{ data.title.length > 38 ? data.title.substring(0, 35) + '...' : data.title }}</td>
                <td class="table-primary"><button type="button" class="btn btn-primary" data-bs-toggle="modal" v-bind:data-bs-target="data.modal_news_id">點我</button></td>
                <td class="table-primary"><a target="_blank" v-bind:href="data.link" class="link-info">點我</a></td>
              </template>
              <template v-else>
                <td>{{ (new Date(data.pub_date)).toJSON().split('T')[0] }}</td>
                <td>{{ data.department_name }}</td>
                <td>{{ data.title.length > 38 ? data.title.substring(0, 35) + '...' : data.title }}</td>
                <td><button type="button" class="btn btn-primary" data-bs-toggle="modal" v-bind:data-bs-target="data.modal_news_id">點我</button></td>
                <td><a target="_blank" v-bind:href="data.link" class="link-info">點我</a></td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div v-for="data in filteredTable" :key="data" class="modal fade" v-bind:id="data.news_id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h6 class="modal-title text-primary" id="exampleModalLabel">{{ data.title }}</h6>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
      <div class="modal-body" v-html="data.description"></div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
      </div>
    </div>
    </div>
  </div>
  </main>
</template>

<script>
import mohwRSS from '../assets/mohw_rss.json'

export default {
  name: 'MohwRSS',
  setup() {
    return {
      mohwRSS,
    };
  },
  data() {
    return {
      title: '衛生福利部RSS訊息(更新頻率：每小時)',
      filter: '',
      checked: false,
    };
  },
  computed: {
    filteredTable() {
      let dateIndexes = Object.keys(mohwRSS);
      let dateIndex = '';
      let results = {};
      let dateJson = '';

      dateIndexes.sort((a, b) => {
        return new Date(b) - new Date(a);
      });

      let filteredKeyword = this.filter;
      if (this.checked === true) {
        filteredKeyword = '指揮中心公布新增';
      }
      if (filteredKeyword === '') {
        for (var index in dateIndexes) {
          dateIndex = dateIndexes[index];
          results[dateIndex] = mohwRSS[dateIndex];
        }
        return results;
      }

      for (index in dateIndexes) {
        dateIndex = dateIndexes[index];
        dateJson = (new Date(dateIndex)).toJSON().split('T')[0];
        if (dateJson.includes(filteredKeyword)) {
          results[dateIndex] = this.mohwRSS[dateIndex];
          continue;
        }
        if (this.mohwRSS[dateIndex].title.includes(filteredKeyword)) {
          results[dateIndex] = this.mohwRSS[dateIndex];
          continue;
        }
        if (filteredKeyword === '指揮中心公布新增' && this.mohwRSS[dateIndex].title.substring(0, 2) === '新增') {
          results[dateIndex] = this.mohwRSS[dateIndex];
          continue;
        }
        if (this.mohwRSS[dateIndex].department_name.includes(filteredKeyword)) {
          results[dateIndex] = this.mohwRSS[dateIndex];
          continue;
        }
        if (this.mohwRSS[dateIndex].description.includes(filteredKeyword)) {
          results[dateIndex] = this.mohwRSS[dateIndex];
          continue;
        }
      }

      return results;
    },
  },
}
</script>
