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
    
        <input type="checkbox" id="county35" name="county35" value="San Diego" onclick="handleCheckboxClick(this)">
        <label for="county35">San Diego</label><br>
    
        <input type="checkbox" id="county36" name="county36" value="San Francisco" onclick="handleCheckboxClick(this)">
        <label for="county36">San Francisco</label><br>
    
        <input type="checkbox" id="county37" name="county37" value="San Joaquin" onclick="handleCheckboxClick(this)">
        <label for="county37">San Joaquin</label><br>
    
        <input type="checkbox" id="county38" name="county38" value="San Luis Obispo" onclick="handleCheckboxClick(this)">
        <label for="county38">San Luis Obispo</label><br>
    
        <input type="checkbox" id="county39" name="county39" value="San Mateo" onclick="handleCheckboxClick(this)">
        <label for="county39">San Mateo</label><br>
    
        <input type="checkbox" id="county40" name="county40" value="Santa Barbara" onclick="handleCheckboxClick(this)">
        <label for="county40">Santa Barbara</label><br>
    
        <input type="checkbox" id="county41" name="county41" value="Santa Clara" onclick="handleCheckboxClick(this)">
        <label for="county41">Santa Clara</label><br>
    
        <input type="checkbox" id="county42" name="county42" value="Santa Cruz" onclick="handleCheckboxClick(this)">
        <label for="county42">Santa Cruz</label><br>
    
        <input type="checkbox" id="county43" name="county43" value="Shasta" onclick="handleCheckboxClick(this)">
        <label for="county43">Shasta</label><br>
    
        <input type="checkbox" id="county44" name="county44" value="Sierra" onclick="handleCheckboxClick(this)">
        <label for="county44">Sierra</label><br>
    
        <input type="checkbox" id="county45" name="county45" value="Siskiyou" onclick="handleCheckboxClick(this)">
        <label for="county45">Siskiyou</label><br>
    
        <input type="checkbox" id="county46" name="county46" value="Solano" onclick="handleCheckboxClick(this)">
        <label for="county46">Solano</label><br>
    
        <input type="checkbox" id="county47" name="county47" value="Sonoma" onclick="handleCheckboxClick(this)">
        <label for="county47">Sonoma</label><br>
    
        <input type="checkbox" id="county48" name="county48" value="Stanislaus" onclick="handleCheckboxClick(this)">
        <label for="county48">Stanislaus</label><br>
    
        <input type="checkbox" id="county49" name="county49" value="Sutter" onclick="handleCheckboxClick(this)">
        <label for="county49">Sutter</label><br>
    
        <input type="checkbox" id="county50" name="county50" value="Tehama" onclick="handleCheckboxClick(this)">
        <label for="county50">Tehama</label><br>
    
        <input type="checkbox" id="county51" name="county51" value="Tulare" onclick="handleCheckboxClick(this)">
        <label for="county51">Tulare</label><br>
    
        <input type="checkbox" id="county52" name="county52" value="Tuolumne" onclick="handleCheckboxClick(this)">
        <label for="county52">Tuolumne</label><br>
    
        <input type="checkbox" id="county53" name="county53" value="Ventura" onclick="handleCheckboxClick(this)">
        <label for="county53">Ventura</label><br>
    
        <input type="checkbox" id="county54" name="county54" value="Yolo" onclick="handleCheckboxClick(this)">
        <label for="county54">Yolo</label><br>
    
        <input type="checkbox" id="county55" name="county55" value="Yuba" onclick="handleCheckboxClick(this)">
        <label for="county55">Yuba</label><br>
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
