<template>
  <!-- Begin page content -->
  <main id="main-block" class="flex-shrink-0">
    <div class="container">
      <h1 class="mt-5">{{ title }}</h1>
      <div class="row">
         <div class="col">
          <select v-model="filterCounty" v-on:change="filteredCounty($event)" class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
            <option value="select_county" selected>請選擇縣市</option>
            <option v-for="(county, index) in counties" :key="index" :value="index">{{ county }}</option>
          </select>
        </div>
        <div class="col">
          <a class="btn btn-primary" v-on:click="collapseButton($event)" data-bs-toggle="collapse" href="#collapseLabTable" role="button" aria-expanded="false" aria-controls="collapseExample">
            {{ labTableButton }}
          </a>
        </div>
      </div>
      <div class="row">
        <div class="collapse" id="collapseLabTable">
        <div id="covid-19-labs-table" class="col card card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">縣市</th>
              <th scope="col">篩檢所名稱</th>
              <th scope="col">篩檢所地址</th>
              <th scope="col">電話</th>
            </tr>
          </thead>
          <tbody id="covid19-labs-rows">
            <tr v-for="data in filteredLabsTable" :key="data">
              <td>{{ data.county }}</td>
              <td>{{ data.agency_name }}</td>
              <td>{{ data.address }}</td>
              <td>{{ data.phone_number }}</td>
            </tr>
          </tbody>
        </table>
        </div>
        </div>
      </div>
      <div class="row">
        <div id="map" class="col"></div>
      </div>
    </div>
  </main>
</template>

<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet/dist/leaflet.js";
import covid19Labs from "../assets/covid19_labs.json";

export default {
  name: 'Labs',
  setup() {
    return {
      covid19Labs,
    };
  },
  data() {
    return {
      title: '篩檢所分布地圖',
      labTableButton: '顯示篩檢所列表',
      map: null,
      markers: null,
      counties: [],
      filterCounty: 'select_county',
    };
  },
  methods: {
    collapseButton(event) {
      if (event.target.text === '顯示篩檢所列表') {
        this.labTableButton = '關閉篩檢所列表';
      } else {
        this.labTableButton = '顯示篩檢所列表';
      }
    },
    filteredCounty(event) {
      let county = null;
      let popupTemplate = '';
      if (event.target.value === 'select_county') {
        county = this.counties;
      } else {
        county = this.counties[event.target.value];
      }

      if (this.map) {
        this.map.removeLayer(this.markers);
        this.markers = new L.FeatureGroup();
      }

      let marker = null;
      for (let agentCode in covid19Labs) {
        if (typeof county === 'string' && county !== covid19Labs[agentCode]['county']) {
          continue;
        }
        popupTemplate = '<p>' + covid19Labs[agentCode]['address'] + '</p><p>' + covid19Labs[agentCode]['agency_name'] + '</p>電話：' + covid19Labs[agentCode]['phone_number'];
        marker = L.marker(L.latLng(covid19Labs[agentCode]['latitude'], covid19Labs[agentCode]['longitude']));
        marker.bindPopup(popupTemplate, {
          showOnMouseOver: true,
        });

        this.markers.addLayer(marker);
      }
      this.map.addLayer(this.markers);
    },
  },
  computed: {
    filteredLabsTable() {
      let county = this.counties[this.filterCounty];
      if (this.filterCounty === 'select_county' || this.filterCounty === '') {
        return this.covid19Labs;
      }
      let results = {};
      for (let agentCode in covid19Labs) {
        if (covid19Labs[agentCode]['county'] === county) {
          results[agentCode] = covid19Labs[agentCode];
        }
      }

      return results;
    },
  },
  mounted() {
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
      iconUrl: require("leaflet/dist/images/marker-icon.png"),
      shadowUrl: require("leaflet/dist/images/marker-shadow.png")
    });

    /* instantiate and configure map */
    let markers = new L.FeatureGroup();
    let minZoom = 7;
    let maxZoom = 30;
    let initLat = 25.105497;
    let initLng = 121.597366;
    this.counties = [];
    this.map = L.map('map').setView(L.latLng(initLat, initLng), minZoom);
    let accessToken = process.env.VUE_APP_MAPKEY;

    if (!accessToken) {
      console.log('Access token is required');
    }

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}',
      {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery  <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: accessToken,
        minZoom: minZoom,
        maxZoom: maxZoom,
      }).addTo(this.map);

    if (this.map) {
      this.map.removeLayer(markers);
      markers = new L.FeatureGroup();
    }

    let marker = null;
    let popupTemplate = '';
    for (let agentCode in covid19Labs) {
      if (!this.counties.includes(covid19Labs[agentCode]['county'])) {
        this.counties.push(covid19Labs[agentCode]['county']);
      }
      marker = L.marker(L.latLng(covid19Labs[agentCode]['latitude'], covid19Labs[agentCode]['longitude']));
      popupTemplate = '<p>' + covid19Labs[agentCode]['address'] + '</p><p>' + covid19Labs[agentCode]['agency_name'] + '</p>電話：' + covid19Labs[agentCode]['phone_number'];
      marker.bindPopup(popupTemplate, {
        showOnMouseOver: true,
      });

      markers.addLayer(marker);
    }
    this.map.addLayer(markers);
    this.markers = markers;
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove();
    }
  },
}
</script>

<style scoped>
  #map {
    width: 100vw;
    height: 100vh;
  }
</style>
