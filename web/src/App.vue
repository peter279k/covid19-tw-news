<template>
  <header>
  <!-- Fixed navbar -->
  <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">COVID-19 臺灣消息</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
          <li class="nav-item">
            <router-link class="nav-link active" aria-current="page" :to="{ name: 'Index'}">首頁</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" aria-current="page" :to="{ name: 'mohwRSS'}">衛福部RSS</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" aria-current="page" :to="{ name: 'Labs'}">篩檢所地圖</router-link>
          </li>
          <li class="nav-item dropdown">
            <a id="navbarDropdown" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false" class="nav-link dropdown-toggle" aria-current="page">資料統計</a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="/covid19CountryStats">各國家地區累積病例數與死亡數</a></li>
              <li><a class="dropdown-item" href="/agstableDailyCov19">臺灣COVID-19各式資料統計</a></li>
            </ul>
          </li>
          <li class="nav-item">
            <a href="https://github.com/peter279k/covid19-tw-news#data-sources-%E8%B3%87%E6%96%99%E4%BE%86%E6%BA%90" class="nav-link" target="_blank">資料來源</a>
          </li>
          <li class="nav-item">
            <a href="https://github.com/peter279k/covid19-tw-news" class="nav-link" target="_blank">
            Fork me on Github
            <svg height="16px" fill="#777" class="octicon octicon-mark-github" viewBox="0 0 16 16" version="1.1" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path></svg>
          </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  </header>
  <router-view/>
</template>
