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
    


</head>
<body>
    
    <form id="checkboxForm">
        <input type="checkbox" name="county1" value="San Diego" onclick="handleCheckboxClick(this)"> San Diego<br>
        <input type="checkbox" name="county2" value="Los Angeles" onclick="handleCheckboxClick(this)"> Los Angeles<br>
        <input type="checkbox" name="county3" value="Riverside" onclick="handleCheckboxClick(this)"> Riverside<br>
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
