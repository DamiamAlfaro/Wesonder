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
        max-width: 600px;
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
    
    .info-card {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        padding: 24px;
        max-width: 920px;
        margin: 20px auto;
        line-height: 1.8;
        transition: transform 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
    }
    
    .info-card strong {
        display: block;
        font-weight: bold;
        font-size: 1.1em;
        color: #2c3e50;
        margin-bottom: 4px;
    }
    
    .info-card a {
        color: #2980b9;
        text-decoration: none;
        font-weight: 600;
    }
    
    .info-card a:hover {
        text-decoration: underline;
    }
    
    .info-item {
        background-color: #ecf0f1;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 14px;
        font-size: 17px;
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
        
        $sql = "SELECT * FROM finalized_piee_bids";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                
                $functional_url = $row['functional_url'];
                $solicitation_value = $row['solicitation_value'];
                $notice_type_element = $row['notice_type_element'];
                $due_date = $row['due_date'];
                $set_aside_code = $row['set_aside_code'];
                $contact_name = $row['contact_name'];
                $description = $row['description'];
                $subject = $row['subject'];
                $posting_date = $row['posting_date'];
                $product_service_code = $row['product_service_code'];
                $naics_code = $row['naics_code'];
                $place_of_performance = $row['place_of_performance'];
                $address = $row['address'];
                $dodaac = $row['dodaac'];
                $office_name = $row['office_name'];
                $office_address = $row['office_address'];
                $X_Coordinates = $row['X_Coordinates'];
                $Y_Coordinates = $row['Y_Coordinates'];

                $string_display = "
                    <div class='info-card'>
                        <div class='info-item'><strong>🌐 Functional URL:</strong> <a href='$functional_url' target='_blank'>$functional_url</a></div>
                        <div class='info-item'><strong>💰 Solicitation Value:</strong> $solicitation_value</div>
                        <div class='info-item'><strong>📋 Notice Type:</strong> $notice_type_element</div>
                        <div class='info-item'><strong>📅 Due Date:</strong> $due_date</div>
                        <div class='info-item'><strong>🎯 Set Aside Code:</strong> $set_aside_code</div>
                        <div class='info-item'><strong>👤 Contact Name:</strong> $contact_name</div>
                        <div class='info-item'><strong>📝 Description:</strong> $description</div>
                        <div class='info-item'><strong>📂 Subject:</strong> $subject</div>
                        <div class='info-item'><strong>🗓️ Posting Date:</strong> $posting_date</div>
                        <div class='info-item'><strong>🔧 Product Service Code:</strong> $product_service_code</div>
                        <div class='info-item'><strong>📇 NAICS Code:</strong> $naics_code</div>
                        <div class='info-item'><strong>📍 Place of Performance:</strong> $place_of_performance</div>
                        <div class='info-item'><strong>🏠 Address:</strong> $address</div>
                        <div class='info-item'><strong>🏢 DODAAC:</strong> $dodaac</div>
                        <div class='info-item'><strong>🏛️ Office Name:</strong> $office_name</div>
                        <div class='info-item'><strong>📬 Office Address:</strong> $office_address</div>
                        <div class='info-item'><strong>🗺️ Coordinates:</strong> ($X_Coordinates, $Y_Coordinates)</div>
                    </div>
                ";

                
                $mapMarkersScript .= "
                    var marker = L.circleMarker([$X_Coordinates, $Y_Coordinates], {
                        radius: 8,
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
            disableClusteringAtZoom: 40,
            maxClusterRadius: 40,
            spiderfyOnMaxZoom: true,
            showCoverageOnHover: false
        });
    
        <?php echo $mapMarkersScript; ?>
    
        map.addLayer(markers);
    </script>

</body>
</html>
