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
    

    <?php 
    
        $host = "localhost"; 
        $username = "u978864605_wesonder";
        $password = "Elchapillo34?nmddam";
        $dbname = "u978864605_wesonder";
        
        $conn = new mysqli($host, $username, $password, $dbname);
        
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $mapMarkersScript = "var markers = L.markerClusterGroup();\n";

        $sql = "SELECT * FROM dir_projects LIMIT 1000";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                
                // Assign variables based on the headers of the table from MySQL
                $project_number = $row['project_number'];
                $project_name = $row['project_name'];
                $awarding_body = $row['awarding_body'];
                $project_id_number = $row['project_id_number'];
                $project_dir_number = $row['project_dir_number'];
                $project_description = $row['project_description'];
                $start_date = $row['date_started'];
                $finish_date = $row['date_finished'];
                $complete_address = $row['complete_address'];
                $x_coordinates = $row['x_coordinates'];
                $y_coordinates = $row['y_coordinates'];
                $county = $row['county'];
                
                $string_display = "
                <strong>Project Name:</strong> $project_name <br>
                <strong>Project Number:</strong> $project_number <br>
                <strong>Awarding Body:</strong> $awarding_body <br>
                <strong>Address:</strong> $complete_address <br>
                <strong>Project ID Number:</strong> $project_id_number <br>
                <strong>Project DIR Number:</strong> $project_dir_number <br>
                <strong>Description:</strong> $project_description <br>
                <strong>Start Date:</strong> $start_date <br>
                <strong>End Date:</strong> $finish_date <br>
                ";
                
                $mapMarkersScript .= "
                    var marker = L.circleMarker([$x_coordinates, $y_coordinates], {
                        radius: 6, // Marker size
                        color: '#3388ff', // Border color
                        fillColor: '#3388ff', // Fill color
                        fillOpacity: 0.5 // Opacity
                    }).bindPopup(" . json_encode($string_display) . ");
                    markers.addLayer(marker);
                ";
                
                
            }
        } else {
            echo "No results found.";
        }
        
        $conn->close();

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
        map.addLayer(markers);
        
        
        
    </script>


</body>
</html>
;
