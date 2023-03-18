
// defining a dummy json output when we search a song or click for a decade
let calledFeatures = {
  "danceability": 0.614,
  "energy": 0.809,
  "key": 9,
  "loudness": -4.749,
  "mode": 1,
  "speechiness": 0.0738,
  "acousticness": 0.0105,
  "instrumentalness": 0.000353,
  "liveness": 0.148,
  "valence": 0.354,
  "tempo": 112.023,
  "type": "audio_features",
  "id": "2oap3QptGISyIvwKpnJJId",
  "uri": "spotify:track:2oap3QptGISyIvwKpnJJId",
  "track_href": "https://api.spotify.com/v1/tracks/2oap3QptGISyIvwKpnJJId",
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/2oap3QptGISyIvwKpnJJId",
  "duration_ms": 176774,
  "time_signature": 4
};

let decadeRawData = {
  "danceability": 1.6,
  "energy": 2.809,
  "key": 1,
  "loudness": -1.749,
  "mode": 2,
  "speechiness": 0.0453,
  "acousticness": 0.0305,
  "instrumentalness": 0.0043,
  "liveness": 0.2,
  "valence": 0.1,
  "tempo": 112,
  "type": "audio_features",
  "id": "2oap3QptGISyIvwKpnJJId",
  "uri": "spotify:track:2oap3QptGISyIvwKpnJJId",
  "track_href": "https://api.spotify.com/v1/tracks/2oap3QptGISyIvwKpnJJId",
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/2oap3QptGISyIvwKpnJJId",
  "duration_ms": 176774,
  "time_signature": 4
}

// starting out by pre-determing the song features to be measured on the radar chart
let songFeatures = [
  'danceability',
  'energy',
  'loudness',
  'speechiness',
  'acousticness',
  'liveness'
]

let decadeFeatures = [
  'danceability',
  'energy',
  'loudness',
  'speechiness',
  'acousticness',
  'instrumentalness',
  'liveness',
  'valence',
  'tempo',
  'duration_ms'
]


// function to clean data, assuming it will be aiight
function cleanData(featureData){
  let cleanFeatureData = [];
  for (let k in songFeatures) {
  for (let j in featureData){
    if (j == songFeatures[k]) {
      cleanFeatureData.push(featureData[j])
    };
  };
};
return cleanFeatureData
};

// creating dummy listening event for when a user searches for a song
let typedSong = ""
const songInput = document.querySelector('#search-song');
const artistInput = document.querySelector('#search-artist');
const buttonSubmit = document.querySelector('#submit');

//put on button instead of search
// call in the pre-created bars into the event listener
buttonSubmit.addEventListener("click", (event) => {
    // if song box is empty, return 'you need to fill this in
    // if artist box is empty, return 'you need to fill this in too'
    // else, return song name, artist name 

    songValue = songInput.value
    artistValue = artistInput.value

    if (!songValue || !artistValue) {
      console.log('missing value')
      return
    }
    else {
      songUrl = `https://billboard-predictor.onrender.com/search_spotify/${songValue}/${artistValue}`
      d3.json(songUrl).then(function(data){
        console.log(data)
      })

    }
    return data 
  }
    // songData = cleanData(rawSongData)
    // radarChart.data.datasets[0].data = songData;
    // radarChart.update();
    // console.log(songData)
);


// adding dummy dropdown listener event
const decadeInput = document.querySelector('#decade');

decadeInput.addEventListener('change', (e) => {
  decadeValue = decadeInput.value
  const parameterizeArray = (key, arr) => {
    arr = arr.map(encodeURIComponent)
    return '?'+key+'[]=' + arr.join('&'+key+'[]=')
  }
  results = parameterizeArray('features',songFeatures)
  decadeURL = `https://billboard-predictor.onrender.com/search_spotify/use_model/${songFeatures}/${results}`
  d3.json(decadeURL).then(function(decadeRawData){
    console.log(decadeRawData)});
  // decadeData = cleanData(rawDecadeData)
  // radarChart.data.datasets[1].data = decadeData;
  // radarChart.update();
  // console.log(decadeInput.value)

});

// creating element that selects radar chart
var canvasElement = document.getElementById('radar-compare');

function setSelectedIndex(s, i){
s.options[i-1].selected = true;
return;
}

function createChart(initialDecade){
  const data = {
    labels: songFeatures,
    datasets: [{
      label: 'songs',
      data: [1,2,3,4,5,6],
      fill: true,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgb(255, 99, 132)',
      pointBackgroundColor: 'rgb(255, 99, 132)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(255, 99, 132)'
    }, {
      label: `${initialDecade}`,
      data: [5,3,2,1,2,3],
      fill: true,
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgb(54, 162, 235)',
      pointBackgroundColor: 'rgb(54, 162, 235)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgb(54, 162, 235)'
    }]
  };
  
  var config = {
    type: 'radar',
    data: data,
    options: {
      elements: {
        line: {
          borderWidth: 3
        }
      }
    },
  };
  //var radarChart = new Chart(canvasElement, config);
  var radarChart = new Chart(canvasElement, config);
  return radarChart
};

// creating dummy song data as i expect the output to be like 
// let songData = [];
// for (let k in songFeatures) {
//   for (let j in calledFeatures){
//     if (j == songFeatures[k]) {
//       songData.push(calledFeatures[j])
//     };
//   };
// };

// //creating dummy decade data as i expect the output to be like 
// let decadeData = []
// for (let k in songFeatures) {
//   for (let v in decadeRawData){
//     if (v == songFeatures[k]) {
//       decadeData.push(decadeRawData[v])
//     };
//   };
// };


//dummy chart
const data = {
  labels: songFeatures,
  datasets: [{
    label: 'songs',
    data: [1,2,3,4,5,6],
    fill: true,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgb(255, 99, 132)',
    pointBackgroundColor: 'rgb(255, 99, 132)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(255, 99, 132)'
  }, {
    label: 'Decade Name',
    data: [5,3,2,1,2,3],
    fill: true,
    backgroundColor: 'rgba(54, 162, 235, 0.2)',
    borderColor: 'rgb(54, 162, 235)',
    pointBackgroundColor: 'rgb(54, 162, 235)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(54, 162, 235)'
  }]
};

var config = {
  type: 'radar',
  data: data,
  options: {
    elements: {
      line: {
        borderWidth: 3
      }
    }
  },
};
var radarChart = new Chart(canvasElement, config);


// function chartCreate (decadeInit){
  
// }

//13 features selection box selection

// textboxes to select values for features you care sbout with the values you care about

//initializing charts right off the bat so it is there when page loads
// function init() {
//   // d3.json(url).then(function (data) {
//   //     chartCreate(data[0].spot);
//   // })
//   chartCreate(setSelectedIndex(document.querySelector("#greet"),1));
// };
// init();