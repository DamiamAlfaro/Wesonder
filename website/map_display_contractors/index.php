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

    <title>Contractors/Subcontractors</title>
    
    <style>
        
        #map {
            height: 100vh;
            width: 100%;
            position: relative;
        }
        
        #checkboxForm {
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
            width: 190px; /* Fixed width */
            overflow-y: auto; /* Enable scrolling for vertical overflow */
        }
        
        #checkboxForm input[type="checkbox"] {
            transform: scale(1.3);
            margin-right: 10px; /* Add spacing between checkbox and label */
        }
        
        #checkboxForm input[type="checkbox"] + label {
            font-size: 20px; /* Adjust font size */
            font-family: Optima;
        }
        
    </style>
    


</head>
<body>
    
    <form id="checkboxForm">
        <input type="checkbox" id="county1" name="county1" value="Alameda" onclick="handleCheckboxClick(this)">
        <label for="county1">Alameda</label><br>
    
        <input type="checkbox" id="county2" name="county2" value="Amador" onclick="handleCheckboxClick(this)">
        <label for="county2">Amador</label><br>
    
        <input type="checkbox" id="county3" name="county3" value="Butte" onclick="handleCheckboxClick(this)">
        <label for="county3">Butte</label><br>
    
        <input type="checkbox" id="county4" name="county4" value="Calaveras" onclick="handleCheckboxClick(this)">
        <label for="county4">Calaveras</label><br>
    
        <input type="checkbox" id="county5" name="county5" value="Colusa" onclick="handleCheckboxClick(this)">
        <label for="county5">Colusa</label><br>
    
        <input type="checkbox" id="county6" name="county6" value="Contra Costa" onclick="handleCheckboxClick(this)">
        <label for="county6">Contra Costa</label><br>
    
        <input type="checkbox" id="county7" name="county7" value="Del Norte" onclick="handleCheckboxClick(this)">
        <label for="county7">Del Norte</label><br>
    
        <input type="checkbox" id="county8" name="county8" value="El Dorado" onclick="handleCheckboxClick(this)">
        <label for="county8">El Dorado</label><br>
    
        <input type="checkbox" id="county9" name="county9" value="Fresno" onclick="handleCheckboxClick(this)">
        <label for="county9">Fresno</label><br>
    
        <input type="checkbox" id="county10" name="county10" value="Glenn" onclick="handleCheckboxClick(this)">
        <label for="county10">Glenn</label><br>
    
        <input type="checkbox" id="county11" name="county11" value="Humboldt" onclick="handleCheckboxClick(this)">
        <label for="county11">Humboldt</label><br>
    
        <input type="checkbox" id="county12" name="county12" value="Imperial" onclick="handleCheckboxClick(this)">
        <label for="county12">Imperial</label><br>
    
        <input type="checkbox" id="county13" name="county13" value="Inyo" onclick="handleCheckboxClick(this)">
        <label for="county13">Inyo</label><br>
    
        <input type="checkbox" id="county14" name="county14" value="Kern" onclick="handleCheckboxClick(this)">
        <label for="county14">Kern</label><br>
    
        <input type="checkbox" id="county15" name="county15" value="Kings" onclick="handleCheckboxClick(this)">
        <label for="county15">Kings</label><br>
    
        <input type="checkbox" id="county16" name="county16" value="Lake" onclick="handleCheckboxClick(this)">
        <label for="county16">Lake</label><br>
    
        <input type="checkbox" id="county17" name="county17" value="Lassen" onclick="handleCheckboxClick(this)">
        <label for="county17">Lassen</label><br>
    
        <input type="checkbox" id="county18" name="county18" value="Los Angeles" onclick="handleCheckboxClick(this)">
        <label for="county18">Los Angeles</label><br>
    
        <input type="checkbox" id="county19" name="county19" value="Madera" onclick="handleCheckboxClick(this)">
        <label for="county19">Madera</label><br>
    
        <input type="checkbox" id="county20" name="county20" value="Marin" onclick="handleCheckboxClick(this)">
        <label for="county20">Marin</label><br>
    
        <input type="checkbox" id="county21" name="county21" value="Mendocino" onclick="handleCheckboxClick(this)">
        <label for="county21">Mendocino</label><br>
    
        <input type="checkbox" id="county22" name="county22" value="Merced" onclick="handleCheckboxClick(this)">
        <label for="county22">Merced</label><br>
    
        <input type="checkbox" id="county23" name="county23" value="Modoc" onclick="handleCheckboxClick(this)">
        <label for="county23">Modoc</label><br>
    
        <input type="checkbox" id="county24" name="county24" value="Mono" onclick="handleCheckboxClick(this)">
        <label for="county24">Mono</label><br>
    
        <input type="checkbox" id="county25" name="county25" value="Monterey" onclick="handleCheckboxClick(this)">
        <label for="county25">Monterey</label><br>
    
        <input type="checkbox" id="county26" name="county26" value="Napa" onclick="handleCheckboxClick(this)">
        <label for="county26">Napa</label><br>
    
        <input type="checkbox" id="county27" name="county27" value="Nevada" onclick="handleCheckboxClick(this)">
        <label for="county27">Nevada</label><br>
    
        <input type="checkbox" id="county28" name="county28" value="Orange" onclick="handleCheckboxClick(this)">
        <label for="county28">Orange</label><br>
    
        <input type="checkbox" id="county29" name="county29" value="Placer" onclick="handleCheckboxClick(this)">
        <label for="county29">Placer</label><br>
    
        <input type="checkbox" id="county30" name="county30" value="Plumas" onclick="handleCheckboxClick(this)">
        <label for="county30">Plumas</label><br>
    
        <input type="checkbox" id="county31" name="county31" value="Riverside" onclick="handleCheckboxClick(this)">
        <label for="county31">Riverside</label><br>
    
        <input type="checkbox" id="county32" name="county32" value="Sacramento" onclick="handleCheckboxClick(this)">
        <label for="county32">Sacramento</label><br>
    
        <input type="checkbox" id="county33" name="county33" value="San Benito" onclick="handleCheckboxClick(this)">
        <label for="county33">San Benito</label><br>
    
        <input type="checkbox" id="county34" name="county34" value="San Bernardino" onclick="handleCheckboxClick(this)">
        <label for="county34">San Bernardino</label><br>
    
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
        
        function handleCheckboxClick(checkbox) {
            // Prepare the data to send to the server
            const formData = new FormData();
            formData.append('checkbox_name', checkbox.name);
            formData.append('checkbox_value', checkbox.value);
            formData.append('checkbox_checked', checkbox.checked);
        
            if (checkbox.checked) {

                fetch('loading_contractors.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json()) // Change to `.json()` if the server returns JSON
                .then(data => {
                    if (data.status === 'success') {
                        
                        const contractors = data.contractors;
                        
                        var markers = L.markerClusterGroup();
                        
                        contractors.forEach(contractor => {
                            const license_number = contractor.license_number;
                            const business_type = contractor.business_type;
                            const contractor_name = contractor.contractor_name;
                            const county = contractor.county;
                            const phone_number = contractor.phone_number;
                            const issue_date = contractor.issue_date;
                            const expiration_date = contractor.expiration_date;
                            const classifications = contractor.classifications;
                            const complete_address = contractor.complete_address;
                            const x_coordinates = parseFloat(contractor.x_coordinates);
                            const y_coordinates = parseFloat(contractor.y_coordinates);
                        
                            
                            const popupContent = `
                                <strong>Name: </strong> ${contractor_name}<br>
                                <strong>Business Type: </strong> ${business_type}<br>
                                <strong>License Number:</strong> ${license_number}<br>
                                <strong>Phone Number:</strong> ${phone_number}<br>
                                <strong>Classifications:</strong> ${classifications}<br>
                                <strong>Address:</strong> ${complete_address}<br>
                            `;
                           
                            var marker = L.circleMarker([x_coordinates, y_coordinates], {
                                radius: 6, // Marker size
                                color: '#3388ff', // Border color
                                fillColor: '#3388ff', // Fill color
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
