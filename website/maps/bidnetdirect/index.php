<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Map Display"/>
    <link rel="icon" type="image/png" href="../../media/bauhaus_logo_transparent.png"/>
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

    <title>Bidnet Direct Active Bids</title>
    
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
    
    .leaflet-popup-content {
        max-width: 300px; /* Set the maximum width for the popup */
        white-space: normal; /* Ensure text wraps within the content */
        overflow-wrap: break-word; /* Break long words to fit within the popup */
    }

    /* Add scrolling for very large content */
    .leaflet-popup-content-wrapper {
        max-height: 400px; /* Set a maximum height */
        overflow-y: auto; /* Enable vertical scrolling if content exceeds height */
    }

    .leaflet-popup-content a {
        word-wrap: break-word; /* Break long links into multiple lines */
        color: blue; /* Optional: Make links more readable */
        text-decoration: underline;
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
        $mapMarkersScript = "";

        
        $sql = "SELECT * FROM bidnetdirect_bids WHERE solicitation_number != 'none'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                
                // Assign variables based on the headers of the table from MySQL
                $awarding_body = addslashes($row['awarding_body']);
                $url = addslashes($row['url']);
                $couty = addslashes($row['county']);
                $x_coordinates = $row['x_coordinates'];
                $y_coordinates = $row['y_coordinates'];
                $solicitation_number = $row['solicitation_number'];
                $solicitation_name = $row['solicitation_name'];
                $opening_date = $row['opening_date'];
                $closing_date = $row['closing_date'];
                $solicitation_url = $row['solicitation_url'];
                $closing_time = $row['closing_time'];


                
                $string_display = "
                    <strong>Name:</strong> $awarding_body <br>
                    <strong>Bidnet Direct URL: </strong> <a href='$url' target='_blank'>$url</a><br>
                    <strong>Solicitation Number: </strong> $solicitation_number <br>
                    <strong>Solicitation Name: </strong> $solicitation_name <br>
                    <strong>Opening Date: </strong> $opening_date <br>
                    <strong>Closing Date: </strong> $closing_date <br>
                    <strong>Closing Time: </strong> $closing_time <br>
                    <strong>Solicitation Link: </strong> <a href='$solicitation_url' target='_blank'>$solicitation_url</a><br>
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
    
        // Add tile layer
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
    
        // Create a MarkerClusterGroup with custom options
        var markers = L.markerClusterGroup({
            disableClusteringAtZoom: 18, // Disable clustering at zoom level 18 and closer
            maxClusterRadius: 40, // Cluster markers within a 40-pixel radius
            spiderfyOnMaxZoom: true, // Allow spiderfying overlapping markers
            showCoverageOnHover: false, // Don't show cluster coverage area on hover
            iconCreateFunction: function(cluster) {
                // Customize cluster icon appearance
                var childCount = cluster.getChildCount();
    
                var c = 'marker-cluster-';
                if (childCount < 25) {
                    c += 'small';
                } else if (childCount < 350) {
                    c += 'medium';
                } else {
                    c += 'large';
                }
    
                return new L.DivIcon({
                    html: '<div><span>' + childCount + '</span></div>',
                    className: 'marker-cluster ' + c,
                    iconSize: [40, 40]
                });
            }
        });
    
        // Add dynamically generated markers
        <?php echo $mapMarkersScript; ?>
    
        // Add the MarkerClusterGroup to the map
        map.addLayer(markers);
    </script>


</body>
</html>
