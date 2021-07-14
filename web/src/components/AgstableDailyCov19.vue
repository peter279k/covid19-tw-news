<template>
  <!-- Begin page content -->
  <main id="main-block" class="flex-shrink-0">
  <div class="container">
    <h1 class="mt-5">{{ title }}</h1>
    <div class="row">
      <div class="col">
        <h3 class="text-info mt-6">{{ '境外移入確診總人數：' + String(sumOfImportedCases) }}</h3>
      </div>
      <div class="col">
        <h3 class="text-info mt-6">{{ '本土確診總人數：' + String(sumOfLocalCases) }}</h3>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <vue3-chart-js v-bind="{ ...monthOfImportedCaseBarLineChart }" />
      </div>
      <div class="col">
        <vue3-chart-js v-bind="{ ...monthOfLocalCaseBarLineChart }" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <vue3-chart-js v-bind="{ ...importedCasesPieChart }" />
      </div>
      <div class="col">
        <vue3-chart-js v-bind="{ ...localCasesPieChart }" />
      </div>
      <div class="col">
        <vue3-chart-js v-bind="{ ...allCasesPieChart }" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <vue3-chart-js v-bind="{ ...importedCasesOfAgeBarChart }" />
      </div>
      <div class="col">
        <vue3-chart-js v-bind="{ ...localCasesOfAgeBarChart }" />
      </div>
      <div class="col">
        <vue3-chart-js v-bind="{ ...allCasesOfAgeBarChart }" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <vue3-chart-js v-bind="{ ...importedCasesAgeRangeBarChart }" />
      </div>
    </div>
    <div class="row">
       <div class="col">
        <vue3-chart-js v-bind="{ ...localCasesAgeRangeBarChart }" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <vue3-chart-js v-bind="{ ...allCasesAgeRangeBarChart }" />
      </div>
    </div>
    <div class="row">
      <div class="col">
        <vue3-chart-js v-bind="{ ...countyLocalCasesBarChart }" />
      </div>
    </div>
  </div>
  </main>
</template>

<script>
import Vue3ChartJs from '@j-t-mcc/vue3-chartjs'
import DayConfirmationAgeCountyGender19CoV from '../assets/DayConfirmationAgeCountyGender19CoV.json'

function getRandomHexColors(counter, isUnique=false) {
  let colors = new Array(counter);
  let randomHexColor = String('#' + Math.floor(Math.random()*16777215).toString(16));

  if (isUnique) {
    colors.fill('');
    return colors.map((value) => {
      value = String('#' + Math.floor(Math.random()*16777215).toString(16));
      value = hexToRgb(value);

      return 'rgb(' + value.r + ',' + value.g + ',' + value.b + ')';
    });
  }

  return colors.fill(randomHexColor);
}

function hexToRgb(hex) {
  if (hex.length !== 7) {
    hex += hex[hex.length-1];
  }
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
}

function getSumOfImportedCases() {
  let county = '';
  let importedCases = 0;
  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    if (county !== '空值') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    importedCases += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
  }

  return importedCases;
}

function getSumOfLocalCases() {
  let county = '';
  let localCases = 0;
  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    if (county === '空值') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    localCases += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
  }

  return localCases;

}

function getAgeRangesOfCasesNumbers() {
  let ageRangesOfImportedCases = {};
  let ageRangesOfLocalCases = {};
  let ageRangesOfAllCases = {};
  let ageRangesOfImportedCasesKey = [];
  let ageRangesOfLocalCasesKey = [];
  let ageRangesOfAllCasesKey = [];
  let county = '';

  let ageRangeStr = '';
  let cases = 0;
  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }

    ageRangeStr = String(DayConfirmationAgeCountyGender19CoV[caseIndex][6]);
    cases = Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    ageRangesOfAllCasesKey = Object.keys(ageRangesOfAllCases);
    ageRangesOfLocalCasesKey = Object.keys(ageRangesOfLocalCases);
    ageRangesOfImportedCasesKey = Object.keys(ageRangesOfImportedCases);

    if (!ageRangesOfAllCasesKey.includes(ageRangeStr)) {
      ageRangesOfAllCases[ageRangeStr] = cases;
    } else {
      ageRangesOfAllCases[ageRangeStr] += cases;
    }

    if (county !== '空值') {
      if (!ageRangesOfLocalCasesKey.includes(ageRangeStr)) {
        ageRangesOfLocalCases[ageRangeStr] = cases;
      } else {
        ageRangesOfLocalCases[ageRangeStr] += cases;
      }
    } else {
      if (!ageRangesOfImportedCasesKey.includes(ageRangeStr)) {
        ageRangesOfImportedCases[ageRangeStr] = cases;
      } else {
        ageRangesOfImportedCases[ageRangeStr] += cases;
      }
    }
  }

  return [
    ageRangesOfImportedCases,
    ageRangesOfLocalCases,
    ageRangesOfAllCases,
  ];
}

function getSumOfImportedCasesFemales() {
  let county = '';
  let importedCases = 0;
  let sex = '';
  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    sex = DayConfirmationAgeCountyGender19CoV[caseIndex][4];
    if (county !== '空值') {
      continue;
    }
    if (sex === '男') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    importedCases += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
  }

  return importedCases;
}

function getSumOfLocalCasesFemales() {
  let county = '';
  let localCases = 0;
  let sex = '';
  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    sex = DayConfirmationAgeCountyGender19CoV[caseIndex][4];
    if (county === '空值') {
      continue;
    }
    if (sex === '男') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    localCases += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
  }

  return localCases;
}

function getSumOfImportedCasesMales() {
  let county = '';
  let importedCases = 0;
  let sex = '';
  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    sex = DayConfirmationAgeCountyGender19CoV[caseIndex][4];
    if (county !== '空值') {
      continue;
    }
    if (sex !== '男') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    importedCases += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
  }

  return importedCases;
}

function getSumOfLocalCasesMales() {
  let county = '';
  let localCases = 0;
  let sex = '';
  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    sex = DayConfirmationAgeCountyGender19CoV[caseIndex][4];
    if (county === '空值') {
      continue;
    }
    if (sex !== '男') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    localCases += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
  }

  return localCases;
}

function monthOfImportedCases() {
  let importedCasesOfMonth = {};
  let monthKeys = [];
  let monthKey = '';
  let county = '';

  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    monthKey = DayConfirmationAgeCountyGender19CoV[caseIndex][1];
    monthKey = monthKey.replace(/\//g, '');
    monthKey = monthKey.substring(0, 6);
    monthKeys = Object.keys(importedCasesOfMonth);
    if (county !== '空值') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    if (!monthKeys.includes(monthKey)) {
      importedCasesOfMonth[monthKey] = Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
    } else {
      importedCasesOfMonth[monthKey] += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
    }
  }

  return importedCasesOfMonth;
}

function monthOfLocalCases() {
  let localCasesOfMonth = {};
  let monthKeys = [];
  let monthKey = '';
  let county = '';

  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    county = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    monthKey = DayConfirmationAgeCountyGender19CoV[caseIndex][1];
    monthKey = monthKey.replace(/\//g, '');
    monthKey = monthKey.substring(0, 6);
    monthKeys = Object.keys(localCasesOfMonth);
    if (county === '空值') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    if (!monthKeys.includes(monthKey)) {
      localCasesOfMonth[monthKey] = Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
    } else {
      localCasesOfMonth[monthKey] += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
    }
  }

  return localCasesOfMonth;
}

function countyOfLocalCases() {
  let localCasesOfCounty = {};
  let countyKeys = [];
  let countyKey = '';

  for (let caseIndex in DayConfirmationAgeCountyGender19CoV) {
    if (caseIndex === 0) {
      continue;
    }
    countyKey = DayConfirmationAgeCountyGender19CoV[caseIndex][2];
    countyKeys = Object.keys(localCasesOfCounty);
    if (countyKey === '空值') {
      continue;
    }
    if (DayConfirmationAgeCountyGender19CoV[caseIndex][7] === '確定病例數') {
      continue;
    }
    if (!countyKeys.includes(countyKey)) {
      localCasesOfCounty[countyKey] = Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
    } else {
      localCasesOfCounty[countyKey] += Number(DayConfirmationAgeCountyGender19CoV[caseIndex][7]);
    }
  }

  return localCasesOfCounty;
}

function getMonthLocalCaseBarLineChart() {
  let monthOfLocalCasesObj = monthOfLocalCases();
  let monthOfLocalCaseValues = Object.values(monthOfLocalCasesObj);
  let monthOfLocalCasesObjKeys = Object.keys(monthOfLocalCasesObj);
  monthOfLocalCasesObjKeys = monthOfLocalCasesObjKeys.map((value) => {
    let string = String(value);

    return string.substring(0, 4) + '-' + string.substring(4);
  });

  return {
    type: 'line',
    data: {
      datasets: [
        {
          type: 'bar',
          label: '月份長條圖',
          data: monthOfLocalCaseValues,
          borderColor: 'rgb(26, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          stack: 'combined',
        },
        {
          label: '月份折線圖',
          data: monthOfLocalCaseValues,
          fill: false,
          borderColor: 'rgb(54, 162, 235)',
          stack: 'combined',
        }
      ],
      labels: monthOfLocalCasesObjKeys,
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '全國本土病例確診人數月份曲線圖',
        },
        scales: {
          y: {
            stacked: true,
          },
        },
      },
    },
  };
}

function getMonthImportedCaseBarLineChart() {
  let monthOfImportedCasesObj = monthOfImportedCases();
  let monthOfImportedCaseValues = Object.values(monthOfImportedCasesObj);
  let monthOfImportedCasesObjKeys = Object.keys(monthOfImportedCasesObj);
  monthOfImportedCasesObjKeys = monthOfImportedCasesObjKeys.map((value) => {
    let string = String(value);

    return string.substring(0, 4) + '-' + string.substring(4);
  });

  return {
    type: 'line',
    data: {
      datasets: [
        {
          type: 'bar',
          label: '月份長條圖',
          data: monthOfImportedCaseValues,
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          stack: 'combined',
        },
        {
          label: '月份折線圖',
          data: monthOfImportedCaseValues,
          fill: false,
          borderColor: 'rgb(54, 162, 235)',
          stack: 'combined',
        }
      ],
      labels: monthOfImportedCasesObjKeys,
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '全國境外移入病例確診人數月份曲線圖',
        },
        scales: {
          y: {
            stacked: true,
          },
        },
      },
    },
  }
}

function getImportedCasesPieChart() {
  let importedCasesOfMale = getSumOfImportedCasesMales();
  let importedCasesOfFemale = getSumOfImportedCasesFemales();
  let sumOfCases = importedCasesOfMale + importedCasesOfFemale;
  let importedMaleRate = importedCasesOfMale / sumOfCases * 100;
  let importedFemaleRate = importedCasesOfFemale / sumOfCases * 100;

  return {
    type: 'pie',
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '全國境外移入確診人數性別比',
        },
      },
    },
    data: {
      labels: ['男 (%)', '女 (%)'],
      datasets: [{
        label: '全國境外移入確診人數性別比',
        data: [importedMaleRate, importedFemaleRate],
        backgroundColor: [
          'rgb(54, 162, 235)',
          'rgb(255, 99, 132)',
        ],
        hoverOffset: 4
      }],
    },
  }
}

function getLocalCasesPieChart() {
  let localCasesOfMale = getSumOfLocalCasesMales();
  let localCasesOfFemale = getSumOfLocalCasesFemales();
  let sumOfCases = localCasesOfMale + localCasesOfFemale;
  let localCasesMaleRate = localCasesOfMale / sumOfCases * 100;
  let localCasesFemaleRate = localCasesOfFemale / sumOfCases * 100;

  return {
    type: 'pie',
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '全國本土病例確診人數性別比',
        },
      },
    },
    data: {
      labels: ['男 (%)', '女 (%)'],
      datasets: [{
        label: '全國本土病例確診人數性別比',
        data: [localCasesMaleRate, localCasesFemaleRate],
        backgroundColor: [
          'rgb(54, 162, 235)',
          'rgb(255, 99, 132)',
        ],
        hoverOffset: 4
      }],
    },
  }
}

function getAllCasesPieChart() {
  let allCasesOfMale = getSumOfImportedCasesMales() + getSumOfLocalCasesMales();
  let allCasesOfFemale = getSumOfImportedCasesFemales() + getSumOfLocalCasesFemales();
  let sumOfCases = allCasesOfMale + allCasesOfFemale;
  let allCasesMaleRate = allCasesOfMale / sumOfCases * 100;
  let allCasesFemaleRate = allCasesOfFemale / sumOfCases * 100;

  return {
    type: 'pie',
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '全國確診人數性別比',
        },
      },
    },
    data: {
      labels: ['男 (%)', '女 (%)'],
      datasets: [{
        label: '全國確診人數性別比',
        data: [allCasesMaleRate, allCasesFemaleRate],
        backgroundColor: [
          'rgb(54, 162, 235)',
          'rgb(255, 99, 132)',
        ],
        hoverOffset: 4
      }],
    }
  };
}

function getImportedCasesAgeRangeBarChart(isRatio=false) {
  let ageRangeOfCaseNumbers = getAgeRangesOfCasesNumbers();
  let ageRangeImportedCases = ageRangeOfCaseNumbers[0];
  let ageRangeImportedCasesOfSum = Object.values(ageRangeImportedCases).reduce((current, next) => {
    return current + next;
  });
  let ageRangeImportedCasesValues = [];
  let ageRangeImportedCasesRatioValues = [];
  let ageRanges = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5-9',
    '10-14',
    '15-19',
    '20-24',
    '25-29',
    '30-34',
    '35-39',
    '40-44',
    '45-49',
    '50-54',
    '55-59',
    '60-64',
    '65-69',
    '70+',
  ];
  for (let index in ageRanges) {
    if (ageRangeImportedCases[ageRanges[index]]) {
      ageRangeImportedCasesValues.push(ageRangeImportedCases[ageRanges[index]]);
      ageRangeImportedCasesRatioValues.push(ageRangeImportedCases[ageRanges[index]] / ageRangeImportedCasesOfSum * 100);
    } else {
      ageRangeImportedCasesValues.push(0);
      ageRangeImportedCasesRatioValues.push(0.0);
    }
  }

  if (isRatio) {
    return {
      type: 'pie',
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: '全國境外移入確診人數年齡比(%)',
          },
        } ,
      },
      data: {
        labels: ageRanges.map((value) => { return value + '歲(%)'; }),
        datasets: [{
          label: '全國境外移入確診人數年齡比(%)',
          data: ageRangeImportedCasesRatioValues,
          backgroundColor: getRandomHexColors(ageRanges.length, true),
          hoverOffset: 4
        }],
      },
    }
  }

  return {
    type: 'bar',
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
      },
      scales: {
        y: {
          ticks: {
            callback: function (value) {
              return numeral(value).format('0,0');
            }
          },
        },
      },
    },
    data: {
      labels: ageRanges,
      datasets: [{
        label: '全國境外移入人數年齡分佈',
        data: ageRangeImportedCasesValues,
        backgroundColor: getRandomHexColors(ageRangeImportedCasesValues.length),
        borderWidth: 1,
      }],
    },
  };
}

function getLocalCasesAgeRangeBarChart(isRatio=false) {
  let ageRangeOfCaseNumbers = getAgeRangesOfCasesNumbers();
  let ageRangeLocalCasesValues = [];
  let ageRangeLocalCasesRatioValues = [];
  let ageRangeLocalCases = ageRangeOfCaseNumbers[1];
  let ageRangeLocalCasesOfSum = Object.values(ageRangeLocalCases).reduce((current, next) => {
    return current + next;
  });
  let ageRanges = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5-9',
    '10-14',
    '15-19',
    '20-24',
    '25-29',
    '30-34',
    '35-39',
    '40-44',
    '45-49',
    '50-54',
    '55-59',
    '60-64',
    '65-69',
    '70+',
  ];
  let value = 0;

  for (let index in ageRanges) {
    value = ageRangeLocalCases[ageRanges[index]];
    if (value) {
      ageRangeLocalCasesValues.push(value);
      ageRangeLocalCasesRatioValues.push(value / ageRangeLocalCasesOfSum * 100);
    } else {
      ageRangeLocalCasesValues.push(0);
      ageRangeLocalCasesRatioValues.push(0.0);
    }
  }

  if (isRatio) {
    return {
      type: 'pie',
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: '全國本土確診人數年齡比(%)',
          },
        } ,
      },
      data: {
        labels: ageRanges.map((value) => { return value + '歲(%)'; }),
        datasets: [{
          label: '全國本土確診人數年齡比(%)',
          data: ageRangeLocalCasesRatioValues,
          backgroundColor: getRandomHexColors(ageRanges.length, true),
          hoverOffset: 4
        }],
      },
    }
  }

  return {
    type: 'bar',
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
      },
      scales: {
        y: {
          ticks: {
            callback: function (value) {
              return numeral(value).format('0,0');
            }
          },
        },
      },
    },
    data: {
      labels: ageRanges,
      datasets: [{
        label: '全國本土病例人數之年齡分佈',
        data: ageRangeLocalCasesValues,
        backgroundColor: getRandomHexColors(ageRangeLocalCasesValues.length),
        borderWidth: 1,
      }],
    },
  };
}

function getAllCasesAgeRangeBarChart(isRatio=false) {
  let ageRangeOfCaseNumbers = getAgeRangesOfCasesNumbers();
  let ageRangeAllCasesValues = [];
  let ageRangeAllCasesRatioValues = [];
  let ageRangeAllCases = ageRangeOfCaseNumbers[2];
  let ageRangeAllCasesOfSum = Object.values(ageRangeAllCases).reduce((current, next) => {
    return current + next;
  });

  let ageRanges = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5-9',
    '10-14',
    '15-19',
    '20-24',
    '25-29',
    '30-34',
    '35-39',
    '40-44',
    '45-49',
    '50-54',
    '55-59',
    '60-64',
    '65-69',
    '70+',
  ];
  let value = 0;
  for (let index in ageRanges) {
    value = ageRangeAllCases[ageRanges[index]];
    if (value) {
      ageRangeAllCasesValues.push(value);
      ageRangeAllCasesRatioValues.push(value / ageRangeAllCasesOfSum * 100);
    } else {
      ageRangeAllCasesValues.push(0);
      ageRangeAllCasesRatioValues.push(0.0);
    }
  }

  if (isRatio) {
    return {
      type: 'pie',
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: '全國確診總人數年齡比(%)',
          },
        } ,
      },
      data: {
        labels: ageRanges.map((value) => { return value + '歲(%)'; }),
        datasets: [{
          label: '全國確診總人數年齡比(%)',
          data: ageRangeAllCasesRatioValues,
          backgroundColor: getRandomHexColors(ageRanges.length, true),
          hoverOffset: 4
        }],
      },
    }
  }

  return {
    type: 'bar',
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
      },
      scales: {
        y: {
          ticks: {
            callback: function (value) {
              return numeral(value).format('0,0');
            }
          },
        },
      },
    },
    data: {
      labels: ageRanges,
      datasets: [{
        label: '全國確診總人數年齡分佈',
        data: ageRangeAllCasesValues,
        backgroundColor: getRandomHexColors(ageRangeAllCasesValues.length),
        borderWidth: 1,
      }],
    },
  };
}

function getCountyLocalCasesBarChart() {
  let countyOfLocalCasesObj = countyOfLocalCases();
  let countyOfLocalCasesObjKey = [
    '台北市',
    '新北市',
    '桃園市',
    '新竹市',
    '新竹縣',
    '苗栗縣',
    '台中市',
    '彰化縣',
    '南投縣',
    '雲林縣',
    '嘉義市',
    '嘉義縣',
    '台南市',
    '高雄市',
    '屏東縣',
    '基隆市',
    '宜蘭縣',
    '花蓮縣',
    '台東縣',
    '連江縣',
    '澎湖縣',
    '金門縣',
  ];
  let countyOfLocalCasesObjValues = [];
  let value = null;
  for (let index in countyOfLocalCasesObjKey) {
    value = countyOfLocalCasesObj[countyOfLocalCasesObjKey[index]];
    if (value) {
      countyOfLocalCasesObjValues.push(value);
    } else {
      countyOfLocalCasesObjValues.push(0);
    }
  }

  return {
    type: 'bar',
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
      },
      scales: {
        y: {
          ticks: {
            callback: function (value) {
              return numeral(value).format('0,0');
            }
          },
        },
      },
    },
    data: {
      labels: countyOfLocalCasesObjKey,
      datasets: [{
        label: '全國各縣市確診分佈',
        data: countyOfLocalCasesObjValues,
        backgroundColor: getRandomHexColors(countyOfLocalCasesObjValues.length),
        borderWidth: 1,
      }],
    },
  };
}

var numeral = require('numeral');

export default {
  name: 'AgstableDailyCov19',
  components: {
      Vue3ChartJs,
  },
  setup() {
    const monthOfLocalCaseBarLineChart = getMonthLocalCaseBarLineChart();
    const monthOfImportedCaseBarLineChart = getMonthImportedCaseBarLineChart();

    const importedCasesPieChart = getImportedCasesPieChart();
    const localCasesPieChart = getLocalCasesPieChart();
    const allCasesPieChart = getAllCasesPieChart();

    const importedCasesAgeRangeBarChart = getImportedCasesAgeRangeBarChart();
    const localCasesAgeRangeBarChart = getLocalCasesAgeRangeBarChart();
    const allCasesAgeRangeBarChart = getAllCasesAgeRangeBarChart();

    const countyLocalCasesBarChart = getCountyLocalCasesBarChart();

    const importedCasesOfAgeBarChart = getImportedCasesAgeRangeBarChart(true);
    const localCasesOfAgeBarChart = getLocalCasesAgeRangeBarChart(true);
    const allCasesOfAgeBarChart = getAllCasesAgeRangeBarChart(true);

    return {
      monthOfLocalCaseBarLineChart,
      monthOfImportedCaseBarLineChart,
      importedCasesPieChart,
      localCasesPieChart,
      allCasesPieChart,
      importedCasesAgeRangeBarChart,
      localCasesAgeRangeBarChart,
      allCasesAgeRangeBarChart,
      importedCasesOfAgeBarChart,
      localCasesOfAgeBarChart,
      allCasesOfAgeBarChart,
      countyLocalCasesBarChart,
    };
  },
  data() {
    return {
      title: '臺灣COVID-19各式資料統計',
      filter: '',
      sumOfLocalCases: getSumOfLocalCases(),
      sumOfImportedCases: getSumOfImportedCases(),
    };
  },
  mounted() {
  },
  methods: {
  },
  computed: {
  },
}
</script>
