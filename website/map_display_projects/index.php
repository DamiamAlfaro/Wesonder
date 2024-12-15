<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Projects"/>
    <link rel="icon" href="https://wesonder.sfo3.cdn.digitaloceanspaces.com/pictures/potential_favicon_2.png" type="image/x-icon"/>
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

    <title>Projects</title>
    
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
            max-height: 500px;
            width: 190px; /* Fixed width */
            overflow-y: auto; /* Enable scrolling for vertical overflow */
        }
        
        #checkboxForm input[type="checkbox"] {
            margin-right: 10px; /* Add spacing between checkbox and label */
        }
        
    </style>
    


</head>
<body>
    
    <form id="checkboxForm">
        <strong>Select County</strong><br><br>
        <input type="checkbox" name="county1" value="Alameda" onclick="handleCheckboxClick(this)"> Alameda<br>
        <input type="checkbox" name="county2" value="Amador" onclick="handleCheckboxClick(this)"> Amador<br>
        <input type="checkbox" name="county3" value="Butte" onclick="handleCheckboxClick(this)"> Butte<br>
        <input type="checkbox" name="county4" value="Calaveras" onclick="handleCheckboxClick(this)"> Calaveras<br>
        <input type="checkbox" name="county5" value="Colusa" onclick="handleCheckboxClick(this)"> Colusa<br>
        <input type="checkbox" name="county6" value="Contra Costa" onclick="handleCheckboxClick(this)"> Contra Costa<br>
        <input type="checkbox" name="county7" value="Del Norte" onclick="handleCheckboxClick(this)"> Del Norte<br>
        <input type="checkbox" name="county8" value="El Dorado" onclick="handleCheckboxClick(this)"> El Dorado<br>
        <input type="checkbox" name="county9" value="Fresno" onclick="handleCheckboxClick(this)"> Fresno<br>
        <input type="checkbox" name="county10" value="Glenn" onclick="handleCheckboxClick(this)"> Glenn<br>
        <input type="checkbox" name="county11" value="Humboldt" onclick="handleCheckboxClick(this)"> Humboldt<br>
        <input type="checkbox" name="county12" value="Imperial" onclick="handleCheckboxClick(this)"> Imperial<br>
        <input type="checkbox" name="county13" value="Inyo" onclick="handleCheckboxClick(this)"> Inyo<br>
        <input type="checkbox" name="county14" value="Kern" onclick="handleCheckboxClick(this)"> Kern<br>
        <input type="checkbox" name="county15" value="Kings" onclick="handleCheckboxClick(this)"> Kings<br>
        <input type="checkbox" name="county16" value="Lake" onclick="handleCheckboxClick(this)"> Lake<br>
        <input type="checkbox" name="county17" value="Lassen" onclick="handleCheckboxClick(this)"> Lassen<br>
        <input type="checkbox" name="county18" value="Los Angeles" onclick="handleCheckboxClick(this)"> Los Angeles<br>
        <input type="checkbox" name="county19" value="Madera" onclick="handleCheckboxClick(this)"> Madera<br>
        <input type="checkbox" name="county20" value="Marin" onclick="handleCheckboxClick(this)"> Marin<br>
        <input type="checkbox" name="county21" value="Mendocino" onclick="handleCheckboxClick(this)"> Mendocino<br>
        <input type="checkbox" name="county22" value="Merced" onclick="handleCheckboxClick(this)"> Merced<br>
        <input type="checkbox" name="county23" value="Modoc" onclick="handleCheckboxClick(this)"> Modoc<br>
        <input type="checkbox" name="county24" value="Mono" onclick="handleCheckboxClick(this)"> Mono<br>
        <input type="checkbox" name="county25" value="Monterey" onclick="handleCheckboxClick(this)"> Monterey<br>
        <input type="checkbox" name="county26" value="Napa" onclick="handleCheckboxClick(this)"> Napa<br>
        <input type="checkbox" name="county27" value="Nevada" onclick="handleCheckboxClick(this)"> Nevada<br>
        <input type="checkbox" name="county28" value="Orange" onclick="handleCheckboxClick(this)"> Orange<br>
        <input type="checkbox" name="county29" value="Placer" onclick="handleCheckboxClick(this)"> Placer<br>
        <input type="checkbox" name="county30" value="Plumas" onclick="handleCheckboxClick(this)"> Plumas<br>
        <input type="checkbox" name="county31" value="Riverside" onclick="handleCheckboxClick(this)"> Riverside<br>
        <input type="checkbox" name="county32" value="Sacramento" onclick="handleCheckboxClick(this)"> Sacramento<br>
        <input type="checkbox" name="county33" value="San Benito" onclick="handleCheckboxClick(this)"> San Benito<br>
        <input type="checkbox" name="county34" value="San Bernardino" onclick="handleCheckboxClick(this)"> San Bernardino<br>
        <input type="checkbox" name="county35" value="San Diego" onclick="handleCheckboxClick(this)"> San Diego<br>
        <input type="checkbox" name="county36" value="San Francisco" onclick="handleCheckboxClick(this)"> San Francisco<br>
        <input type="checkbox" name="county37" value="San Joaquin" onclick="handleCheckboxClick(this)"> San Joaquin<br>
        <input type="checkbox" name="county38" value="San Luis Obispo" onclick="handleCheckboxClick(this)"> San Luis Obispo<br>
        <input type="checkbox" name="county39" value="San Mateo" onclick="handleCheckboxClick(this)"> San Mateo<br>
        <input type="checkbox" name="county40" value="Santa Barbara" onclick="handleCheckboxClick(this)"> Santa Barbara<br>
        <input type="checkbox" name="county41" value="Santa Clara" onclick="handleCheckboxClick(this)"> Santa Clara<br>
        <input type="checkbox" name="county42" value="Santa Cruz" onclick="handleCheckboxClick(this)"> Santa Cruz<br>
        <input type="checkbox" name="county43" value="Shasta" onclick="handleCheckboxClick(this)"> Shasta<br>
        <input type="checkbox" name="county44" value="Sierra" onclick="handleCheckboxClick(this)"> Sierra<br>
        <input type="checkbox" name="county45" value="Siskiyou" onclick="handleCheckboxClick(this)"> Siskiyou<br>
        <input type="checkbox" name="county46" value="Solano" onclick="handleCheckboxClick(this)"> Solano<br>
        <input type="checkbox" name="county47" value="Sonoma" onclick="handleCheckboxClick(this)"> Sonoma<br>
        <input type="checkbox" name="county48" value="Stanislaus" onclick="handleCheckboxClick(this)"> Stanislaus<br>
        <input type="checkbox" name="county49" value="Sutter" onclick="handleCheckboxClick(this)"> Sutter<br>
        <input type="checkbox" name="county50" value="Tehama" onclick="handleCheckboxClick(this)"> Tehama<br>
        <input type="checkbox" name="county51" value="Tulare" onclick="handleCheckboxClick(this)"> Tulare<br>
        <input type="checkbox" name="county52" value="Tuolumne" onclick="handleCheckboxClick(this)"> Tuolumne<br>
        <input type="checkbox" name="county53" value="Ventura" onclick="handleCheckboxClick(this)"> Ventura<br>
        <input type="checkbox" name="county54" value="Yolo" onclick="handleCheckboxClick(this)"> Yolo<br>
        <input type="checkbox" name="county55" value="Yuba" onclick="handleCheckboxClick(this)"> Yuba<br>

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

                fetch('project_loading.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json()) // Change to `.json()` if the server returns JSON
                .then(data => {
                    if (data.status === 'success') {
                        
                        const projects = data.projects;
                        
                        var markers = L.markerClusterGroup();
                        
                        projects.forEach(project => {
                            const project_name = project.project_name;
                            const awarding_body = project.awarding_body;
                            const project_id_number = project.project_id_number;
                            const project_description = project.project_description;
                            const project_startdate = project.start_date;
                            const project_finishdate = project.finish_date;
                            const project_address = project.complete_address;
                            const x_coordinate = parseFloat(project.x_coordinates);
                            const y_coordinate = parseFloat(project.y_coordinates);
                            const project_county = project.county;
                            
                            const popupContent = `
                                <strong>Project Name:</strong> ${project_name}<br>
                                <strong>Awarding Body:</strong> ${awarding_body}<br>
                                <strong>Project ID Number:</strong> ${project_id_number}<br>
                                <strong>Description:</strong> ${project_description}<br>
                                <strong>Start Date:</strong> ${project_startdate}<br>
                                <strong>Finish Date:</strong> ${project_finishdate}<br>
                                <strong>Address:</strong> ${project_address}<br>
                            `;
                           
                            var marker = L.circleMarker([x_coordinate, y_coordinate], {
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
