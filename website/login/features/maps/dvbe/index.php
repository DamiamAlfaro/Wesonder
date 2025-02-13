<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Damiam Alfaro"/>
    <meta name="description" content="WESONDER Projects"/>
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;;
        }
        
        #DvbeForm .checkbox-container {
            display: flex;
            align-items: flex-start; /* Align checkbox and text */
            margin-bottom: 15px; /* Add spacing between rows */
        }
        
        #DvbeForm .checkbox-container input[type="checkbox"] {
            transform: scale(1.2);
            margin-right: 12px; /* Add spacing between checkbox and label */
            margin-top: 6px; /* Adjust alignment with text */
        }
        
        #DvbeForm .checkbox-container label {
            font-size: 18px; /* Adjust font size */
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;;
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
            <label for="license1">Disabled Veteran Business Enterprise (DVBE)</label>
        </div>
        
        <div class="checkbox-container">
            <input type="checkbox" id="license2" name="license2" value="SB" onclick="DvbeCheckboxingClick(this)">
            <label for="license2">Small Business (SB)</label>
        </div>
        
        <div class="checkbox-container">
            <input type="checkbox" id="license3" name="license3" value="SB(Micro)" onclick="DvbeCheckboxingClick(this)">
            <label for="license3">Small Business (SB - Micro)</label>
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
                        
                                // Define slightly darker, yet still soft fill and border colors dynamically
                                var clusterFillColor = count < 10 ? '#3A7D44' : count < 50 ? '#497D74' : '#818C78'; // Slightly darker fill colors
                                var clusterBorderColor = count < 10 ? '#3F4F44' : count < 50 ? '#71BBB2' : '#A7B49E'; // Slightly darker border colors
                        
                                // Create the custom cluster icon with a minimalistic design
                                return L.divIcon({
                                    html: `
                                        <div style="
                                            background-color: ${clusterFillColor}; 
                                            border: 2px solid ${clusterBorderColor}; 
                                            border-radius: 50%; 
                                            color: #333; 
                                            text-align: center; 
                                            line-height: 35px; 
                                            width: 35px; 
                                            height: 35px;
                                            font-weight: 500;
                                            font-size: 14px;
                                            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                                        ">
                                            ${count}
                                        </div>`,
                                    className: 'cluster-icon',
                                    iconSize: [30, 30] // Slightly larger for better visibility
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
                                <div class="popup-content" style="
                                    max-width: 300px;
                                    max-height: 400px;
                                    overflow-y: auto;
                                    background: #ffffff;
                                    border-radius: 12px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                                    padding: 16px;
                                    line-height: 1.6;
                                    font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif;
                                    font-size: 24px;
                                    color: #2c3e50;
                                ">
                                    <div style="margin-bottom: 10px; font-size: 16px;"><strong>🏢 Name:</strong> ${legal_business_name}</div>
                                    <div style="margin-bottom: 10px; font-size: 16px;"><strong>📋 Certification Type:</strong> ${certification_type}</div>
                                    <div style="margin-bottom: 10px; font-size: 16px;"><strong>📧 Email:</strong> <a href="mailto:${email_id}" style="color: #2980b9; text-decoration: none;">${email_id}</a></div>
                                    <div style="margin-bottom: 10px; font-size: 16px;"><strong>📞 Phone:</strong> ${telephone}</div>
                                    <div style="margin-bottom: 10px; font-size: 16px;"><strong>🔧 Licenses:</strong> ${license}</div>
                                    <div style="margin-bottom: 10px; font-size: 16px;"><strong>🏷️ Classifications:</strong> 
                                        <div class="popup-classifications" style="background-color: #ecf0f1; padding: 8px; border-radius: 6px;">
                                            ${keywords}
                                        </div>
                                    </div>
                                    <div style="margin-bottom: 10px; font-size: 16px"><strong>🏗️ Industry Type:</strong> ${industry_type}</div>
                                    <div style="margin-bottom: 10px; font-size: 16px"><strong>📍 Address:</strong> ${complete_address}</div>
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