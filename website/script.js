
// THIS IS FOR THE SHOWING OF ONLY THE MARKERS, 
// BUT IF YOU SHOW THEM ALL, THE BROWSER BECOMES
// QUITE SLOW.

// // Create the map and set the initial view to some coordinates (adjust as needed)
// var map = L.map('map').setView([37.7749, -122.4194], 10);  // Starting position (San Francisco)

// // Add the tile layer (background map)
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// // Fetch the CSV file
// fetch('https://storage.googleapis.com/wesonder_databases/geolocations_dir_entities/dir_entities_geolocations.csv')
//   .then(response => response.text())  // Convert the response to text (CSV format)
//   .then(csvText => {
//     // Use PapaParse to parse the CSV data
//     Papa.parse(csvText, {
//       header: true,  // Treat the first row as headers
//       complete: function(results) {
//         // Access the parsed CSV data (results.data is an array of objects)
//         const data = results.data;

//         // Get the first 50 rows with X_Coordinate and Y_Coordinate
//         const first50Coordinates = data.slice(0, 400).map(row => {
//           return {
//             lng: parseFloat(row['Y_Coordinate']),
//             lat: parseFloat(row['X_Coordinate'])
//           };
//         });

//         console.log(first50Coordinates)

//         // Plot each coordinate on the map
//         first50Coordinates.forEach(coord => {
//           if (!isNaN(coord.lat) && !isNaN(coord.lng)) {
//             L.marker([coord.lat, coord.lng]).addTo(map)
//               .bindPopup(`Latitude: ${coord.lat}, Longitude: ${coord.lng}`);
//           }
//         });
//       },
//       error: function(error) {
//         console.error('Error parsing CSV:', error);
//       }
//     });
//   })
//   .catch(error => console.error('Error fetching CSV:', error));


// Create the map (starting with a wide zoom level)
var map = L.map('map').setView([37.7749, -122.4194], 2);  // Global view

// Add the tile layer (background map)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Create a MarkerClusterGroup for clustering
var markers = L.markerClusterGroup();

// Fetch the CSV file
fetch('https://storage.googleapis.com/wesonder_databases/geolocations_dir_entities/dir_entities_geolocations.csv')
  .then(response => response.text())  // Convert the response to text (CSV format)
  .then(csvText => {
    // Use PapaParse to parse the CSV data
    Papa.parse(csvText, {
      header: true,  // Treat the first row as headers
      complete: function(results) {
        // Access the parsed CSV data (results.data is an array of objects)
        const data = results.data;

        // Get the first 1000 rows and map lat to X_Coordinate and lng to Y_Coordinate
        const first1000Coordinates = data.slice(0, 4000).map(row => {
          return {
            lat: parseFloat(row['X_Coordinate']),  // Latitude comes from X_Coordinate
            lng: parseFloat(row['Y_Coordinate'])   // Longitude comes from Y_Coordinate
          };
        });

        // Filter valid coordinates
        const validCoordinates = first1000Coordinates.filter(coord => {
          return !isNaN(coord.lat) && !isNaN(coord.lng) && 
                 coord.lat >= -90 && coord.lat <= 90 &&
                 coord.lng >= -180 && coord.lng <= 180;
        });

        console.log(validCoordinates.length);  // Log the number of valid coordinates

        // Plot each valid coordinate on the map using clustering
        validCoordinates.forEach(coord => {
          var marker = L.marker([coord.lat, coord.lng]);
          markers.addLayer(marker);  // Add marker to the cluster group
        });

        // Add the marker cluster group to the map
        map.addLayer(markers);
      },
      error: function(error) {
        console.error('Error parsing CSV:', error);
      }
    });
  })
  .catch(error => console.error('Error fetching CSV:', error));

