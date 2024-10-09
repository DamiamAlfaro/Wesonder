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
        <div class="filter-box-content">
            <label><input type="checkbox" id="selectAll" onchange="toggleSelectAll(this)"> Select All<br/></label>
            <label><input type="checkbox" value="C-2" id="C2" onchange="filterByLicense()"> C-2 - Insulation and Acoustical Contractor<br/></label>
            <label><input type="checkbox" value="C-4" id="C4" onchange="filterByLicense()"> C-4 - Boiler, Hot Water Heating and Steam Fitting Contractor<br/></label>
            <label><input type="checkbox" value="C-5" id="C5" onchange="filterByLicense()"> C-5 - Framing and Rough Carpentry Contractor<br/></label>
            <label><input type="checkbox" value="C-6" id="C6" onchange="filterByLicense()"> C-6 - Cabinet, Millwork and Finish Carpentry Contractor<br/></label>
            <label><input type="checkbox" value="C-7" id="C7" onchange="filterByLicense()"> C-7 - Low Voltage Systems Contractor<br/></label>
            <label><input type="checkbox" value="C-8" id="C8" onchange="filterByLicense()"> C-8 - Concrete Contractor<br/></label>
            <label><input type="checkbox" value="C-9" id="C9" onchange="filterByLicense()"> C-9 - Drywall Contractor<br/></label>
            <label><input type="checkbox" value="C-10" id="C10" onchange="filterByLicense()"> C-10 - Electrical Contractor<br/></label>
            <label><input type="checkbox" value="C-11" id="C11" onchange="filterByLicense()"> C-11 - Elevator Contractor<br/></label>
            <label><input type="checkbox" value="C-12" id="C12" onchange="filterByLicense()"> C-12 - Earthwork and Paving Contractors<br/></label>
            <label><input type="checkbox" value="C-13" id="C13" onchange="filterByLicense()"> C-13 - Fencing Contractor<br/></label>
            <label><input type="checkbox" value="C-15" id="C15" onchange="filterByLicense()"> C-15 - Flooring and Floor Covering Contractors<br/></label>
            <label><input type="checkbox" value="C-16" id="C16" onchange="filterByLicense()"> C-16 - Fire Protection Contractor<br/></label>
            <label><input type="checkbox" value="C-17" id="C17" onchange="filterByLicense()"> C-17 - Glazing Contractor<br/></label>
            <label><input type="checkbox" value="C-20" id="C20" onchange="filterByLicense()"> C-20 - Warm-Air Heating, Ventilating and Air-Conditioning Contractor<br/></label>
            <label><input type="checkbox" value="C-21" id="C21" onchange="filterByLicense()"> C-21 - Building Moving/Demolition Contractor<br/></label>
            <label><input type="checkbox" value="C-22" id="C22" onchange="filterByLicense()"> C-22 - Asbestos Abatement Contractor<br/></label>
            <label><input type="checkbox" value="C-23" id="C23" onchange="filterByLicense()"> C-23 - Ornamental Metal Contractor<br/></label>
            <label><input type="checkbox" value="C-27" id="C27" onchange="filterByLicense()"> C-27 - Landscaping Contractor<br/></label>
            <label><input type="checkbox" value="C-28" id="C28" onchange="filterByLicense()"> C-28 - Lock and Security Equipment Contractor<br/></label>
            <label><input type="checkbox" value="C-29" id="C29" onchange="filterByLicense()"> C-29 - Masonry Contractor<br/></label>
            <label><input type="checkbox" value="C-31" id="C31" onchange="filterByLicense()"> C-31 - Construction Zone Traffic Control Contractor<br/></label>
            <label><input type="checkbox" value="C-32" id="C32" onchange="filterByLicense()"> C-32 - Parking and Highway Improvement Contractor<br/></label>
            <label><input type="checkbox" value="C-33" id="C33" onchange="filterByLicense()"> C-33 - Painting and Decorating Contractor<br/></label>
            <label><input type="checkbox" value="C-34" id="C34" onchange="filterByLicense()"> C-34 - Pipeline Contractor<br/></label>
            <label><input type="checkbox" value="C-35" id="C35" onchange="filterByLicense()"> C-35 - Lathing and Plastering Contractor<br/></label>
            <label><input type="checkbox" value="C-36" id="C36" onchange="filterByLicense()"> C-36 - Plumbing Contractor<br/></label>
            <label><input type="checkbox" value="C-38" id="C38" onchange="filterByLicense()"> C-38 - Refrigeration Contractor<br/></label>
            <label><input type="checkbox" value="C-39" id="C39" onchange="filterByLicense()"> C-39 - Roofing Contractor<br/></label>
            <label><input type="checkbox" value="C-42" id="C42" onchange="filterByLicense()"> C-42 - Sanitation System Contractor<br/></label>
            <label><input type="checkbox" value="C-43" id="C43" onchange="filterByLicense()"> C-43 - Sheet Metal Contractor<br/></label>
            <label><input type="checkbox" value="C-45" id="C45" onchange="filterByLicense()"> C-45 - Sign Contractor<br/></label>
            <label><input type="checkbox" value="C-46" id="C46" onchange="filterByLicense()"> C-46 - Solar Contractor<br/></label>
            <label><input type="checkbox" value="C-47" id="C47" onchange="filterByLicense()"> C-47 - General Manufactured Housing Contractor<br/></label>
            <label><input type="checkbox" value="C-49" id="C49" onchange="filterByLicense()"> C-49 - Tree and Palm Contractor<br/></label>
            <label><input type="checkbox" value="C-50" id="C50" onchange="filterByLicense()"> C-50 - Reinforcing Steel Contractor<br/></label>
            <label><input type="checkbox" value="C-51" id="C51" onchange="filterByLicense()"> C-51 - Structural Steel Contractor<br/></label>
            <label><input type="checkbox" value="C-53" id="C53" onchange="filterByLicense()"> C-53 - Swimming Pool Contractor<br/></label>
            <label><input type="checkbox" value="C-54" id="C54" onchange="filterByLicense()"> C-54 - Ceramic and Mosaic Tile Contractor<br/></label>
            <label><input type="checkbox" value="C-55" id="C55" onchange="filterByLicense()"> C-55 - Water Conditioning Contractor<br/></label>
            <label><input type="checkbox" value="C-57" id="C57" onchange="filterByLicense()"> C-57 - Well Drilling Contractor<br/></label>
            <label><input type="checkbox" value="C-60" id="C60" onchange="filterByLicense()"> C-60 - Welding Contractor<br/></label>
            <label><input type="checkbox" value="D-1" id="D1" onchange="filterByLicense()"> D-1 - Architectural Porcelain<br/></label>
            <label><input type="checkbox" value="D-2" id="D2" onchange="filterByLicense()"> D-2 - Asbestos Fabrication<br/></label>
            <label><input type="checkbox" value="D-3" id="D3" onchange="filterByLicense()"> D-3 - Awnings<br/></label>
            <label><input type="checkbox" value="D-4" id="D4" onchange="filterByLicense()"> D-4 - Central Vacuum Systems<br/></label>
            <label><input type="checkbox" value="D-5" id="D5" onchange="filterByLicense()"> D-5 - Communication Equipment<br/></label>
            <label><input type="checkbox" value="D-6" id="D6" onchange="filterByLicense()"> D-6 - Concrete Related Services<br/></label>
            <label><input type="checkbox" value="D-7" id="D7" onchange="filterByLicense()"> D-7 - Conveyors-Cranes<br/></label>
            <label><input type="checkbox" value="D-8" id="D8" onchange="filterByLicense()"> D-8 - Doors and Door Services<br/></label>
            <label><input type="checkbox" value="D-9" id="D9" onchange="filterByLicense()"> D-9 - Drilling, Blasting and Oil Field Work<br/></label>
            <label><input type="checkbox" value="D-10" id="D10" onchange="filterByLicense()"> D-10 - Elevated Floors<br/></label>
            <label><input type="checkbox" value="D-11" id="D11" onchange="filterByLicense()"> D-11 - Fencing<br/></label>
            <label><input type="checkbox" value="D-12" id="D12" onchange="filterByLicense()"> D-12 - Synthetic Products<br/></label>
            <label><input type="checkbox" value="D-13" id="D13" onchange="filterByLicense()"> D-13 - Fire Extinguisher Systems<br/></label>
            <label><input type="checkbox" value="D-14" id="D14" onchange="filterByLicense()"> D-14 - Floor Covering<br/></label>
            <label><input type="checkbox" value="D-15" id="D15" onchange="filterByLicense()"> D-15 - Furnaces<br/></label>
            <label><input type="checkbox" value="D-16" id="D16" onchange="filterByLicense()"> D-16 - Hardware, Locks and Safes<br/></label>
            <label><input type="checkbox" value="D-17" id="D17" onchange="filterByLicense()"> D-17 - Industrial Insulation<br/></label>
            <label><input type="checkbox" value="D-18" id="D18" onchange="filterByLicense()"> D-18 - Prison and Jail Equipment<br/></label>
            <label><input type="checkbox" value="D-19" id="D19" onchange="filterByLicense()"> D-19 - Land Clearing<br/></label>
            <label><input type="checkbox" value="D-20" id="D20" onchange="filterByLicense()"> D-20 - Lead Burning and Fabrication<br/></label>
            <label><input type="checkbox" value="D-21" id="D21" onchange="filterByLicense()"> D-21 - Machinery and Pumps<br/></label>
            <label><input type="checkbox" value="D-22" id="D22" onchange="filterByLicense()"> D-22 - Marble<br/></label>
            <label><input type="checkbox" value="D-23" id="D23" onchange="filterByLicense()"> D-23 - Medical Gas Systems<br/></label>
            <label><input type="checkbox" value="D-24" id="D24" onchange="filterByLicense()"> D-24 - Metal Products<br/></label>
            <label><input type="checkbox" value="D-25" id="D25" onchange="filterByLicense()"> D-25 - Mirrors and Fixed Glass<br/></label>
            <label><input type="checkbox" value="D-26" id="D26" onchange="filterByLicense()"> D-26 - Mobile Home Installation and Repairs<br/></label>
            <label><input type="checkbox" value="D-27" id="D27" onchange="filterByLicense()"> D-27 - Movable Partitions<br/></label>
            <label><input type="checkbox" value="D-28" id="D28" onchange="filterByLicense()"> D-28 - Doors, Gates and Activating Devices<br/></label>
            <label><input type="checkbox" value="D-29" id="D29" onchange="filterByLicense()"> D-29 - Paperhanging<br/></label>
            <label><input type="checkbox" value="D-30" id="D30" onchange="filterByLicense()"> D-30 - Pile Driving and Pressure Foundation Jacking<br/></label>
            <label><input type="checkbox" value="D-31" id="D31" onchange="filterByLicense()"> D-31 - Pole Installation and Maintenance<br/></label>
            <label><input type="checkbox" value="D-32" id="D32" onchange="filterByLicense()"> D-32 - Power Nailing and Fastening<br/></label>
            <label><input type="checkbox" value="D-33" id="D33" onchange="filterByLicense()"> D-33 - Precast Concrete Stairs<br/></label>
            <label><input type="checkbox" value="D-34" id="D34" onchange="filterByLicense()"> D-34 - Prefabricated Equipment<br/></label>
            <label><input type="checkbox" value="D-35" id="D35" onchange="filterByLicense()"> D-35 - Pool and Spa Maintenance<br/></label>
            <label><input type="checkbox" value="D-36" id="D36" onchange="filterByLicense()"> D-36 - Rigging and Rig Building<br/></label>
            <label><input type="checkbox" value="D-37" id="D37" onchange="filterByLicense()"> D-37 - Safes and Vaults<br/></label>
            <label><input type="checkbox" value="D-38" id="D38" onchange="filterByLicense()"> D-38 - Sand and Water Blasting<br/></label>
            <label><input type="checkbox" value="D-39" id="D39" onchange="filterByLicense()"> D-39 - Scaffolding<br/></label>
            <label><input type="checkbox" value="D-40" id="D40" onchange="filterByLicense()"> D-40 - Service Station Equipment and Maintenance<br/></label>
            <label><input type="checkbox" value="D-41" id="D41" onchange="filterByLicense()"> D-41 - Siding and Decking<br/></label>
            <label><input type="checkbox" value="D-42" id="D42" onchange="filterByLicense()"> D-42 - Non-Electrical Sign Installation<br/></label>
            <label><input type="checkbox" value="D-43" id="D43" onchange="filterByLicense()"> D-43 - Soil Grouting<br/></label>
            <label><input type="checkbox" value="D-44" id="D44" onchange="filterByLicense()"> D-44 - Sprinklers<br/></label>
            <label><input type="checkbox" value="D-45" id="D45" onchange="filterByLicense()"> D-45 - Staff and Stone<br/></label>
            <label><input type="checkbox" value="D-46" id="D46" onchange="filterByLicense()"> D-46 - Steeple Jack Work<br/></label>
            <label><input type="checkbox" value="D-47" id="D47" onchange="filterByLicense()"> D-47 - Tennis Court Surfacing<br/></label>
            <label><input type="checkbox" value="D-48" id="D48" onchange="filterByLicense()"> D-48 - Theater and School Equipment<br/></label>
            <label><input type="checkbox" value="D-49" id="D49" onchange="filterByLicense()"> D-49 - Tree Service<br/></label>
            <label><input type="checkbox" value="D-50" id="D50" onchange="filterByLicense()"> D-50 - Suspended Ceilings<br/></label>
            <label><input type="checkbox" value="D-51" id="D51" onchange="filterByLicense()"> D-51 - Waterproofing and Weatherproofing<br/></label>
            <label><input type="checkbox" value="D-52" id="D52" onchange="filterByLicense()"> D-52 - Window Coverings<br/></label>
            <label><input type="checkbox" value="D-53" id="D53" onchange="filterByLicense()"> D-53 - Wood Tanks<br/></label>
            <label><input type="checkbox" value="D-54" id="D54" onchange="filterByLicense()"> D-54 - Rockscaping<br/></label>
            <label><input type="checkbox" value="D-55" id="D55" onchange="filterByLicense()"> D-55 - Blasting<br/></label>
            <label><input type="checkbox" value="D-56" id="D56" onchange="filterByLicense()"> D-56 - Trenching Only<br/></label>
            <label><input type="checkbox" value="D-57" id="D57" onchange="filterByLicense()"> D-57 - Propane Gas Plants<br/></label>
            <label><input type="checkbox" value="D-58" id="D58" onchange="filterByLicense()"> D-58 - Residential Floating Docks<br/></label>
            <label><input type="checkbox" value="D-59" id="D59" onchange="filterByLicense()"> D-59 - Hydroseed Spraying<br/></label>
            <label><input type="checkbox" value="D-60" id="D60" onchange="filterByLicense()"> D-60 - Striping<br/></label>
            <label><input type="checkbox" value="D-61" id="D61" onchange="filterByLicense()"> D-61 - Gold Leaf Gilding<br/></label>
            <label><input type="checkbox" value="D-62" id="D62" onchange="filterByLicense()"> D-62 - Air and Water Balancing<br/></label>
            <label><input type="checkbox" value="D-63" id="D63" onchange="filterByLicense()"> D-63 - Construction Clean-up<br/></label>
            <label><input type="checkbox" value="D-64" id="D64" onchange="filterByLicense()"> D-64 - Non-specialized<br/></label>
            <label><input type="checkbox" value="D-65" id="D65" onchange="filterByLicense()"> D-65 - Weatherization and Energy Conservation<br/></label>
        </div>
    `;

    L.DomEvent.disableScrollPropagation(div);
    L.DomEvent.disableClickPropagation(div);

    return div;
};
filterControl.addTo(map);

function toggleSelectAll(selectAllCheckbox) {
    var checkboxes = document.querySelectorAll('.filter-box input[type="checkbox"]:not(#selectAll)'); // Exclude the "Select All" checkbox

    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked; // Set all checkboxes to match the "Select All" checkbox state
    });

    filterByLicense(); // Call filterByLicense to update the map based on the new selections
}


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
    var csvUrl = 'https://storage.googleapis.com/wesonder_databases/geolocations_cslb/refined_cslb_geolocations.csv'; // Replace with actual URL

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

function filterByLicense() {
    // Get selected checkboxes
    var checkboxes = document.querySelectorAll('.filter-box input[type="checkbox"]:checked');
    selectedLicenses = Array.from(checkboxes).map(checkbox => checkbox.value);

    // Clear existing markers
    markers.clearLayers();

    // If no license is selected or 'Select All' is checked, display all data
    var filteredData;
    if (selectedLicenses.length === 0 || document.getElementById('selectAll').checked) {
        filteredData = dataCache.filter(row => row['State'] === 'CA');
    } else {
        // Filter based on selected licenses
        filteredData = dataCache.filter(row => {
            const classification = (row['Classification'] || '').replace(/\s+/g, ''); // Remove any spaces
            const licenseArray = classification.split('|'); // Split the classification by "|" into an array

            return row['State'] === 'CA' && selectedLicenses.some(license => {
                const cleanLicense = license.replace(/-/g, ''); // Normalize the selected license (e.g., "C-2" becomes "C2")
                return licenseArray.some(classItem => classItem.replace(/-/g, '') === cleanLicense); // Exact match for each item
            });
        });
    }

    // Add filtered markers to the map
    filteredData.forEach(coord => {
        if (!isNaN(parseFloat(coord['X_Coordinate'])) && !isNaN(parseFloat(coord['Y_Coordinate']))) {
            var marker = L.marker([parseFloat(coord['X_Coordinate']), parseFloat(coord['Y_Coordinate'])]);
            marker.bindPopup(`
                <strong>Business Name:</strong> ${coord['BusinessName'] || 'N/A'}<br/>
                <strong>License Number:</strong> ${coord['LicenseNumber'] || 'N/A'}<br/>
                <strong>Classification:</strong> ${coord['Classification'] || 'N/A'}<br/>
                <strong>Address:</strong> ${coord['CompleteAddress'] || 'N/A'}<br/>
                <strong>Phone Number:</strong> ${coord['PhoneNumber'] || 'N/A'}<br/>
                <strong>Business Type:</strong> ${coord['BusinessType'] || 'N/A'}
            `);
            markers.addLayer(marker);
        }
    });
}






