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
    
        echo "
            <script type=\"text/javascript\">
                function handleCheckboxClick(checkbox) {
                    // Prepare the data to send to the server
                    const formData = new FormData();
                    formData.append('checkbox_name', checkbox.name);
                    formData.append('checkbox_value', checkbox.value);
                    formData.append('checkbox_checked', checkbox.checked);
                
                    // Send the data using AJAX
                    fetch('project_loading.php', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json()) // Change to `.json()` if the server returns JSON
                    .then(data => {
                        if (data.status === 'success') {
                            const projects = data.projects;
                            console.log(projects);
                        } else if (data.status === 'unchecked') {
                            console.log(data.message);
                        } else {
                            console.error('Unexpected response:', data);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }
            </script>
        ";
    

        $mapMarkersScript = "var markers = L.markerClusterGroup();\n";
                
        $mapMarkersScript .= "
            var marker = L.circleMarker([$x_coordinates, $y_coordinates], {
                radius: 6, // Marker size
                color: '#3388ff', // Border color
                fillColor: '#3388ff', // Fill color
                fillOpacity: 0.5 // Opacity
            }).bindPopup(" . json_encode($string_display) . ");
            markers.addLayer(marker);
        ";
        
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
        

        <?php echo $mapMarkersScript; ?>
        // map.addLayer(markers);
        
        
        
    </script>


</body>
</html>
;
