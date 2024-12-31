<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Projects"/>
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

    <title>DVBE/SB</title>
    
    <style>
        
        #map {
            height: 100vh;
            width: 100%;
            position: relative;
        }
        
        #DvbeForm {
            position: absolute;
            top: 20px; /* Distance from the top */
            right: 20px; /* Distance from the right */
            background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white background */
            padding: 10px; /* Padding for better spacing */
            border-radius: 8px; /* Rounded corners */
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); /* Add a slight shadow */
            z-index: 1000; /* Ensure it is above the map */
            height: auto; /* Fixed height */
            max-height: 650px;
            width: 240px; /* Fixed width */
            overflow-y: auto; /* Enable scrolling for vertical overflow */
            font-size: 18px;
            font-family: Optima;
        }
        
        #DvbeForm .checkbox-container {
            display: flex;
            align-items: flex-start; /* Align checkbox and text */
            margin-bottom: 15px; /* Add spacing between rows */
        }
        
        #DvbeForm .checkbox-container input[type="checkbox"] {
            transform: scale(1.2);
            margin-right: 10px; /* Add spacing between checkbox and label */
            margin-top: 2px; /* Adjust alignment with text */
        }
        
        #DvbeForm .checkbox-container label {
            font-size: 18px; /* Adjust font size */
            font-family: Optima;
            line-height: 1.2; /* Add better spacing for multiple lines */
        }
        
        .popup-content {
            max-width: 250px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        .popup-classifications {
            white-space: pre-wrap;
        }

        
    </style>
    


</head>
<body>
    
    <form id="DvbeForm">
        <strong>Select Construction License</strong><br><br>
        
        <div class="checkbox-container">
            <input type="checkbox" id="license1" name="license1" value="DVBE" onclick="DvbeCheckboxingClick(this)">
            <label for="license1">Disabled Veteran Business Enterprise</label>
        </div>
        
        <div class="checkbox-container">
            <input type="checkbox" id="license2" name="license2" value="SB" onclick="DvbeCheckboxingClick(this)">
            <label for="license2">Small Business</label>
        </div>
        
        <div class="checkbox-container">
            <input type="checkbox" id="license3" name="license3" value="SB(Micro)" onclick="DvbeCheckboxingClick(this)">
            <label for="license3">Small Business (Micro)</label>
        </div>
    </form>



    


    <?php

        
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
        
        var markerGroups = {};
        
        function DvbeCheckboxingClick(checkbox) {
            // Prepare the data to send to the server
            const formData = new FormData();
            formData.append('checkbox_name', checkbox.name);
            formData.append('checkbox_value', checkbox.value);
            formData.append('checkbox_checked', checkbox.checked);
        
            if (checkbox.checked) {

                fetch('loading_dvbes.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json()) // Change to `.json()` if the server returns JSON
                .then(data => {
                    if (data.status === 'success') {
                        
                        const dvbes = data.dvbes;
                        
                        var markers = L.markerClusterGroup({
                            iconCreateFunction: function(cluster) {
                                // Get the count of markers in the cluster
                                var count = cluster.getChildCount();
                        
                                // Define border and fill colors dynamically
                                var clusterFillColor = count < 10 ? '#68c4cc' : count < 50 ? '#ffa500' : '#ff5733'; // Fill colors
                                var clusterBorderColor = count < 10 ? '#1f5572' : count < 50 ? '#cc8400' : '#b53324'; // Border colors
                        
                                // Create the custom cluster icon
                                return L.divIcon({
                                    html: `
                                        <div style="
                                            background-color: ${clusterFillColor}; 
                                            border: 3px solid ${clusterBorderColor}; 
                                            border-radius: 50%; 
                                            color: black; 
                                            text-align: center; 
                                            line-height: 35px; 
                                            width: 35px; 
                                            height: 35px;
                                            font-weight: bold;
                                            font-size: 13px;
                                        ">
                                            ${count}
                                        </div>`,
                                    className: 'cluster-icon',
                                    iconSize: [20, 20] // Size of the cluster icon
                                });
                            }
                        });

                        
                        dvbes.forEach(dvbe_entity => {
                            const certification_id = dvbe_entity.Certification_ID;
                            const legal_business_name = dvbe_entity.Legal_Business_Name;
                            const doing_business_as_1 = dvbe_entity.Doing_Business_As_1;
                            const other_dbas = dvbe_entity.Other_DBAs;
                            const certification_type = dvbe_entity.Certification_Type;
                            const start_date = dvbe_entity.Start_Date;
                            const end_date = dvbe_entity.End_Date;
                            const email_id = dvbe_entity.Email_ID;
                            const first_name = dvbe_entity.First_Name;
                            const last_name = dvbe_entity.Last_Name;
                            const urlid = dvbe_entity.URLID;
                            const telephone = dvbe_entity.Telephone;
                            const keywords = dvbe_entity.Keywords;
                            const license = dvbe_entity.License;
                            const industry_type = dvbe_entity.Industry_Type;
                            const ethnicity = dvbe_entity.Ethnicity;
                            const race = dvbe_entity.Race;
                            const gender_identity = dvbe_entity.Gender_Identity;
                            const lgbqtia = dvbe_entity.LGBQTIA;
                            const complete_address = dvbe_entity.CompleteAddress;
                            const x_coordinates = parseFloat(dvbe_entity.x_coordinates);
                            const y_coordinates = parseFloat(dvbe_entity.y_coordinates);
                        
                            
                            const popupContent = `
                                <div class="popup-content">
                                    <strong>Name: </strong> ${legal_business_name}<br>
                                    <strong>Certification Type: </strong> ${certification_type}<br>
                                    <strong>Email Address:</strong> ${email_id}<br>
                                    <strong>Phone Number:</strong> ${telephone}<br>
                                    <strong>Construction Licenses:</strong> ${license}<br>
                                    <strong>Classifications:</strong> 
                                    <div class="popup-classifications">${keywords}</div>
                                    <strong>Industry Type:</strong> ${industry_type}<br>
                                    <strong>Address:</strong> ${complete_address}<br>
                                </div>
                            `;
                           
                            var marker = L.circleMarker([x_coordinates, y_coordinates], {
                                radius: 7, // Marker size
                                color: '#1f5572', // Border color
                                fillColor: '#68c4cc', // Fill color
                                fillOpacity: 0.5 // Opacity
                                }).bindPopup(popupContent);
                                markers.addLayer(marker);
                        });
                        
                        map.addLayer(markers);
                        markerGroups[checkbox.name] = markers;
        
                    } else if (data.status === 'unchecked') {
                        console.log(data.message);
                    } else {
                        console.error('Unexpected response:', data);
                    }
                })
                .catch(error => console.error('Error:', error));
                
            } else {
                
                if (markerGroups[checkbox.name]) {
                    map.removeLayer(markerGroups[checkbox.name]); // Remove the marker group from the map
                    delete markerGroups[checkbox.name]; // Remove the reference from the object
                }
                
                
            }
        }
        
        
    </script>


</body>
</html>
;
