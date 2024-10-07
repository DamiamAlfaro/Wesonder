
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


// EVERY SINGLE ENTITY, NOT ONLY THE AWARDING BODIES,
// WHICH IS WHAT WE NEED FROM THE DIR

// // Create the map (starting with a wide zoom level)
// var map = L.map('map').setView([37.7749, -122.4194], 2);  // Global view

// // Add the tile layer (background map)
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// // Create a MarkerClusterGroup for clustering
// var markers = L.markerClusterGroup();

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

//         // Get the first 1000 rows and map lat to X_Coordinate and lng to Y_Coordinate
//         const first1000Coordinates = data.slice(0, 100000).map(row => {
//           return {
//             lat: parseFloat(row['X_Coordinate']),  // Latitude comes from X_Coordinate
//             lng: parseFloat(row['Y_Coordinate'])   // Longitude comes from Y_Coordinate
//           };
//         });

//         // Filter valid coordinates
//         const validCoordinates = first1000Coordinates.filter(coord => {
//           return !isNaN(coord.lat) && !isNaN(coord.lng) && 
//                  coord.lat >= -90 && coord.lat <= 90 &&
//                  coord.lng >= -180 && coord.lng <= 180;
//         });

//         console.log(validCoordinates.length);  // Log the number of valid coordinates

//         // Plot each valid coordinate on the map using clustering
//         validCoordinates.forEach(coord => {
//           var marker = L.marker([coord.lat, coord.lng]);
//           markers.addLayer(marker);  // Add marker to the cluster group
//         });

//         // Add the marker cluster group to the map
//         map.addLayer(markers);
//       },
//       error: function(error) {
//         console.error('Error parsing CSV:', error);
//       }
//     });
//   })
//   .catch(error => console.error('Error fetching CSV:', error));


// DISPLAYING THE AWARDING BODIES, WHICH IS 
// ULTIMATELY THE AIM FOR THIS DATASET FROM THE 
// DIR WEBSITE

// // Create the map (starting with a wide zoom level)
// var map = L.map('map').setView([37.7749, -122.4194], 2);  // Global view

// // Add the tile layer (background map)
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// // Create a MarkerClusterGroup for clustering
// var markers = L.markerClusterGroup();

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

//         // Filter the rows where 'EntityType' equals "Awarding Body Type"
//         const filteredData = data.filter(row => 
//           row['EntityType'] === 'Awarding Body\nType' && row['EntityState'] === "CA"
//           );

//         // Get up to 1000 rows and map lat to X_Coordinate and lng to Y_Coordinate
//         const first1000Coordinates = filteredData.slice(0, 100000).map(row => {
//           return {
//             lat: parseFloat(row['X_Coordinate']),  // Latitude comes from X_Coordinate
//             lng: parseFloat(row['Y_Coordinate'])   // Longitude comes from Y_Coordinate
//           };
//         });

//         // Filter valid coordinates
//         const validCoordinates = first1000Coordinates.filter(coord => {
//           return !isNaN(coord.lat) && !isNaN(coord.lng) && 
//                  coord.lat >= -90 && coord.lat <= 90 &&
//                  coord.lng >= -180 && coord.lng <= 180;
//         });

//         console.log(validCoordinates.length);  // Log the number of valid coordinates

//         // Plot each valid coordinate on the map using clustering
//         validCoordinates.forEach(coord => {
//           var marker = L.marker([coord.lat, coord.lng]);
//           markers.addLayer(marker);  // Add marker to the cluster group
//         });

//         // Add the marker cluster group to the map
//         map.addLayer(markers);
//       },
//       error: function(error) {
//         console.error('Error parsing CSV:', error);
//       }
//     });
//   })
//   .catch(error => console.error('Error fetching CSV:', error));


// DISPLAYING THE AWARDING BODIES, AND THE EMAILS,
// NAMES, COORDINATES, AND ADDRESSES.


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

        // Filter the rows where 'EntityType' equals "Awarding Body Type" and 'EntityState' equals "CA"
        const filteredData = data.filter(row => 
          row['EntityType'] === 'Awarding Body\nType' && row['EntityState'] === 'CA'
        );

        // Get up to 1000 rows and map lat to X_Coordinate and lng to Y_Coordinate
        const first1000Coordinates = filteredData.slice(0, 100000).map(row => {
          return {
            lat: parseFloat(row['X_Coordinate']),  // Latitude comes from X_Coordinate
            lng: parseFloat(row['Y_Coordinate']),  // Longitude comes from Y_Coordinate
            name: row['EntityName'],               // EntityName
            address: row['FullAddress'],           // FullAddress
            email: row['EntityEmail'],             // EntityEmail
            x: row['X_Coordinate'],                // X_Coordinate
            y: row['Y_Coordinate']                 // Y_Coordinate
          };
        });

        // Filter valid coordinates
        const validCoordinates = first1000Coordinates.filter(coord => {
          return !isNaN(coord.lat) && !isNaN(coord.lng) && 
                 coord.lat >= -90 && coord.lat <= 90 &&
                 coord.lng >= -180 && coord.lng <= 180;
        });

        console.log(validCoordinates.length);  // Log the number of valid coordinates

        // Plot each valid coordinate on the map using clustering and add popups
        validCoordinates.forEach(coord => {
          var marker = L.marker([coord.lat, coord.lng]);

          // Create the popup content with the respective data
          var popupContent = `
            <strong>Entity Name:</strong> ${coord.name || 'N/A'}<br/>
            <strong>Full Address:</strong> ${coord.address || 'N/A'}<br/>
            <strong>Email:</strong> ${coord.email || 'N/A'}<br/>
            <strong>X Coordinate:</strong> ${coord.x}<br/>
            <strong>Y Coordinate:</strong> ${coord.y}
          `;

          // Bind the popup to the marker
          marker.bindPopup(popupContent);

          // Add marker to the cluster group
          markers.addLayer(marker);
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
