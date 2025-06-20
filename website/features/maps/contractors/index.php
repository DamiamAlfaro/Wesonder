
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

    <title>Contractors/Subcontractors</title>
    
    <style>
        
        #map {
            height: 100vh;
            width: 100%;
            position: relative;
        }
        
        #licenseForm {
            position: absolute;
            background: linear-gradient(145deg, #f3f4f6, #ffffff);
            top: 20px; /* Distance from the top */
            right: 20px; /* Distance from the right */
            background-color: rgba(255, 255, 255, 0.9); /* Semi-transparent white background */
            padding: 20px; /* Padding for better spacing */
            border-radius: 12px; /* Rounded corners */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* Add a slight shadow */
            z-index: 1000; /* Ensure it is above the map */
            height: auto; /* Fixed height */
            max-height: 650px;
            width: 240px; /* Fixed width */
            overflow-y: auto; /* Enable scrolling for vertical overflow */
            font-size: 18px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        
        #licenseForm input[type="checkbox"] {
            transform: scale(1.2);
            margin-right: 10px; /* Add spacing between checkbox and label */
            width: 16px;
            height: 16px;
            border: 2px solid #1f5572;
            border-radius: 4px;
            position: relative;
            cursor: pointer;
        }
        
        #licenseForm input[type="checkbox"]:checked {
            background-color: #1f5572;
        }

        
        #licenseForm label {
            font-size: 16px;
            color: #333;
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
        <!-- Go Back Button -->
    <button id="back-button" onclick="history.back();">⬅ Go Back</button>
    
    <form id="licenseForm">
        
        <strong>Select Construction License</strong><br><br>
        
        <input type="checkbox" id="license1" name="license1" value="A" onclick="LicenseCheckboxingClick(this)">
        <label for="license1">A - General Engineering Contractor</label><br><br>
        
        <input type="checkbox" id="license1" name="license1" value="B" onclick="LicenseCheckboxingClick(this)">
        <label for="license1">B - General Building Contractor</label><br><br>
        
        <input type="checkbox" id="license1" name="license1" value="C2" onclick="LicenseCheckboxingClick(this)">
        <label for="license1">C-2 - Insulation and Acoustical Contractor</label><br><br>
    
        <input type="checkbox" id="license2" name="license2" value="C4" onclick="LicenseCheckboxingClick(this)">
        <label for="license2">C-4 - Boiler, Hot Water Heating and Steam Fitting Contractor</label><br><br>
    
        <input type="checkbox" id="license3" name="license3" value="C5" onclick="LicenseCheckboxingClick(this)">
        <label for="license3">C-5 - Framing and Rough Carpentry Contractor</label><br><br>
    
        <input type="checkbox" id="license4" name="license4" value="C6" onclick="LicenseCheckboxingClick(this)">
        <label for="license4">C-6 - Cabinet, Millwork and Finish Carpentry Contractor</label><br><br>
    
        <input type="checkbox" id="license5" name="license5" value="C7" onclick="LicenseCheckboxingClick(this)">
        <label for="license5">C-7 - Low Voltage Systems Contractor</label><br><br>
    
        <input type="checkbox" id="license6" name="license6" value="C8" onclick="LicenseCheckboxingClick(this)">
        <label for="license6">C-8 - Concrete Contractor</label><br><br>
    
        <input type="checkbox" id="license7" name="license7" value="C9" onclick="LicenseCheckboxingClick(this)">
        <label for="license7">C-9 - Drywall Contractor</label><br><br>
    
        <input type="checkbox" id="license8" name="license8" value="C10" onclick="LicenseCheckboxingClick(this)">
        <label for="license8">C-10 - Electrical Contractor</label><br><br>
    
        <input type="checkbox" id="license9" name="license9" value="C11" onclick="LicenseCheckboxingClick(this)">
        <label for="license9">C-11 - Elevator Contractor</label><br><br>
    
        <input type="checkbox" id="license10" name="license10" value="C12" onclick="LicenseCheckboxingClick(this)">
        <label for="license10">C-12 - Earthwork and Paving Contractors</label><br><br>
    
        <input type="checkbox" id="license11" name="license11" value="C13" onclick="LicenseCheckboxingClick(this)">
        <label for="license11">C-13 - Fencing Contractor</label><br><br>
    
        <input type="checkbox" id="license12" name="license12" value="C15" onclick="LicenseCheckboxingClick(this)">
        <label for="license12">C-15 - Flooring and Floor Covering Contractors</label><br><br>
    
        <input type="checkbox" id="license13" name="license13" value="C16" onclick="LicenseCheckboxingClick(this)">
        <label for="license13">C-16 - Fire Protection Contractor</label><br><br>
    
        <input type="checkbox" id="license14" name="license14" value="C17" onclick="LicenseCheckboxingClick(this)">
        <label for="license14">C-17 - Glazing Contractor</label><br><br>
    
        <input type="checkbox" id="license15" name="license15" value="C20" onclick="LicenseCheckboxingClick(this)">
        <label for="license15">C-20 - Warm-Air Heating, Ventilating and Air-Conditioning Contractor</label><br><br>
    
        <input type="checkbox" id="license16" name="license16" value="C21" onclick="LicenseCheckboxingClick(this)">
        <label for="license16">C-21 - Building Moving/Demolition Contractor</label><br><br>
    
        <input type="checkbox" id="license17" name="license17" value="C22" onclick="LicenseCheckboxingClick(this)">
        <label for="license17">C-22 - Asbestos Abatement Contractor</label><br><br>
    
        <input type="checkbox" id="license18" name="license18" value="C23" onclick="LicenseCheckboxingClick(this)">
        <label for="license18">C-23 - Ornamental Metal Contractor</label><br><br>
    
        <input type="checkbox" id="license19" name="license19" value="C27" onclick="LicenseCheckboxingClick(this)">
        <label for="license19">C-27 - Landscaping Contractor</label><br><br>
    
        <input type="checkbox" id="license20" name="license20" value="C28" onclick="LicenseCheckboxingClick(this)">
        <label for="license20">C-28 - Lock and Security Equipment Contractor</label><br><br>
    
        <input type="checkbox" id="license21" name="license21" value="C29" onclick="LicenseCheckboxingClick(this)">
        <label for="license21">C-29 - Masonry Contractor</label><br><br>
    
        <input type="checkbox" id="license22" name="license22" value="C31" onclick="LicenseCheckboxingClick(this)">
        <label for="license22">C-31 - Construction Zone Traffic Control Contractor</label><br><br>
    
        <input type="checkbox" id="license23" name="license23" value="C32" onclick="LicenseCheckboxingClick(this)">
        <label for="license23">C-32 - Parking and Highway Improvement Contractor</label><br><br>
    
        <input type="checkbox" id="license24" name="license24" value="C33" onclick="LicenseCheckboxingClick(this)">
        <label for="license24">C-33 - Painting and Decorating Contractor</label><br><br>
    
        <input type="checkbox" id="license25" name="license25" value="C34" onclick="LicenseCheckboxingClick(this)">
        <label for="license25">C-34 - Pipeline Contractor</label><br><br>
    
        <input type="checkbox" id="license26" name="license26" value="C35" onclick="LicenseCheckboxingClick(this)">
        <label for="license26">C-35 - Lathing and Plastering Contractor</label><br><br>
    
        <input type="checkbox" id="license27" name="license27" value="C36" onclick="LicenseCheckboxingClick(this)">
        <label for="license27">C-36 - Plumbing Contractor</label><br><br>
    
        <input type="checkbox" id="license28" name="license28" value="C38" onclick="LicenseCheckboxingClick(this)">
        <label for="license28">C-38 - Refrigeration Contractor</label><br><br>
    
        <input type="checkbox" id="license29" name="license29" value="C39" onclick="LicenseCheckboxingClick(this)">
        <label for="license29">C-39 - Roofing Contractor</label><br><br>
    
        <input type="checkbox" id="license30" name="license30" value="C42" onclick="LicenseCheckboxingClick(this)">
        <label for="license30">C-42 - Sanitation System Contractor</label><br><br>
    
        <input type="checkbox" id="license31" name="license31" value="C43" onclick="LicenseCheckboxingClick(this)">
        <label for="license31">C-43 - Sheet Metal Contractor</label><br><br>
    
        <input type="checkbox" id="license32" name="license32" value="C45" onclick="LicenseCheckboxingClick(this)">
        <label for="license32">C-45 - Sign Contractor</label><br><br>
    
        <input type="checkbox" id="license33" name="license33" value="C46" onclick="LicenseCheckboxingClick(this)">
        <label for="license33">C-46 - Solar Contractor</label><br><br>
    
        <input type="checkbox" id="license34" name="license34" value="C47" onclick="LicenseCheckboxingClick(this)">
        <label for="license34">C-47 - General Manufactured Housing Contractor</label><br><br>
    
        <input type="checkbox" id="license35" name="license35" value="C49" onclick="LicenseCheckboxingClick(this)">
        <label for="license35">C-49 - Tree and Palm Contractor</label><br><br>
    
        <input type="checkbox" id="license36" name="license36" value="C50" onclick="LicenseCheckboxingClick(this)">
        <label for="license36">C-50 - Reinforcing Steel Contractor</label><br><br>
    
        <input type="checkbox" id="license37" name="license37" value="C51" onclick="LicenseCheckboxingClick(this)">
        <label for="license37">C-51 - Structural Steel Contractor</label><br><br>
    
        <input type="checkbox" id="license38" name="license38" value="C53" onclick="LicenseCheckboxingClick(this)">
        <label for="license38">C-53 - Swimming Pool Contractor</label><br><br>
    
        <input type="checkbox" id="license39" name="license39" value="C54" onclick="LicenseCheckboxingClick(this)">
        <label for="license39">C-54 - Ceramic and Mosaic Tile Contractor</label><br><br>
    
        <input type="checkbox" id="license40" name="license40" value="C55" onclick="LicenseCheckboxingClick(this)">
        <label for="license40">C-55 - Water Conditioning Contractor</label><br><br>
        
        <input type="checkbox" id="license41" name="license41" value="C57" onclick="LicenseCheckboxingClick(this)">
        <label for="license41">C-57 - Well Drilling Contractor</label><br><br>
    
        <input type="checkbox" id="license42" name="license42" value="C60" onclick="LicenseCheckboxingClick(this)">
        <label for="license42">C-60 - Welding Contractor</label><br><br>
    
        <input type="checkbox" id="license43" name="license43" value="D1" onclick="LicenseCheckboxingClick(this)">
        <label for="license43">D-1 - Architectural Porcelain (Now under D-64)</label><br><br>
    
        <input type="checkbox" id="license44" name="license44" value="D2" onclick="LicenseCheckboxingClick(this)">
        <label for="license44">D-2 - Asbestos Fabrication (Now under C-2)</label><br><br>
    
        <input type="checkbox" id="license45" name="license45" value="D3" onclick="LicenseCheckboxingClick(this)">
        <label for="license45">D-3 - Awnings</label><br><br>
    
        <input type="checkbox" id="license46" name="license46" value="D4" onclick="LicenseCheckboxingClick(this)">
        <label for="license46">D-4 - Central Vacuum Systems</label><br><br>
    
        <input type="checkbox" id="license47" name="license47" value="D5" onclick="LicenseCheckboxingClick(this)">
        <label for="license47">D-5 - Communication Equipment (Converted to C-7)</label><br><br>
    
        <input type="checkbox" id="license48" name="license48" value="D6" onclick="LicenseCheckboxingClick(this)">
        <label for="license48">D-6 - Concrete Related Services</label><br><br>
    
        <input type="checkbox" id="license49" name="license49" value="D7" onclick="LicenseCheckboxingClick(this)">
        <label for="license49">D-7 - Conveyors-Cranes (Now under D-21)</label><br><br>
    
        <input type="checkbox" id="license50" name="license50" value="D8" onclick="LicenseCheckboxingClick(this)">
        <label for="license50">D-8 - Doors and Door Services (Now under D-28)</label><br><br>
    
        <input type="checkbox" id="license51" name="license51" value="D9" onclick="LicenseCheckboxingClick(this)">
        <label for="license51">D-9 - Drilling, Blasting and Oil Field Work</label><br><br>
    
        <input type="checkbox" id="license52" name="license52" value="D10" onclick="LicenseCheckboxingClick(this)">
        <label for="license52">D-10 - Elevated Floors</label><br><br>
    
        <input type="checkbox" id="license53" name="license53" value="D11" onclick="LicenseCheckboxingClick(this)">
        <label for="license53">D-11 - Fencing (Converted to C-13)</label><br><br>
    
        <input type="checkbox" id="license54" name="license54" value="D12" onclick="LicenseCheckboxingClick(this)">
        <label for="license54">D-12 - Synthetic Products</label><br><br>
    
        <input type="checkbox" id="license55" name="license55" value="D13" onclick="LicenseCheckboxingClick(this)">
        <label for="license55">D-13 - Fire Extinguisher Systems (Now under C-16)</label><br><br>
    
        <input type="checkbox" id="license56" name="license56" value="D14" onclick="LicenseCheckboxingClick(this)">
        <label for="license56">D-14 - Floor Covering (Converted to C-15)</label><br><br>
    
        <input type="checkbox" id="license57" name="license57" value="D15" onclick="LicenseCheckboxingClick(this)">
        <label for="license57">D-15 - Furnaces (Now under "A" or C-20)</label><br><br>
    
        <input type="checkbox" id="license58" name="license58" value="D16" onclick="LicenseCheckboxingClick(this)">
        <label for="license58">D-16 - Hardware, Locks and Safes</label><br><br>
    
        <input type="checkbox" id="license59" name="license59" value="D17" onclick="LicenseCheckboxingClick(this)">
        <label for="license59">D-17 - Industrial Insulation (Now under C-2)</label><br><br>
    
        <input type="checkbox" id="license60" name="license60" value="D18" onclick="LicenseCheckboxingClick(this)">
        <label for="license60">D-18 - Prison and Jail Equipment (Under relevant class)</label><br><br>
    
        <input type="checkbox" id="license61" name="license61" value="D19" onclick="LicenseCheckboxingClick(this)">
        <label for="license61">D-19 - Land Clearing (Now under C-12 or "A" if license is required)</label><br><br>
    
        <input type="checkbox" id="license62" name="license62" value="D20" onclick="LicenseCheckboxingClick(this)">
        <label for="license62">D-20 - Lead Burning and Fabrication (Now under D-64)</label><br><br>
    
        <input type="checkbox" id="license63" name="license63" value="D21" onclick="LicenseCheckboxingClick(this)">
        <label for="license63">D-21 - Machinery and Pumps</label><br><br>
    
        <input type="checkbox" id="license64" name="license64" value="D22" onclick="LicenseCheckboxingClick(this)">
        <label for="license64">D-22 - Marble (Now under C-29)</label><br><br>
    
        <input type="checkbox" id="license65" name="license65" value="D23" onclick="LicenseCheckboxingClick(this)">
        <label for="license65">D-23 - Medical Gas Systems (Now under C-36)</label><br><br>
        
        <input type="checkbox" id="license66" name="license66" value="D24" onclick="LicenseCheckboxingClick(this)">
        <label for="license66">D-24 - Metal Products</label><br><br>
    
        <input type="checkbox" id="license67" name="license67" value="D25" onclick="LicenseCheckboxingClick(this)">
        <label for="license67">D-25 - Mirrors and Fixed Glass (Now under C-17)</label><br><br>
    
        <input type="checkbox" id="license68" name="license68" value="D26" onclick="LicenseCheckboxingClick(this)">
        <label for="license68">D-26 - Mobile Home Installation and Repairs (Converted to C-47)</label><br><br>
    
        <input type="checkbox" id="license69" name="license69" value="D27" onclick="LicenseCheckboxingClick(this)">
        <label for="license69">D-27 - Movable Partitions (Now under D-34)</label><br><br>
    
        <input type="checkbox" id="license70" name="license70" value="D28" onclick="LicenseCheckboxingClick(this)">
        <label for="license70">D-28 - Doors, Gates and Activating Devices</label><br><br>
    
        <input type="checkbox" id="license71" name="license71" value="D29" onclick="LicenseCheckboxingClick(this)">
        <label for="license71">D-29 - Paperhanging</label><br><br>
    
        <input type="checkbox" id="license72" name="license72" value="D30" onclick="LicenseCheckboxingClick(this)">
        <label for="license72">D-30 - Pile Driving and Pressure Foundation Jacking</label><br><br>
    
        <input type="checkbox" id="license73" name="license73" value="D31" onclick="LicenseCheckboxingClick(this)">
        <label for="license73">D-31 - Pole Installation and Maintenance</label><br><br>
    
        <input type="checkbox" id="license74" name="license74" value="D32" onclick="LicenseCheckboxingClick(this)">
        <label for="license74">D-32 - Power Nailing and Fastening (Now under D-64)</label><br><br>
    
        <input type="checkbox" id="license75" name="license75" value="D33" onclick="LicenseCheckboxingClick(this)">
        <label for="license75">D-33 - Precast Concrete Stairs (Now under C-29)</label><br><br>
    
        <input type="checkbox" id="license76" name="license76" value="D34" onclick="LicenseCheckboxingClick(this)">
        <label for="license76">D-34 - Prefabricated Equipment</label><br><br>
    
        <input type="checkbox" id="license77" name="license77" value="D35" onclick="LicenseCheckboxingClick(this)">
        <label for="license77">D-35 - Pool and Spa Maintenance</label><br><br>
    
        <input type="checkbox" id="license78" name="license78" value="D36" onclick="LicenseCheckboxingClick(this)">
        <label for="license78">D-36 - Rigging and Rig Building (Now under "A")</label><br><br>
    
        <input type="checkbox" id="license79" name="license79" value="D37" onclick="LicenseCheckboxingClick(this)">
        <label for="license79">D-37 - Safes and Vaults (Now under D-16)</label><br><br>
    
        <input type="checkbox" id="license80" name="license80" value="D38" onclick="LicenseCheckboxingClick(this)">
        <label for="license80">D-38 - Sand and Water Blasting</label><br><br>
    
        <input type="checkbox" id="license81" name="license81" value="D39" onclick="LicenseCheckboxingClick(this)">
        <label for="license81">D-39 - Scaffolding</label><br><br>
    
        <input type="checkbox" id="license82" name="license82" value="D40" onclick="LicenseCheckboxingClick(this)">
        <label for="license82">D-40 - Service Station Equipment and Maintenance</label><br><br>
    
        <input type="checkbox" id="license83" name="license83" value="D41" onclick="LicenseCheckboxingClick(this)">
        <label for="license83">D-41 - Siding and Decking</label><br><br>
    
        <input type="checkbox" id="license84" name="license84" value="D42" onclick="LicenseCheckboxingClick(this)">
        <label for="license84">D-42 - Non-Electrical Sign Installation</label><br><br>
    
        <input type="checkbox" id="license85" name="license85" value="D43" onclick="LicenseCheckboxingClick(this)">
        <label for="license85">D-43 - Soil Grouting (Now under C-32, C-12 or "A")</label><br><br>
    
        <input type="checkbox" id="license86" name="license86" value="D44" onclick="LicenseCheckboxingClick(this)">
        <label for="license86">D-44 - Sprinklers (Now under D-12)</label><br><br>
    
        <input type="checkbox" id="license87" name="license87" value="D45" onclick="LicenseCheckboxingClick(this)">
        <label for="license87">D-45 - Staff and Stone (Now under C-29)</label><br><br>
    
        <input type="checkbox" id="license88" name="license88" value="D46" onclick="LicenseCheckboxingClick(this)">
        <label for="license88">D-46 - Steeple Jack Work (under relevant class)</label><br><br>
    
        <input type="checkbox" id="license89" name="license89" value="D47" onclick="LicenseCheckboxingClick(this)">
        <label for="license89">D-47 - Tennis Court Surfacing (Now under C-12 or "A")</label><br><br>
    
        <input type="checkbox" id="license90" name="license90" value="D48" onclick="LicenseCheckboxingClick(this)">
        <label for="license90">D-48 - Theater and School Equipment (Now under D-34)</label><br><br>
    
        <input type="checkbox" id="license91" name="license91" value="D49" onclick="LicenseCheckboxingClick(this)">
        <label for="license91">D-49 – Tree Service (Converted to C-49)</label><br><br>
    
        <input type="checkbox" id="license92" name="license92" value="D50" onclick="LicenseCheckboxingClick(this)">
        <label for="license92">D-50 - Suspended Ceilings</label><br><br>
    
        <input type="checkbox" id="license93" name="license93" value="D51" onclick="LicenseCheckboxingClick(this)">
        <label for="license93">D-51 - Waterproofing and Weatherproofing (under relevant class)</label><br><br>
    
        <input type="checkbox" id="license94" name="license94" value="D52" onclick="LicenseCheckboxingClick(this)">
        <label for="license94">D-52 - Window Coverings</label><br><br>
    
        <input type="checkbox" id="license95" name="license95" value="D53" onclick="LicenseCheckboxingClick(this)">
        <label for="license95">D-53 - Wood Tanks</label><br><br>
    
        <input type="checkbox" id="license96" name="license96" value="D54" onclick="LicenseCheckboxingClick(this)">
        <label for="license96">D-54 - Rockscaping (Now under C-15 or C-27)</label><br><br>
    
        <input type="checkbox" id="license97" name="license97" value="D55" onclick="LicenseCheckboxingClick(this)">
        <label for="license97">D-55 - Blasting (Now under C-12 or "A")</label><br><br>
    
        <input type="checkbox" id="license98" name="license98" value="D56" onclick="LicenseCheckboxingClick(this)">
        <label for="license98">D-56 - Trenching Only</label><br><br>
    
        <input type="checkbox" id="license99" name="license99" value="D57" onclick="LicenseCheckboxingClick(this)">
        <label for="license99">D-57 - Propane Gas Plants (Now under "A")</label><br><br>
    
        <input type="checkbox" id="license100" name="license100" value="D58" onclick="LicenseCheckboxingClick(this)">
        <label for="license100">D-58 - Residential Floating Docks (Now under "A")</label><br><br>
    
        <input type="checkbox" id="license101" name="license101" value="D59" onclick="LicenseCheckboxingClick(this)">
        <label for="license101">D-59 - Hydroseed Spraying</label><br><br>
    
        <input type="checkbox" id="license102" name="license102" value="D60" onclick="LicenseCheckboxingClick(this)">
        <label for="license102">D-60 - Striping (Now under C-32)</label><br><br>
    
        <input type="checkbox" id="license103" name="license103" value="D61" onclick="LicenseCheckboxingClick(this)">
        <label for="license103">D-61 - Gold Leaf Gilding (Now under D-64)</label><br><br>
    
        <input type="checkbox" id="license104" name="license104" value="D62" onclick="LicenseCheckboxingClick(this)">
        <label for="license104">D-62 - Air and Water Balancing</label><br><br>
    
        <input type="checkbox" id="license105" name="license105" value="D63" onclick="LicenseCheckboxingClick(this)">
        <label for="license105">D-63 - Construction Clean-up</label><br><br>
    
        <input type="checkbox" id="license106" name="license106" value="D64" onclick="LicenseCheckboxingClick(this)">
        <label for="license106">D-64 - Non-specialized</label><br><br>
    
        <input type="checkbox" id="license107" name="license107" value="D65" onclick="LicenseCheckboxingClick(this)">
        <label for="license107">D-65 - Weatherization and Energy Conservation</label><br><br>
    
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
        
        function LicenseCheckboxingClick(checkbox) {
            // Prepare the data to send to the server
            const formData = new FormData();
            formData.append('checkbox_name', checkbox.name);
            formData.append('checkbox_value', checkbox.value);
            formData.append('checkbox_checked', checkbox.checked);
        
            if (checkbox.checked) {

                fetch('loading_contractors.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json()) // Change to `.json()` if the server returns JSON
                .then(data => {
                    if (data.status === 'success') {
                        
                        const contractors = data.contractors;
                        
                        var markers = L.markerClusterGroup({
                            iconCreateFunction: function(cluster) {
                                var count = cluster.getChildCount();
                                
                                // Gradient color based on the count
                                var gradient = count < 10
                                    ? 'linear-gradient(135deg, #68c4cc, #1f5572)'
                                    : count < 50
                                    ? 'linear-gradient(135deg, #ffa500, #cc8400)'
                                    : 'linear-gradient(135deg, #ff5733, #b53324)';
                        
                                return L.divIcon({
                                    html: `
                                        <div style="
                                            background: white; 
                                            border: 4px solid transparent; 
                                            background-clip: padding-box; 
                                            border-radius: 50%; 
                                            position: relative; 
                                            width: 40px; 
                                            height: 40px; 
                                            display: flex; 
                                            justify-content: center; 
                                            align-items: center;
                                            font-weight: bold; 
                                            color: #333;
                                        ">
                                            <div style="
                                                position: absolute; 
                                                top: -4px; 
                                                left: -4px; 
                                                right: -4px; 
                                                bottom: -4px; 
                                                border-radius: 50%; 
                                                background: ${gradient}; 
                                                z-index: -1;
                                            "></div>
                                            ${count}
                                        </div>
                                    `,
                                    className: 'cluster-icon',
                                    iconSize: [40, 40]
                                });
                            }
                        });






                        
                        contractors.forEach(contractor => {
                            const license_number = contractor.license_number;
                            const business_type = contractor.business_type;
                            const contractor_name = contractor.contractor_name;
                            const county = contractor.county;
                            const phone_number = contractor.phone_number;
                            const issue_date = contractor.issue_date;
                            const expiration_date = contractor.expiration_date;
                            const classifications = contractor.classifications;
                            const complete_address = contractor.complete_address;
                            const x_coordinates = parseFloat(contractor.x_coordinates);
                            const y_coordinates = parseFloat(contractor.y_coordinates);
                        
                            
                            const popupContent = `
                                <div style="
                                    display: flex;
                                    border-radius: 10px;
                                    overflow: hidden;
                                    font-family: 'Verdana', sans-serif;
                                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
                                ">
                                    <div style="background: linear-gradient(135deg, #42a5f5, #1e88e5); padding: 10px; color: white;">
                                        <h4 style="margin: 0;">${contractor_name}</h4>
                                        <p style="margin: 4px 0;">🔖 ${license_number}</p>
                                        <p style="margin: 4px 0;">🏷 ${classifications}</p>
                                    </div>
                                    <div style="padding: 10px; background: white; color: #333;">
                                        <p>🏢 <strong>${business_type}</strong></p>
                                        <p>📞 <a href="tel:${phone_number}" style="color: #3bb2b8;">${phone_number}</a></p>
                                        <p>📍 ${complete_address}</p>
                                    </div>
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