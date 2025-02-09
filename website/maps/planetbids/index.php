<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Map Display"/>
    <link rel="icon" type="image/png" href="../media/bauhaus_logo_transparent.png"/>
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

    <title>Planetbids Bids</title>
    
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

        
        $sql = "SELECT * FROM planetbids";
        $result = $conn->query($sql);
        
        $coordinates_tracker = []; // To track occurrences of x, y pairs

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                
                // Assign variables based on the headers of the table from MySQL
                $allegedab = addslashes($row['allegedab']);
                $weblink = addslashes($row['weblink']);
                $county = addslashes($row['county']);
                $x_coordinates = (float)$row['x_coordinate'];
                $y_coordinates = (float)$row['y_coordinate'];
                $bid_url = $row['bid_url'];
                $bid_ab = $row['bid_ab'];
                $bid_posted_date = $row['bid_posted_date'];
                $bid_title = $row['bid_title'];
                $bid_invitation_id = $row['bid_invitation_id'];
                
                // Split the date due date variable into two for Date and Time
                $bid_due_date = $row['bid_due_date'];
                $parts = explode(" ",$bid_due_date);
                $bid_due_day = $parts[0];
                $bid_due_time = $parts[1];
                
                $bid_status = $row['bid_status'];
                $bid_submission_method = $row['bid_submission_method'];

                $key = "$x_coordinates,$y_coordinates";
                if (isset($coordinates_tracker[$key])) {
                    // Increment the counter for this coordinate pair
                    $coordinates_tracker[$key]++;
        
                    // Apply a small random variation
                    $x_coordinates += mt_rand(-10, 10) / 1000; // Adjust to your precision needs
                    $y_coordinates += mt_rand(-10, 10) / 1000;
                } else {
                    // Initialize the counter for this coordinate pair
                    $coordinates_tracker[$key] = 1;
                }

                
                $string_display = "
                    <strong>Name:</strong> $bid_ab <br>
                    <strong>Bid URL: </strong> <a href='$bid_url' target='_blank'>$bid_url</a><br>
                    <strong>Solicitation Number: </strong> $bid_invitation_id <br>
                    <strong>Solicitation Name: </strong> $bid_title <br>
                    <strong>Opening Date: </strong> $bid_posted_date <br>
                    <strong>Closing Date: </strong> $bid_due_day <br>
                    <strong>Closing Time: </strong> $bid_due_time <br>
                    <strong>Submission Method: </strong> $bid_submission_method<br>
                    <strong>X: </strong> $x_coordinates<br>
                    <strong>Y: </strong> $y_coordinates<br>
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
