// // Initialize the map
// var map = L.map('map').setView([37.7749, -122.4194], 2);

// // Add the tile layer (background map)
// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

// // Global marker cluster variable
// var markers;

// // Function to load data from a CSV file
// function loadData(dataset) {
//     // Remove previous markers from the map if any
//     if (markers) {
//         map.removeLayer(markers);
//     }

//     // Create a new marker cluster group
//     markers = L.markerClusterGroup({
//         disableClusteringAtZoom: 16  // Disable clustering at zoom level 12
//     });

//     // Determine which CSV file to load based on the dataset
//     var csvUrl;
//     if (dataset === 'csv1') {
//         csvUrl = 'https://storage.googleapis.com/wesonder_databases/geolocations_dir_entities/dir_entities_geolocations.csv'; // Replace with actual CSV URL
//     } else if (dataset === 'csv2') {
//         csvUrl = 'https://storage.googleapis.com/wesonder_databases/geolocations_cslb/cslb_contractors_geolocation.csv'; // Replace with actual CSV URL
//     }

//     // Fetch the CSV file
//     fetch(csvUrl)
//         .then(response => response.text())
//         .then(csvText => {
//             // Parse the CSV file
//             Papa.parse(csvText, {
//                 header: true,
//                 complete: function(results) {
//                     // Access parsed data
//                     const data = results.data;

//                     // Check which dataset is loaded
//                     if (dataset === 'csv1') {
//                         // For the first CSV, filter by "CA" in State and Zip starting with 9
//                         const validCoordinates = data.filter(row => 
//                             !isNaN(parseFloat(row['X_Coordinate'])) &&
//                             !isNaN(parseFloat(row['Y_Coordinate'])) &&
//                             row['EntityType'] === 'Awarding Body\nType' &&
//                             row['EntityState'] === 'CA'
//                         ).map(row => {
//                             return {
//                                 lat: parseFloat(row['X_Coordinate']),
//                                 lng: parseFloat(row['Y_Coordinate']),
//                                 name: row['EntityName'],
//                                 address: row['FullAddress'],
//                                 email: row['EntityEmail'],
//                                 x: row['X_Coordinate'],
//                                 y: row['Y_Coordinate']
//                             };
//                         });

//                         // Add markers to the cluster group
//                         validCoordinates.forEach(coord => {
//                             var marker = L.marker([coord.lat, coord.lng]);
//                             marker.bindPopup(`
//                                 <strong>Entity Name:</strong> ${coord.name || 'N/A'}<br/>
//                                 <strong>Full Address:</strong> ${coord.address || 'N/A'}<br/>
//                                 <strong>Email:</strong> ${coord.email || 'N/A'}<br/>
//                                 <strong>X Coordinate:</strong> ${coord.x}<br/>
//                                 <strong>Y Coordinate:</strong> ${coord.y}
//                             `);
//                             markers.addLayer(marker);
//                         });

//                     } else if (dataset === 'csv2') {
//                         // For the second CSV, filter by "CA" in State and Zip starting with 9
//                         const validCoordinates = data.filter(row => 
//                             !isNaN(parseFloat(row['X_Coordinate'])) &&
//                             !isNaN(parseFloat(row['Y_Coordinate'])) &&
//                             row['State'] === 'CA' &&
//                             row['Zip'] && row['Zip'].startsWith('9')
//                         ).map(row => {
//                             return {
//                                 lat: parseFloat(row['X_Coordinate']),
//                                 lng: parseFloat(row['Y_Coordinate']),
//                                 name: row['BusinessName'],
//                                 address: row['CompleteAddress'],
//                                 phone: row['PhoneNumber'],
//                                 license: row['LicenseNumber'],
//                                 businessType: row['BusinessType'],
//                                 x: row['X_Coordinate'],
//                                 y: row['Y_Coordinate']
//                             };
//                         });

//                         // Add markers to the cluster group
//                         validCoordinates.forEach(coord => {
//                             var marker = L.marker([coord.lat, coord.lng]);
//                             marker.bindPopup(`
//                                 <strong>Business Name:</strong> ${coord.name || 'N/A'}<br/>
//                                 <strong>Complete Address:</strong> ${coord.address || 'N/A'}<br/>
//                                 <strong>Phone Number:</strong> ${coord.phone || 'N/A'}<br/>
//                                 <strong>License Number:</strong> ${coord.license || 'N/A'}<br/>
//                                 <strong>Business Type:</strong> ${coord.businessType || 'N/A'}<br/>
//                                 <strong>X Coordinate:</strong> ${coord.x}<br/>
//                                 <strong>Y Coordinate:</strong> ${coord.y}
//                             `);
//                             markers.addLayer(marker);
//                         });
//                     }

//                     // Add the markers to the map
//                     map.addLayer(markers);
//                 }
//             });
//         })
//         .catch(error => console.error('Error fetching CSV:', error));
// }



// Initialize the map
var map = L.map('map').setView([37.7749, -122.4194], 5);

// Add the tile layer (background map)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Global marker cluster variable
var markers = L.markerClusterGroup({
    disableClusteringAtZoom: 16
});

map.addLayer(markers); // Add empty cluster group to the map initially

// Create a custom control for filtering CSV2 options
var filterControl = L.control({position: 'topright'});
filterControl.onAdd = function(map) {
    var div = L.DomUtil.create('div', 'filter-box hidden');
    div.id = 'filterBox';
    div.innerHTML = `
        <strong>Select License Types:</strong><br/>
        <input type="checkbox" value="C-2" id="C2" onchange="filterByLicense()"> C-2 - Insulation and Acoustical Contractor<br/>
        <input type="checkbox" value="C-4" id="C4" onchange="filterByLicense()"> C-4 - Boiler, Hot Water Heating and Steam Fitting Contractor<br/>
        <input type="checkbox" value="C-5" id="C5" onchange="filterByLicense()"> C-5 - Framing and Rough Carpentry Contractor<br/>
        <input type="checkbox" value="C-6" id="C6" onchange="filterByLicense()"> C-6 - Cabinet, Millwork and Finish Carpentry Contractor<br/>
        <input type="checkbox" value="C-7" id="C7" onchange="filterByLicense()"> C-7 - Low Voltage Systems Contractor<br/>
        <input type="checkbox" value="C-8" id="C8" onchange="filterByLicense()"> C-8 - Concrete Contractor<br/>
        <input type="checkbox" value="C-9" id="C9" onchange="filterByLicense()"> C-9 - Drywall Contractor<br/>
        <input type="checkbox" value="C-10" id="C10" onchange="filterByLicense()"> C-10 - Electrical Contractor<br/>
        <input type="checkbox" value="C-11" id="C11" onchange="filterByLicense()"> C-11 - Elevator Contractor<br/>
        <input type="checkbox" value="C-12" id="C12" onchange="filterByLicense()"> C-12 - Earthwork and Paving Contractors<br/>
        <input type="checkbox" value="C-13" id="C13" onchange="filterByLicense()"> C-13 - Fencing Contractor<br/>
        <input type="checkbox" value="C-15" id="C15" onchange="filterByLicense()"> C-15 - Flooring and Floor Covering Contractors<br/>
        <input type="checkbox" value="C-16" id="C16" onchange="filterByLicense()"> C-16 - Fire Protection Contractor<br/>
        <input type="checkbox" value="C-17" id="C17" onchange="filterByLicense()"> C-17 - Glazing Contractor<br/>
        <input type="checkbox" value="C-20" id="C20" onchange="filterByLicense()"> C-20 - Warm-Air Heating, Ventilating and Air-Conditioning Contractor<br/>
        <input type="checkbox" value="C-21" id="C21" onchange="filterByLicense()"> C-21 - Building Moving/Demolition Contractor<br/>
        <input type="checkbox" value="C-22" id="C22" onchange="filterByLicense()"> C-22 - Asbestos Abatement Contractor<br/>
        <input type="checkbox" value="C-23" id="C23" onchange="filterByLicense()"> C-23 - Ornamental Metal Contractor<br/>
        <input type="checkbox" value="C-27" id="C27" onchange="filterByLicense()"> C-27 - Landscaping Contractor<br/>
        <input type="checkbox" value="C-28" id="C28" onchange="filterByLicense()"> C-28 - Lock and Security Equipment Contractor<br/>
        <input type="checkbox" value="C-29" id="C29" onchange="filterByLicense()"> C-29 - Masonry Contractor<br/>
        <input type="checkbox" value="C-31" id="C31" onchange="filterByLicense()"> C-31 - Construction Zone Traffic Control Contractor<br/>
        <input type="checkbox" value="C-32" id="C32" onchange="filterByLicense()"> C-32 - Parking and Highway Improvement Contractor<br/>
        <input type="checkbox" value="C-33" id="C33" onchange="filterByLicense()"> C-33 - Painting and Decorating Contractor<br/>
        <input type="checkbox" value="C-34" id="C34" onchange="filterByLicense()"> C-34 - Pipeline Contractor<br/>
        <input type="checkbox" value="C-35" id="C35" onchange="filterByLicense()"> C-35 - Lathing and Plastering Contractor<br/>
        <input type="checkbox" value="C-36" id="C36" onchange="filterByLicense()"> C-36 - Plumbing Contractor<br/>
        <input type="checkbox" value="C-38" id="C38" onchange="filterByLicense()"> C-38 - Refrigeration Contractor<br/>
        <input type="checkbox" value="C-39" id="C39" onchange="filterByLicense()"> C-39 - Roofing Contractor<br/>
        <input type="checkbox" value="C-42" id="C42" onchange="filterByLicense()"> C-42 - Sanitation System Contractor<br/>
        <input type="checkbox" value="C-43" id="C43" onchange="filterByLicense()"> C-43 - Sheet Metal Contractor<br/>
        <input type="checkbox" value="C-45" id="C45" onchange="filterByLicense()"> C-45 - Sign Contractor<br/>
        <input type="checkbox" value="C-46" id="C46" onchange="filterByLicense()"> C-46 - Solar Contractor<br/>
        <input type="checkbox" value="C-47" id="C47" onchange="filterByLicense()"> C-47 - General Manufactured Housing Contractor<br/>
        <input type="checkbox" value="C-49" id="C49" onchange="filterByLicense()"> C-49 - Tree and Palm Contractor<br/>
        <input type="checkbox" value="C-50" id="C50" onchange="filterByLicense()"> C-50 - Reinforcing Steel Contractor<br/>
        <input type="checkbox" value="C-51" id="C51" onchange="filterByLicense()"> C-51 - Structural Steel Contractor<br/>
        <input type="checkbox" value="C-53" id="C53" onchange="filterByLicense()"> C-53 - Swimming Pool Contractor<br/>
        <input type="checkbox" value="C-54" id="C54" onchange="filterByLicense()"> C-54 - Ceramic and Mosaic Tile Contractor<br/>
        <input type="checkbox" value="C-55" id="C55" onchange="filterByLicense()"> C-55 - Water Conditioning Contractor<br/>
        <input type="checkbox" value="C-57" id="C57" onchange="filterByLicense()"> C-57 - Well Drilling Contractor<br/>
        <input type="checkbox" value="C-60" id="C60" onchange="filterByLicense()"> C-60 - Welding Contractor<br/>
        <input type="checkbox" value="D-1" id="D1" onchange="filterByLicense()"> D-1 - Architectural Porcelain<br/>
        <input type="checkbox" value="D-2" id="D2" onchange="filterByLicense()"> D-2 - Asbestos Fabrication<br/>
        <input type="checkbox" value="D-3" id="D3" onchange="filterByLicense()"> D-3 - Awnings<br/>
        <input type="checkbox" value="D-4" id="D4" onchange="filterByLicense()"> D-4 - Central Vacuum Systems<br/>
        <input type="checkbox" value="D-5" id="D5" onchange="filterByLicense()"> D-5 - Communication Equipment<br/>
        <input type="checkbox" value="D-6" id="D6" onchange="filterByLicense()"> D-6 - Concrete Related Services<br/>
        <input type="checkbox" value="D-7" id="D7" onchange="filterByLicense()"> D-7 - Conveyors-Cranes<br/>
        <input type="checkbox" value="D-8" id="D8" onchange="filterByLicense()"> D-8 - Doors and Door Services<br/>
        <input type="checkbox" value="D-9" id="D9" onchange="filterByLicense()"> D-9 - Drilling, Blasting and Oil Field Work<br/>
        <input type="checkbox" value="D-10" id="D10" onchange="filterByLicense()"> D-10 - Elevated Floors<br/>
        <input type="checkbox" value="D-11" id="D11" onchange="filterByLicense()"> D-11 - Fencing<br/>
        <input type="checkbox" value="D-12" id="D12" onchange="filterByLicense()"> D-12 - Synthetic Products<br/>
        <input type="checkbox" value="D-13" id="D13" onchange="filterByLicense()"> D-13 - Fire Extinguisher Systems<br/>
        <input type="checkbox" value="D-14" id="D14" onchange="filterByLicense()"> D-14 - Floor Covering<br/>
        <input type="checkbox" value="D-15" id="D15" onchange="filterByLicense()"> D-15 - Furnaces<br/>
        <input type="checkbox" value="D-16" id="D16" onchange="filterByLicense()"> D-16 - Hardware, Locks and Safes<br/>
        <input type="checkbox" value="D-17" id="D17" onchange="filterByLicense()"> D-17 - Industrial Insulation<br/>
        <input type="checkbox" value="D-18" id="D18" onchange="filterByLicense()"> D-18 - Prison and Jail Equipment<br/>
        <input type="checkbox" value="D-19" id="D19" onchange="filterByLicense()"> D-19 - Land Clearing<br/>
        <input type="checkbox" value="D-20" id="D20" onchange="filterByLicense()"> D-20 - Lead Burning and Fabrication<br/>
        <input type="checkbox" value="D-21" id="D21" onchange="filterByLicense()"> D-21 - Machinery and Pumps<br/>
        <input type="checkbox" value="D-22" id="D22" onchange="filterByLicense()"> D-22 - Marble<br/>
        <input type="checkbox" value="D-23" id="D23" onchange="filterByLicense()"> D-23 - Medical Gas Systems<br/>
        <input type="checkbox" value="D-24" id="D24" onchange="filterByLicense()"> D-24 - Metal Products<br/>
        <input type="checkbox" value="D-25" id="D25" onchange="filterByLicense()"> D-25 - Mirrors and Fixed Glass<br/>
        <input type="checkbox" value="D-26" id="D26" onchange="filterByLicense()"> D-26 - Mobile Home Installation and Repairs<br/>
        <input type="checkbox" value="D-27" id="D27" onchange="filterByLicense()"> D-27 - Movable Partitions<br/>
        <input type="checkbox" value="D-28" id="D28" onchange="filterByLicense()"> D-28 - Doors, Gates and Activating Devices<br/>
        <input type="checkbox" value="D-29" id="D29" onchange="filterByLicense()"> D-29 - Paperhanging<br/>
        <input type="checkbox" value="D-30" id="D30" onchange="filterByLicense()"> D-30 - Pile Driving and Pressure Foundation Jacking<br/>
        <input type="checkbox" value="D-31" id="D31" onchange="filterByLicense()"> D-31 - Pole Installation and Maintenance<br/>
        <input type="checkbox" value="D-32" id="D32" onchange="filterByLicense()"> D-32 - Power Nailing and Fastening<br/>
        <input type="checkbox" value="D-33" id="D33" onchange="filterByLicense()"> D-33 - Precast Concrete Stairs<br/>
        <input type="checkbox" value="D-34" id="D34" onchange="filterByLicense()"> D-34 - Prefabricated Equipment<br/>
        <input type="checkbox" value="D-35" id="D35" onchange="filterByLicense()"> D-35 - Pool and Spa Maintenance<br/>
        <input type="checkbox" value="D-36" id="D36" onchange="filterByLicense()"> D-36 - Rigging and Rig Building<br/>
        <input type="checkbox" value="D-37" id="D37" onchange="filterByLicense()"> D-37 - Safes and Vaults<br/>
        <input type="checkbox" value="D-38" id="D38" onchange="filterByLicense()"> D-38 - Sand and Water Blasting<br/>
        <input type="checkbox" value="D-39" id="D39" onchange="filterByLicense()"> D-39 - Scaffolding<br/>
        <input type="checkbox" value="D-40" id="D40" onchange="filterByLicense()"> D-40 - Service Station Equipment and Maintenance<br/>
        <input type="checkbox" value="D-41" id="D41" onchange="filterByLicense()"> D-41 - Siding and Decking<br/>
        <input type="checkbox" value="D-42" id="D42" onchange="filterByLicense()"> D-42 - Non-Electrical Sign Installation<br/>
        <input type="checkbox" value="D-43" id="D43" onchange="filterByLicense()"> D-43 - Soil Grouting<br/>
        <input type="checkbox" value="D-44" id="D44" onchange="filterByLicense()"> D-44 - Sprinklers<br/>
        <input type="checkbox" value="D-45" id="D45" onchange="filterByLicense()"> D-45 - Staff and Stone<br/>
        <input type="checkbox" value="D-46" id="D46" onchange="filterByLicense()"> D-46 - Steeple Jack Work<br/>
        <input type="checkbox" value="D-47" id="D47" onchange="filterByLicense()"> D-47 - Tennis Court Surfacing<br/>
        <input type="checkbox" value="D-48" id="D48" onchange="filterByLicense()"> D-48 - Theater and School Equipment<br/>
        <input type="checkbox" value="D-49" id="D49" onchange="filterByLicense()"> D-49 - Tree Service<br/>
        <input type="checkbox" value="D-50" id="D50" onchange="filterByLicense()"> D-50 - Suspended Ceilings<br/>
        <input type="checkbox" value="D-51" id="D51" onchange="filterByLicense()"> D-51 - Waterproofing and Weatherproofing<br/>
        <input type="checkbox" value="D-52" id="D52" onchange="filterByLicense()"> D-52 - Window Coverings<br/>
        <input type="checkbox" value="D-53" id="D53" onchange="filterByLicense()"> D-53 - Wood Tanks<br/>
        <input type="checkbox" value="D-54" id="D54" onchange="filterByLicense()"> D-54 - Rockscaping<br/>
        <input type="checkbox" value="D-55" id="D55" onchange="filterByLicense()"> D-55 - Blasting<br/>
        <input type="checkbox" value="D-56" id="D56" onchange="filterByLicense()"> D-56 - Trenching Only<br/>
        <input type="checkbox" value="D-57" id="D57" onchange="filterByLicense()"> D-57 - Propane Gas Plants<br/>
        <input type="checkbox" value="D-58" id="D58" onchange="filterByLicense()"> D-58 - Residential Floating Docks<br/>
        <input type="checkbox" value="D-59" id="D59" onchange="filterByLicense()"> D-59 - Hydroseed Spraying<br/>
        <input type="checkbox" value="D-60" id="D60" onchange="filterByLicense()"> D-60 - Striping<br/>
        <input type="checkbox" value="D-61" id="D61" onchange="filterByLicense()"> D-61 - Gold Leaf Gilding<br/>
        <input type="checkbox" value="D-62" id="D62" onchange="filterByLicense()"> D-62 - Air and Water Balancing<br/>
        <input type="checkbox" value="D-63" id="D63" onchange="filterByLicense()"> D-63 - Construction Clean-up<br/>
        <input type="checkbox" value="D-64" id="D64" onchange="filterByLicense()"> D-64 - Non-specialized<br/>
        <input type="checkbox" value="D-65" id="D65" onchange="filterByLicense()"> D-65 - Weatherization and Energy Conservation<br/>
    `;
    return div;
};
filterControl.addTo(map);

// Global variables to store data and selected licenses
var dataCache = [];
var selectedLicenses = [];
var currentDataset = 'csv1'; // Keep track of which dataset is active

// Function to load data based on dataset selection
function loadData(dataset) {
    currentDataset = dataset;

    // Show filter options only for csv2
    var filterBox = document.getElementById('filterBox');
    if (dataset === 'csv2') {
        filterBox.classList.remove('hidden');
    } else {
        filterBox.classList.add('hidden');
    }

    markers.clearLayers(); // Clear existing markers

    if (dataset === 'csv1') {
        loadCSV1Data();
    } else if (dataset === 'csv2') {
        loadCSV2Data();
    }
}

// Function to load CSV1 data (no filtering)
function loadCSV1Data() {
    var csvUrl = 'https://storage.googleapis.com/wesonder_databases/geolocations_dir_entities/dir_entities_geolocations.csv'; // Replace with actual URL

    fetch(csvUrl)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: function(results) {
                    var data = results.data;

                    // Filter and display markers for CSV1
                    var validCoordinates = data.filter(row => 
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
                            email: row['EntityEmail']
                        };
                    });

                    // Add markers to the map for CSV1
                    validCoordinates.forEach(coord => {
                        var marker = L.marker([coord.lat, coord.lng]);
                        marker.bindPopup(`
                            <strong>Entity Name:</strong> ${coord.name || 'N/A'}<br/>
                            <strong>Full Address:</strong> ${coord.address || 'N/A'}<br/>
                            <strong>Email:</strong> ${coord.email || 'N/A'}
                        `);
                        markers.addLayer(marker);
                    });
                }
            });
        })
        .catch(error => console.error('Error fetching CSV1:', error));
}

// Function to load CSV2 data
function loadCSV2Data() {
    var csvUrl = 'https://storage.googleapis.com/wesonder_databases/geolocations_cslb/cslb_contractors_geolocation.csv'; // Replace with actual URL

    fetch(csvUrl)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: function(results) {
                    dataCache = results.data; // Cache the parsed data for filtering
                    filterByLicense(); // Initially populate the map with all markers
                }
            });
        })
        .catch(error => console.error('Error fetching CSV2:', error));
}

// Function to filter and update markers on the map for CSV2
function filterByLicense() {
    // Get selected checkboxes
    var checkboxes = document.querySelectorAll('.filter-box input[type="checkbox"]:checked');
    selectedLicenses = Array.from(checkboxes).map(checkbox => checkbox.value);

    // Clear existing markers
    markers.clearLayers();

    // Filter the cached data based on selected licenses
    var filteredData = dataCache.filter(row => {
        const classification = (row['Classification'] || '').replace(/-/g, '');
        return selectedLicenses.some(license => classification.includes(license.replace('-', '')));
    });

    // Add filtered markers to the map
    filteredData.forEach(coord => {
        if (!isNaN(parseFloat(coord['X_Coordinate'])) && !isNaN(parseFloat(coord['Y_Coordinate']))) {
            var marker = L.marker([parseFloat(coord['X_Coordinate']), parseFloat(coord['Y_Coordinate'])]);
            marker.bindPopup(`
                <strong>Business Name:</strong> ${coord['BusinessName'] || 'N/A'}<br/>
                <strong>License Number:</strong> ${coord['LicenseNumber'] || 'N/A'}<br/>
                <strong>Classification:</strong> ${coord['Classification'] || 'N/A'}
            `);
            markers.addLayer(marker);
        }
    });
}






