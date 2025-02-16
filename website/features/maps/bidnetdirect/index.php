<?php
    // Enable error reporting
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    ini_set('log_errors', 1);
    ini_set('error_log', __DIR__ . '/php-error.log'); // Log errors to a file

    // Custom error handler
    set_error_handler(function ($errno, $errstr, $errfile, $errline) {
        $errorMessage = "Error: $errstr in $errfile on line $errline";
        error_log($errorMessage);
        
        // Display a user-friendly error message
        echo "<div style='color: red; font-weight: bold; margin: 20px;'>
                An error occurred: <br>
                <strong>$errstr</strong> <br>
                Please contact <a href='mailto:support@wesonder.com'>support@wesonder.com</a> with this message.
              </div>";
        
        // Logout option
        echo "<div style='margin: 20px;'>
                <a href='/logout.php' style='color: blue; text-decoration: underline;'>Click here to log out</a>
              </div>";

        exit;
    });

    // Ensure the user is logged in
    require_once '../../auth_check.php';

?>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Map Display"/>
    <link rel="icon" type="image/png" href="../../../../media/bauhaus_logo_transparent.png"/>
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
    
    .marker-cluster {
        background-clip: padding-box;
        border-radius: 50%;
        color: black;
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        line-height: 40px;
        cursor: pointer;
    }
    
    .marker-cluster-small {
        background-color: #90ee90;
        width: 40px;
        height: 40px;
    }
    
    .marker-cluster-medium {
        background-color: #ffa500;
        width: 50px;
        height: 50px;
    }
    
    .marker-cluster-large {
        background-color: #ff4500;
        width: 60px;
        height: 60px;
    }
    
    .leaflet-popup-content {
        max-width: 300px;
        white-space: normal;
        overflow-wrap: break-word;
    }

    .leaflet-popup-content-wrapper {
        max-height: 400px;
        overflow-y: auto;
    }

    .leaflet-popup-content a {
        word-wrap: break-word;
        color: blue;
        text-decoration: underline;
    }
    
        /* Go Back Button */
    #back-button {
        position: absolute;
        top: 20px;
        left: 20px;
        background: #007acc;
        color: white;
        padding: 10px 15px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        z-index: 1000; /* Ensure it's above other elements */
    }

    #back-button:hover {
        background: #005f99;
    }
    
    </style>


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
        
        $mapMarkersScript = "";
        
        $sql = "SELECT * FROM finalized_bidnetdirect_bids WHERE SolicitationNumber != 'none'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                
                $awarding_body = addslashes($row['AwardingBody']);
                $url = addslashes($row['AwardingBodyLink']);
                $county = addslashes($row['County']);
                $x_coordinates = $row['X_Coordinates'];
                $y_coordinates = $row['Y_Coordinates'];
                $solicitation_number = $row['SolicitationNumber'];
                $solicitation_name = $row['BidTitle'];
                $opening_date = $row['PostedDate'];
                $closing_date = $row['DueDate'];
                $solicitation_url = $row['BidLink'];
                $closing_time = $row['DueTime'];
                
                $string_display = "
                    <div style='font-family: \"Roboto\", sans-serif; color: #2f3640; padding: 12px; background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                        <h3 style='margin: 0 0 8px; font-size: 20px; color: #273c75;'>🏛️ $awarding_body</h3>
                        <p style='margin: 6px 0;'><strong>🔗 URL:</strong> <a href='$url' target='_blank' style='color: #0097e6; text-decoration: none;'>Visit Site</a></p>
                        <p style='margin: 4px 0;'><strong>📄 Solicitation #:</strong> <span style='color: #353b48;'>$solicitation_number</span></p>
                        <p style='margin: 4px 0;'><strong>📝 Name:</strong> <span style='color: #353b48;'>$solicitation_name</span></p>
                        <p style='margin: 4px 0;'><strong>🗓️ Opens:</strong> <span style='color: #4cd137;'>$opening_date</span></p>
                        <p style='margin: 4px 0;'><strong>⏳ Closes:</strong> <span style='color: #e84118;'>$closing_date</span> at <strong>$closing_time</strong></p>
                        <p style='margin: 6px 0;'><strong>📥 Details:</strong> <a href='$solicitation_url' target='_blank' style='color: #0097e6; text-decoration: none;'>View Solicitation</a></p>
                    </div>
                ";
                
                $mapMarkersScript .= "
                    var marker = L.circleMarker([$x_coordinates, $y_coordinates], {
                        radius: 6,
                        color: '#3388ff',
                        fillColor: '#3388ff',
                        fillOpacity: 0.5
                    }).bindPopup(" . json_encode($string_display) . ");
                    markers.addLayer(marker);
                ";
            }
        } else {
            echo "No results found.";
        }
        
        $conn->close();
    ?>

    <button id="back-button" onclick="history.back();">⬅ Go Back</button>

    <div id="map"></div>
    
    <script>
        var map = L.map('map', {
            renderer: L.canvas()
        }).setView([37.7749, -122.4194], 5);
    
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
    
        var markers = L.markerClusterGroup({
            disableClusteringAtZoom: 18,
            maxClusterRadius: 40,
            spiderfyOnMaxZoom: true,
            showCoverageOnHover: false,
            iconCreateFunction: function(cluster) {
                var childCount = cluster.getChildCount();
                var c = 'marker-cluster-';
                if (childCount < 5) {
                    c += 'small';
                } else if (childCount < 25) {
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
    
        <?php echo $mapMarkersScript; ?>
        
        map.addLayer(markers);
    </script>

</body>
</html>
