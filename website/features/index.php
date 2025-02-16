<?php 
require_once 'auth_check.php'; // Ensure only authorized users can access
?>

<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wesonder - Features</title>
  <script src="client.js" defer></script>
  <link rel="icon" type="image/png" href="bauhaus_logo_transparent.png"/>
  <link rel="stylesheet" type="text/css" href="features_styles.css">
</head>
<body>
    
    <?php if (isset($_GET['message'])): ?>
        <p style="color: red; font-weight: bold;"><?php echo htmlspecialchars($_GET['message']); ?></p>
    <?php endif; ?>

    <img src="bauhaus_logo_circle_black.png" id="background-logo" alt="Background Logo">

    <section>
        <div class="maps">
            <div class="main-title">
                🗺️ Maps
            </div>
            <div class="maps-photo">
                <img src="bauhaus_style_map.png" alt="Maps Illustration">
            </div>
            <div class="map-features">
                <ul>
                    <li><a href="maps/contractors"><span class="name">Contractors</span></a></li>
                    <li><a href="maps/awarding_bodies"><span class="name">Awarding Bodies</span></a></li>
                    <li><a href="maps/dvbe"><span class="name">DVBE</span></a></li>
                    <li><a href="maps/planetbids"><span class="name">Planetbids</span></a></li>
                    <li><a href="maps/bidnetdirect"><span class="name">Bidnet Direct</span></a></li>
                    <li><a href="maps/sam_gov"><span class="name">SAM.gov</span></a></li>
                    <li><a href="maps/piee"><span class="name">PIEE</span></a></li>
                    <li><a href="maps/projects"><span class="name">Projects</span></a></li>
                </ul>
            </div>
        </div>
        
        <div class="tabulations">
            <div class="main-title">
                📊 Tabulations
            </div>
            <div class="tabulations-photo">
                <img src="bauhaus_style_tabulation.png" alt="Tabulations Illustration">
            </div>
            <div class="tabulations-features">
                <ul>
                    <li><a href="tabulations/contractors"><span class="name">Contractors</span></a></li>
                    <li><a href="tabulations/awarding_bodies"><span class="name">Awarding Bodies</span></a></li>
                    <li><a href="tabulations/dvbe"><span class="name">DVBE</span></a></li>
                    <li><a href="tabulations/slbe_elbe"><span class="name">ELBE/ELBE</span></a></li>
                    <li><a href="tabulations/planetbids"><span class="name">Planetbids</span></a></li>
                    <li><a href="tabulations/bidnetdirect"><span class="name">Bidnet Direct</span></a></li>
                    <li><a href="tabulations/sam_gov"><span class="name">SAM.gov</span></a></li>
                    <li><a href="tabulations/piee"><span class="name">PIEE</span></a></li>
                    <li><a href="tabulations/projects"><span class="name">Projects</span></a></li>
                </ul>
            </div>
        </div>
    </section>

    <!-- Centered Logout and Cancel Subscription buttons -->
    <div class="button-container">
        <form action="../logout.php" method="POST">
            <button type="submit" class="logout-btn">Logout</button>
        </form>
        
<!--         <form action="../payments/public/cancel_subscription.php" method="POST">
            <button type="submit" class="cancel-btn">Cancel Subscription</button>
        </form> -->
    </div>

</body>
</html>
