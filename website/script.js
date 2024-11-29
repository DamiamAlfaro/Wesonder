var map = L.map('map').setView([37.7749, -122.4194], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var markers = L.markerClusterGroup({
    disableClusteringAtZoom: 15
});

map.addLayer(markers)