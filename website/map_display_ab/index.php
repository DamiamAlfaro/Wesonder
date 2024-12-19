<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Map Display"/>
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

    <title>Map Display</title>
    
    <style>
    
    #map {
        height: 100vh;
        width: 100%;
        position: relative;
    }
    
    /* Base cluster style */
    .marker-cluster {
        background-clip: padding-box;
        border-radius: 50%; /* Makes the cluster circular */
        color: black;
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        line-height: 40px; /* Align text vertically */
        cursor: pointer;
    }
    
    /* Small clusters */
    .marker-cluster-small {
        background-color: #90ee90; /* Light green */
        width: 40px;
        height: 40px;
    }
    
    /* Medium clusters */
    .marker-cluster-medium {
        background-color: #ffa500; /* Orange */
        width: 50px;
        height: 50px;
    }
    
    /* Large clusters */
    .marker-cluster-large {
        background-color: #ff4500; /* Red */
        width: 60px;
        height: 60px;
    }
    
    </style>


</head>
<body>
    

    <?php 
        
        $host = "localhost"; 
        $username = "u978864605_wesonder";
        $password = "Elchapillo34?nmddam";
        $dbname = "u978864605_wesonder";
        
        // Connect to the database
        $conn = new mysqli($host, $username, $password, $dbname);
        
        
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        
        // Markers that will later be displayed on the leaflet.js map
        $mapMarkersScript = "
            var markers = L.markerClusterGroup({
                iconCreateFunction: function(cluster) {
                    // Calculate the number of markers in the cluster
                    var childCount = cluster.getChildCount();
                    
                    // Define a class based on the number of markers
                    var c = 'marker-cluster-'; 
                    if (childCount < 25) {
                        c += 'small';
                    } else if (childCount < 350) {
                        c += 'medium';
                    } else {
                        c += 'large';
                    } 
        
                    // Return a custom cluster icon
                    return new L.DivIcon({ 
                        html: '<div><span>' + childCount + '</span></div>',
                        className: 'marker-cluster ' + c, 
                        iconSize: [40, 40] // Size of the cluster icon
                    });
                }
            });
        ";

        
        $sql = "SELECT * FROM dir_awarding_bodies WHERE state = 'CA'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                
                // Assign variables based on the headers of the table from MySQL
                $name = addslashes($row['name']);
                $email = addslashes($row['email']);
                $state = addslashes($row['state']);
                $county = addslashes($row['county']);
                $address = addslashes($row['full_address']);
                $x_coordinates = $row['x_coordinate'];
                $y_coordinates = $row['y_coordinate'];
                $awarding_body_name = addslashes(htmlspecialchars($row['ab_name'], ENT_QUOTES));
                $entity_web_pages = $row['web_pages'];
                $entity_web_links = $row['web_links'];
                
                // Segreate and accommodate the respective webpages for each Awarding body 
                $web_pages_array = explode(',', $row['web_pages']);
                $web_links_array = explode(',', $entity_web_links);
                
                $webpageHTML = [];
                foreach ($web_pages_array as $index => $web_page) {
                    $web_page = trim($web_page);
                    $web_link = isset($web_links_array[$index]) ? trim($web_links_array[$index]) : '#';
                    if (!empty($web_page)) {
                        $webpageHTML[] = "<a href='" . htmlspecialchars($web_link, ENT_QUOTES) . "' target='_blank'>" . htmlspecialchars($web_page, ENT_QUOTES) . "</a>";
                    }
                }
                $webpageHTMLFormatted = implode(', ', $webpageHTML);

                
                $string_display = "
                <strong>Name:</strong> $awarding_body_name <br>
                <strong>Email: </strong> $email <br>
                <strong>Address: </strong> $address <br>
                <strong>WebPages: </strong> $webpageHTMLFormatted
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
        
        // Close the connection
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
