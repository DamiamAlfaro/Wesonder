
// Initialize the map
let x = 32.562698
let y = -117.07699
var map = L.map('map').setView([x, y], 15);

// Add a tile layer to add to our map, in this case it's OpenStreetMap.
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var marker = L.marker([x,y]).addTo(map);
marker.bindPopup("Name: Subcontractor X<br> PhoneNumber: 666-000-999 <br> License: C12, C32, A");


