<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Map Display"/>
    <link rel="icon" type="image/png" href="../../../media/bauhaus_logo_transparent.png"/>
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

    <!-- Leaflet MarkerCluster J-S -->
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

    <title>Map Display</title>
    
    <style>
    
    #map {
        height: 100vh;
        width: 100%;
        position: relative;
    }
    
    /* Brutalistic Minimalistic Modern Design */
    .marker-cluster.block-shadow {
        background: white;
        color: black;
        border: 2px solid black;
        box-shadow: 8px 8px 0px black;
        font-family: "Impact", sans-serif;
        font-size: 16px;
        text-transform: uppercase;
        text-align: center;
    }
    
    .marker-cluster:hover {
        transform: scale(1.1);
    }
    
    .marker-cluster-small, .marker-cluster-medium, .marker-cluster-large {
        width: 50px;
        height: 50px;
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
                    <div style='font-family: Poppins, sans-serif; font-size: 14px; font-weight: 500; padding: 20px; background: linear-gradient(135deg, rgba(173, 216, 230, 0.9), rgba(135, 206, 250, 0.9)); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 12px; color: #222; box-shadow: 0 8px 24px rgba(0,0,0,0.1);'>
                        <h4 style='margin: 0 0 12px 0; font-weight: 800;'>
                            🏆 <span style='background: linear-gradient(90deg, #007acc, #005f99); color: #fff; padding: 4px 8px; border-radius: 6px; font-weight: 800;'>$awarding_body_name</span>
                        </h4>
                        <p style='margin: 5px 0; font-weight: 600;'>
                            <strong style='background: linear-gradient(90deg, #2196f3, #64b5f6); padding: 4px 6px; border-radius: 6px; color: white; font-weight: 700;'>📩 Email:</strong> 
                            <a href='mailto:$email' style='color: #007acc; text-decoration: none; font-weight: 600;'>$email</a>
                        </p>
                        <p style='margin: 5px 0; font-weight: 600;'>
                            <strong style='background: linear-gradient(90deg, #00bcd4, #4dd0e1); color: white; padding: 4px 6px; border-radius: 6px; font-weight: 700;'>🗺️ Address:</strong> 
                            $address
                        </p>
                        <p style='margin: 5px 0; font-weight: 600;'>
                            <strong style='background: linear-gradient(90deg, #3f51b5, #7986cb); color: white; padding: 4px 6px; border-radius: 6px; font-weight: 700;'>🏙️ Location:</strong> 
                            $county, $state
                        </p>
                        <p style='margin: 5px 0; font-weight: 600;'>
                            <strong style='background: linear-gradient(90deg, #1e88e5, #42a5f5); color: white; padding: 4px 6px; border-radius: 6px; font-weight: 700;'>🌐 Web:</strong> 
                            $webpageHTMLFormatted
                        </p>
                    </div>
                ";















                
                
                $mapMarkersScript .= "
                    var marker = L.circleMarker([$x_coordinates, $y_coordinates], {
                        radius: 7, // Marker size
                        color: '#F93827', // Border color
                        fillColor: '#F93827', // Fill color
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