function initMap(locations) {

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.71274, lng: -74.005974 },
    zoom: 10,
  });

  const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  
  const markers = locations.map((location, i) => {
    return new google.maps.Marker({
      position: {lat:Number(location.lat), lng:Number(location.lng)},
      label: labels[i % labels.length],
    });
  });

  // Add a marker clusterer to manage the markers.
  new MarkerClusterer(map, markers, {
    imagePath:
      "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
  });
  
  
  
}