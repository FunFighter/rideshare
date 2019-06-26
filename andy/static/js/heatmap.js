var myMap = L.map("map", {
  center: [30.26759, -97.74299],
  zoom: 13
});

L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

var url = "data/austin.geojson";

// Importing local data
// var data = fetchJSON('austin.geojson')
  //          .then(function(data) { return data })




d3.json(url, function(response) {

  console.log(response);

  var heatArray = [];
  var features = response.features
  console.log(features)
  for (var i = 0; i < features.length; i++) {
    var location = features[i];
    // console.log(response)
    if (location.geometry) {
      var geometry = location.geometry
      heatArray.push([geometry.coordinates[1], geometry.coordinates[0]]);
    }
  }
  console.log(heatArray)
  var heat = L.heatLayer(heatArray, {
    radius: 40,
    blur: 55
  }).addTo(myMap);

});
