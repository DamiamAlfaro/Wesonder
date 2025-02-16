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
    <meta name="description" content="Planetbids"/>
    <link rel="icon" type="image/png" href="../../../../media/bauhaus_logo_transparent.png"/>
    <link href="../../style.css" rel="stylesheet" type="text/css">

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

    <title>Planetbids Active Bids</title>
    
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

    #DvbeForm {
        position: absolute;
        top: 40px;
        right: 40px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        height: auto;
        max-height: 650px;
        width: 240px;
        overflow-y: auto;
        font-size: 18px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    #DvbeForm .checkbox-container {
        display: flex;
        align-items: flex-start;
        margin-bottom: 15px;
    }

    #DvbeForm .checkbox-container input[type="checkbox"] {
        transform: scale(1.2);
        margin-right: 12px;
        margin-top: 6px;
    }

    #DvbeForm .checkbox-container label {
        font-size: 18px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.2;
    }
    </style>
</head>
<body>
    <form id="DvbeForm">
        <strong>Select Filters</strong><br><br>
        <div class="checkbox-container">
            <input type="checkbox" id="filter23" name="filter23">
            <label for="filter23">Show Active Bids related to Construction 🏗️</label>
        </div>
    </form>
    <div id="map"></div>

    <?php 
        $host = "localhost"; 
        $username = "u978864605_wesonder";
        $password = "Elchapillo34?nmddam";
        $dbname = "u978864605_wesonder";
        
        $conn = new mysqli($host, $username, $password, $dbname);
        
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        
        $mapMarkersScript = "
            var allMarkers = [];
            var markers = L.markerClusterGroup({
                iconCreateFunction: function(cluster) {
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
        ";

        $sql = "SELECT * FROM planetbids_active_bids";
        $result = $conn->query($sql);
        
        $coordinates_tracker = [];

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                $bid_url = addslashes($row['bid_url']);
                $awarding_body = addslashes($row['awarding_body']);
                $posted_date = addslashes($row['posted_date']);
                $bid_title = addslashes($row['bid_title']);
                $solicitation_number = addslashes($row['solicitation_number']);
                $bid_due_date = addslashes($row['bid_due_date']);
                $bid_due_time = addslashes($row['bid_due_time']);
                $county = addslashes($row['county']);
                $x_coordinates = (float)$row['x_coordinates'];
                $y_coordinates = (float)$row['y_coordinates'];
                $naics_codes = addslashes($row['naics_codes']);

                $key = "$x_coordinates,$y_coordinates";
                if (isset($coordinates_tracker[$key])) {
                    $coordinates_tracker[$key]++;
                    $x_coordinates += mt_rand(-10, 10) / 1000;
                    $y_coordinates += mt_rand(-10, 10) / 1000;
                } else {
                    $coordinates_tracker[$key] = 1;
                }

                $string_display = "
                    <div style='padding: 15px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #444; border-left: 4px solid #444;'>
                        <h2 style='margin-bottom: 8px;'>📄 $bid_title</h2>
                        <p style='margin: 4px 0; font-size: 18px;'>🏢 <strong>$awarding_body</strong></p>
                        <p style='margin: 4px 0; font-size: 18px;'>#️⃣ <strong>$solicitation_number</strong></p>
                        <p style='margin: 4px 0; font-size: 18px;'>🗓️ <strong>Posted:</strong> $posted_date</p>
                        <p style='margin: 4px 0; font-size: 18px;'>⏰ <strong>Due:</strong> $bid_due_date, $bid_due_time</p>
                        <p style='margin: 4px 0; font-size: 18px;'>📍 <strong>County:</strong> $county</p>
                        <p style='margin: 4px 0; font-size: 18px;'>🔢 <strong>NAICS:</strong> $naics_codes</p>
                        <a href='$bid_url' target='_blank' style='color: #444; text-decoration: underline; font-size: 18px;'>🔗 View Bid</a>
                    </div>
                ";

                $mapMarkersScript .= "
                    var marker = L.circleMarker([$x_coordinates, $y_coordinates], {
                        radius: 7,
                        color: '#3388ff',
                        fillColor: '#3388ff',
                        fillOpacity: 0.5
                    }).bindPopup(" . json_encode($string_display) . ");

                    marker.naics_codes = '$naics_codes';
                    allMarkers.push(marker);
                    markers.addLayer(marker);
                ";
            }
        } else {
            echo "No results found.";
        }
        
        $conn->close();
    ?>

    <script>
        var map = L.map('map', {
            renderer: L.canvas()
        }).setView([37.7749, -122.4194], 5);

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        <?php echo $mapMarkersScript; ?>
        map.addLayer(markers);

        document.getElementById('filter23').addEventListener('change', function() {
            markers.clearLayers();
            if (this.checked) {
                allMarkers.forEach(function(marker) {
                    if (marker.naics_codes.split(',').some(code => code.startsWith('23'))) {
                        markers.addLayer(marker);
                    }
                });
            } else {
                allMarkers.forEach(function(marker) {
                    markers.addLayer(marker);
                });
            }
        });
    </script>
</body>
</html>
