<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Map Display"/>
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

    <title>Map Display</title>

</head>
<body>

    <?php 
    
        $host = "localhost"; 
        $username = "u978864605_wesonder";
        $password = "Elchapillo34?nmddam";
        $dbname = "u978864605_wesonder";
        
        // Connect to the database
        $conn = new mysqli($host, $username, $password, $dbname);
        
        // Markers that will later be displayed on the leaflet.js map
        $markers = [];
        
        
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        
        $sql = "SELECT * FROM dir_entities WHERE entity_type IN ('Awarding Body\nType') LIMIT 10";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                $entity_email = $row['entity_email'];
                $entity_address = $row['full_address'];
                $entity_county = $row['entity_county'];
                $x_coordinates = $row['x_coordinates'];
                $y_coordinates = $row['y_coordinates'];
                $awarding_body_name = $row['awarding_body_name'];
                $entity_web_pages = $row['web_pages'];
                $entity_web_links = $row['web_links'];
                
                $markers[] = [
                    'email' => $entity_email,
                    'address' => $entity_address,
                    'county' => $entity_county,
                    'x_coordinate' => $x_coordinates,
                    'y_coordinate' => $y_coordinates,
                    'name' => $awarding_body_name,
                    'web_pages' => $entity_web_pages,
                    'web_links' => $entity_web_links
                ];
                
            }
        } else {
            echo "No results found.";
        }
        
        // Close the connection
        $conn->close();

    ?>
    

    <div id="map"></div>

    <script>
        var map = L.map('map').setView([37.7749, -122.4194], 5);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        var markers = <?php echo json_encode($markers); ?>;
        
        markers.forEach(function(markerData) {
            var marker = L.marker([markerData.x_coordinate, markerData.y_coordinate]).addTo(map);
            marker.bindPopup(markerData.name);
        });
        
        
    </script>


</body>
</html>
