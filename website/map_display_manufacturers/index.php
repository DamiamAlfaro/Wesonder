<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Projects"/>
    <link rel="icon" href="" type="image/x-icon"/>
    <link href="../style.css" rel="stylesheet" type="text/css">

    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""/>
    
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""></script>

    <!-- Leaflet MarkerCluster CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />

    <!-- Leaflet MarkerCluster JS -->
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

    <title>Manufacturers</title>
    
    <style>
        
        #map {
            height: 100vh;
            width: 100%;
            position: relative;
        }
        
        #manufacturerForm {
            position: absolute;
            top: 20px; /* Distance from the top */
            right: 20px; /* Distance from the right */
            background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white background */
            padding: 10px; /* Padding for better spacing */
            border-radius: 8px; /* Rounded corners */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); /* Add a slight shadow */
            z-index: 1000; /* Ensure it is above the map */
            height: auto; /* Fixed height */
            max-height: 650px;
            width: 240px; /* Fixed width */
            overflow-y: auto; /* Enable scrolling for vertical overflow */
            font-size: 18px;
            font-family: Optima;
        }
        
        #manufacturerForm input[type="checkbox"] {
            transform: scale(1.2);
            margin-right: 10px; /* Add spacing between checkbox and label */
        }
        
        #manufacturerForm input[type="checkbox"] + label {
            font-size: 18px; /* Adjust font size */
            font-family: Optima;
        }
        
    </style>
    


</head>
<body>
    
    <form id="manufacturerForm">
        
        <strong>Select Construction License</strong><br><br>
        
        <input type="checkbox" id="division3" name="division3" value="03" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division3">03 Concrete</label><br><br>
        
        <input type="checkbox" id="division4" name="division4" value="04" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division4">04 Masonry</label><br><br>
        
        <input type="checkbox" id="division5" name="division5" value="05" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division5">05 Metals</label><br><br>
        
        <input type="checkbox" id="division6" name="division6" value="06" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division6">06 Wood, Plastics, and Composites</label><br><br>
        
        <input type="checkbox" id="division7" name="division7" value="07" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division7">07 Thermal and Moisture Protection</label><br><br>
        
        <input type="checkbox" id="division8" name="division8" value="08" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division8">08 Openings</label><br><br>
        
        <input type="checkbox" id="division9" name="division9" value="09" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division9">09 Finishes</label><br><br>
        
        <input type="checkbox" id="division10" name="division10" value="10" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division10">10 Specialties</label><br><br>
        
        <input type="checkbox" id="division11" name="division11" value="11" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division11">11 Equipment</label><br><br>
        
        <input type="checkbox" id="division12" name="division12" value="12" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division12">12 Furnishings</label><br><br>
        
        <input type="checkbox" id="division13" name="division13" value="13" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division13">13 Special Construction</label><br><br>
        
        <input type="checkbox" id="division14" name="division14" value="14" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division14">14 Conveying Equipment</label><br><br>
        
        <input type="checkbox" id="division21" name="division21" value="21" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division21">21 Fire Suppression</label><br><br>
        
        <input type="checkbox" id="division22" name="division22" value="22" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division22">22 Plumbing</label><br><br>
        
        <input type="checkbox" id="division23" name="division23" value="23" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division23">23 Heating, Ventilating, and Air Conditioning (HVAC)</label><br><br>
        
        <input type="checkbox" id="division25" name="division25" value="25" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division25">25 Integrated Automation</label><br><br>
        
        <input type="checkbox" id="division26" name="division26" value="26" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division26">26 Electrical</label><br><br>
        
        <input type="checkbox" id="division27" name="division27" value="27" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division27">27 Communications</label><br><br>
        
        <input type="checkbox" id="division28" name="division28" value="28" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division28">28 Electronic Safety and Security</label><br><br>
        
        <input type="checkbox" id="division31" name="division31" value="31" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division31">31 Earthwork</label><br><br>
        
        <input type="checkbox" id="division32" name="division32" value="32" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division32">32 Exterior Improvements</label><br><br>
        
        <input type="checkbox" id="division33" name="division33" value="33" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division33">33 Utilities</label><br><br>
        
        <input type="checkbox" id="division34" name="division34" value="34" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division34">34 Transportation</label><br><br>
        
        <input type="checkbox" id="division35" name="division35" value="35" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division35">35 Waterway and Marine Construction</label><br><br>
        
        <input type="checkbox" id="division40" name="division40" value="40" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division40">40 Process Integration</label><br><br>
        
        <input type="checkbox" id="division41" name="division41" value="41" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division41">41 Material Processing and Handling Equipment</label><br><br>
        
        <input type="checkbox" id="division42" name="division42" value="42" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division42">42 Process Heating, Cooling, and Drying Equipment</label><br><br>
        
        <input type="checkbox" id="division43" name="division43" value="43" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division43">43 Process Gas and Liquid Handling, Purification, and Storage Equipment</label><br><br>
        
        <input type="checkbox" id="division44" name="division44" value="44" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division44">44 Pollution and Waste Control Equipment</label><br><br>
        
        <input type="checkbox" id="division45" name="division45" value="45" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division45">45 Industry-Specific Manufacturing Equipment</label><br><br>
        
        <input type="checkbox" id="division46" name="division46" value="46" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division46">46 Water and Wastewater Equipment</label><br><br>
        
        <input type="checkbox" id="division48" name="division48" value="48" onclick="ManufacturerCheckboxingClick(this)">
        <label for="division48">48 Electrical Power Generation</label><br><br>

    </form>


    


    <?php

        
    ?>
    

    <div id="map"></div>

    <script>
        var map = L.map('map', {
            renderer: L.canvas() // Enable Canvas rendering
        }).setView([37.7749, -122.4194], 5);
        
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
        
        var markerGroups = {};
        
        function ManufacturerCheckboxingClick(checkbox) {
            // Prepare the data to send to the server
            const formData = new FormData();
            formData.append('checkbox_name', checkbox.name);
            formData.append('checkbox_value', checkbox.value);
            formData.append('checkbox_checked', checkbox.checked);
        
            if (checkbox.checked) {

                fetch('loading_manufacturers.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json()) // Change to `.json()` if the server returns JSON
                .then(data => {
                    if (data.status === 'success') {
                        
                        const manufacturers = data.manufacturers;
                        
                        var markers = L.markerClusterGroup({
                            iconCreateFunction: function(cluster) {
                                // Get the count of markers in the cluster
                                var count = cluster.getChildCount();
                        
                                // Define border and fill colors dynamically
                                var clusterFillColor = count < 10 ? '#68c4cc' : count < 50 ? '#ffa500' : '#ff5733'; // Fill colors
                                var clusterBorderColor = count < 10 ? '#1f5572' : count < 50 ? '#cc8400' : '#b53324'; // Border colors
                        
                                // Create the custom cluster icon
                                return L.divIcon({
                                    html: `
                                        <div style="
                                            background-color: ${clusterFillColor}; 
                                            border: 3px solid ${clusterBorderColor}; 
                                            border-radius: 50%; 
                                            color: black; 
                                            text-align: center; 
                                            line-height: 35px; 
                                            width: 35px; 
                                            height: 35px;
                                            font-weight: bold;
                                            font-size: 13px;
                                        ">
                                            ${count}
                                        </div>`,
                                    className: 'cluster-icon',
                                    iconSize: [20, 20] // Size of the cluster icon
                                });
                            }
                        });

                        
                        manufacturers.forEach(manufacturer => {
                            const spec_number = manufacturer.spec_number;
                            const spec_name = manufacturer.spec_name;
                            const spec_complete_name = manufacturer.spec_complete_name;
                            const manufacturer_name = manufacturer.manufacturer_name;
                            const manufacturer_address = manufacturer.manufacturer_address;
                            const manufacturer_phones = manufacturer.manufacturer_phones;
                            const manufacturer_website = manufacturer.manufacturer_website;
                            const x_coordinates = parseFloat(manufacturer.x_coordinates);
                            const y_coordinates = parseFloat(manufacturer.y_coordinates);
                        
                            
                            const popupContent = `
                                <strong>Name: </strong> ${manufacturer_name}<br>
                                <strong>Spec: </strong> ${spec_complete_name}<br>
                                <strong>Phone Number(s): </strong> ${manufacturer_phones}<br>
                                <strong>Manufacturer Website:</strong> <a href='https://${manufacturer_website}'>${manufacturer_website}</a><br>
                                <strong>Manufacturer Address:</strong> ${manufacturer_address}<br>
                            `;
                           
                            var marker = L.circleMarker([x_coordinates, y_coordinates], {
                                radius: 7, // Marker size
                                color: '#1f5572', // Border color
                                fillColor: '#68c4cc', // Fill color
                                fillOpacity: 0.5 // Opacity
                                }).bindPopup(popupContent);
                                markers.addLayer(marker);
                        });
                        
                        map.addLayer(markers);
                        markerGroups[checkbox.name] = markers;
        
                    } else if (data.status === 'unchecked') {
                        console.log(data.message);
                    } else {
                        console.error('Unexpected response:', data);
                    }
                })
                .catch(error => console.error('Error:', error));
                
            } else {
                
                if (markerGroups[checkbox.name]) {
                    map.removeLayer(markerGroups[checkbox.name]); // Remove the marker group from the map
                    delete markerGroups[checkbox.name]; // Remove the reference from the object
                }
                
                
            }
        }
        
        
    </script>


</body>
</html>
;
