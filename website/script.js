// // Create the map (starting with a wide zoom level)
// var map = L.map('map').setView([37.7749, -122.4194], 2);  // Global view

// // Add the tile layer (background map)
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// // Create a MarkerClusterGroup for clustering and stop clustering at zoom level 12 (example)
// var markers = L.markerClusterGroup({
//     disableClusteringAtZoom: 13  // Disable clustering at zoom level 13
// });

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

//         // Filter the rows where 'EntityType' equals "Awarding Body Type" and 'EntityState' equals "CA"
//         const filteredData = data.filter(row => 
//           row['EntityType'] === 'Awarding Body\nType' && row['EntityState'] === 'CA'
//         );

//         // Get up to 1000 rows and map lat to X_Coordinate and lng to Y_Coordinate
//         const first1000Coordinates = filteredData.slice(0, 100000).map(row => {
//           return {
//             lat: parseFloat(row['X_Coordinate']),  // Latitude comes from X_Coordinate
//             lng: parseFloat(row['Y_Coordinate']),  // Longitude comes from Y_Coordinate
//             name: row['EntityName'],               // EntityName
//             address: row['FullAddress'],           // FullAddress
//             email: row['EntityEmail'],             // EntityEmail
//             x: row['X_Coordinate'],                // X_Coordinate
//             y: row['Y_Coordinate']                 // Y_Coordinate
//           };
//         });

//         // Filter valid coordinates
//         const validCoordinates = first1000Coordinates.filter(coord => {
//           return !isNaN(coord.lat) && !isNaN(coord.lng) && 
//                  coord.lat >= -90 && coord.lat <= 90 &&
//                  coord.lng >= -180 && coord.lng <= 180;
//         });

//         console.log(validCoordinates.length);  // Log the number of valid coordinates

//         // Plot each valid coordinate on the map using clustering and add popups
//         validCoordinates.forEach(coord => {
//           var marker = L.marker([coord.lat, coord.lng]);

//           // Create the popup content with the respective data
//           var popupContent = `
//             <strong>Entity Name:</strong> ${coord.name || 'N/A'}<br/>
//             <strong>Full Address:</strong> ${coord.address || 'N/A'}<br/>
//             <strong>Email:</strong> ${coord.email || 'N/A'}<br/>
//             <strong>X Coordinate:</strong> ${coord.x}<br/>
//             <strong>Y Coordinate:</strong> ${coord.y}
//           `;

//           // Bind the popup to the marker
//           marker.bindPopup(popupContent);

//           // Add marker to the cluster group
//           markers.addLayer(marker);
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


// Initialize the map
var map = L.map('map').setView([37.7749, -122.4194], 2);

// Add the tile layer (background map)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Global marker cluster variable
var markers;

// Function to load data from a CSV file
function loadData(dataset) {
    // Remove previous markers from the map if any
    if (markers) {
        map.removeLayer(markers);
    }

    // Create a new marker cluster group
    markers = L.markerClusterGroup({
        disableClusteringAtZoom: 12  // Disable clustering at zoom level 12
    });

    // Determine which CSV file to load based on the dataset
    var csvUrl;
    if (dataset === 'csv1') {
        csvUrl = 'https://storage.googleapis.com/wesonder_databases/geolocations_dir_entities/dir_entities_geolocations.csv'; // Replace with actual CSV URL
    } else if (dataset === 'csv2') {
        csvUrl = 'https://storage.googleapis.com/wesonder_databases/geolocations_cslb/cslb_contractors_geolocation.csv'; // Replace with actual CSV URL
    }

    // Fetch the CSV file
    fetch(csvUrl)
        .then(response => response.text())
        .then(csvText => {
            // Parse the CSV file
            Papa.parse(csvText, {
                header: true,
                complete: function(results) {
                    // Access parsed data
                    const data = results.data;

                    // Check which dataset is loaded
                    if (dataset === 'csv1') {
                        // For the first CSV, filter by "CA" in State and Zip starting with 9
                        const validCoordinates = data.filter(row => 
                            !isNaN(parseFloat(row['X_Coordinate'])) &&
                            !isNaN(parseFloat(row['Y_Coordinate'])) &&
                            row['EntityType'] === 'Awarding Body\nType' &&
                            row['EntityState'] === 'CA'
                        ).map(row => {
                            return {
                                lat: parseFloat(row['X_Coordinate']),
                                lng: parseFloat(row['Y_Coordinate']),
                                name: row['EntityName'],
                                address: row['FullAddress'],
                                email: row['EntityEmail'],
                                x: row['X_Coordinate'],
                                y: row['Y_Coordinate']
                            };
                        });

                        // Add markers to the cluster group
                        validCoordinates.forEach(coord => {
                            var marker = L.marker([coord.lat, coord.lng]);
                            marker.bindPopup(`
                                <strong>Entity Name:</strong> ${coord.name || 'N/A'}<br/>
                                <strong>Full Address:</strong> ${coord.address || 'N/A'}<br/>
                                <strong>Email:</strong> ${coord.email || 'N/A'}<br/>
                                <strong>X Coordinate:</strong> ${coord.x}<br/>
                                <strong>Y Coordinate:</strong> ${coord.y}
                            `);
                            markers.addLayer(marker);
                        });

                    } else if (dataset === 'csv2') {
                        // For the second CSV, filter by "CA" in State and Zip starting with 9
                        const validCoordinates = data.filter(row => 
                            !isNaN(parseFloat(row['X_Coordinate'])) &&
                            !isNaN(parseFloat(row['Y_Coordinate'])) &&
                            row['State'] === 'CA' &&
                            row['Zip'] && row['Zip'].startsWith('9')
                        ).map(row => {
                            return {
                                lat: parseFloat(row['X_Coordinate']),
                                lng: parseFloat(row['Y_Coordinate']),
                                name: row['BusinessName'],
                                address: row['CompleteAddress'],
                                phone: row['PhoneNumber'],
                                license: row['LicenseNumber'],
                                businessType: row['BusinessType'],
                                x: row['X_Coordinate'],
                                y: row['Y_Coordinate']
                            };
                        });

                        // Add markers to the cluster group
                        validCoordinates.forEach(coord => {
                            var marker = L.marker([coord.lat, coord.lng]);
                            marker.bindPopup(`
                                <strong>Business Name:</strong> ${coord.name || 'N/A'}<br/>
                                <strong>Complete Address:</strong> ${coord.address || 'N/A'}<br/>
                                <strong>Phone Number:</strong> ${coord.phone || 'N/A'}<br/>
                                <strong>License Number:</strong> ${coord.license || 'N/A'}<br/>
                                <strong>Business Type:</strong> ${coord.businessType || 'N/A'}<br/>
                                <strong>X Coordinate:</strong> ${coord.x}<br/>
                                <strong>Y Coordinate:</strong> ${coord.y}
                            `);
                            markers.addLayer(marker);
                        });
                    }

                    // Add the markers to the map
                    map.addLayer(markers);
                }
            });
        })
        .catch(error => console.error('Error fetching CSV:', error));
}



