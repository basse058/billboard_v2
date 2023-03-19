// Store arrays for each feature (median value ordered by year)
let years = featuresByYear['year'];
let danceability = featuresByYear['danceability'];
let energy = featuresByYear['energy'];
let loudness = featuresByYear['loudness'];
let speechiness = featuresByYear['speechiness'];
let acousticness = featuresByYear['acousticness'];
let instrumentalness = featuresByYear['instrumentalness'];
let liveness = featuresByYear['liveness'];
let valence = featuresByYear['valence'];
let tempo = featuresByYear['tempo'];
let duration_ms = featuresByYear['duration_ms'];

let featuresCanvas = document.getElementById("featuresChart");

let danceabilityData = {
    label: "Danceability",
    data: danceability,
    lineTension: 0,
    fill: false
    // borderColor: 'red'
};

let energyData = {
    label: "Energy",
    data: energy,
    lineTension: 0,
    fill: false
    // borderColor: 'blue'
};

let loudnessData = {
    label: "Loudness",
    data: loudness,
    lineTension: 0,
    fill: false
    // borderColor: 'blue'
};

let speechinessData = {
    label: "Speechiness",
    data: speechiness,
    lineTension: 0,
    fill: false
    // borderColor: 'blue'
};

let acousticnessData = {
    label: "Acousticness",
    data: acousticness,
    lineTension: 0,
    fill: false
    // borderColor: 'blue'
};
  
let livenessData = {
    label: "Liveness",
    data: liveness,
    lineTension: 0,
    fill: false
    // borderColor: 'blue'
};

let featuresYearlyData = {
    labels: years,
    datasets: [danceabilityData, energyData, loudnessData, 
        speechinessData, acousticnessData, livenessData]
  };

let chartOptions = {
legend: {
    display: true,
    position: 'top',
    labels: {
        boxWidth: 80,
        fontColor: 'black'
    }
}
};

let lineChart = new Chart(featuresCanvas, {
    type: 'line',
    data: featuresYearlyData,
    options: chartOptions
});