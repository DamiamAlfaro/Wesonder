<?php include('../auth.php'); ?>

<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Wesonder - Features</title>
  <script src="client.js" defer></script>
  <link rel="icon" type="image/png" href="../../media/bauhaus_logo_transparent.png"/>
  <style>
        body {
          background: #F5F5F5;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Ubuntu', sans-serif;
          overflow-x: hidden;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
          position: relative;
        }

        #background-logo {
            position: fixed;
            top: 6%;
            left: 50%;
            transform: translate(-50%, 0);
            width: 900px;
            height: auto;
            opacity: 0.07;
            transition: transform 0.1s ease-out;
            z-index: -1;
        }

        section {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            width: 64%;
            gap: 2rem;
        }

        .maps, .tabulations {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 1rem;
            display: flex;
            flex-direction: column;
            max-width: 40%;
            transition: transform 0.5s ease, box-shadow 0.5s ease;
        }
        
        .maps:hover, .tabulations:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }

        img {
            width: 100%;
            border-radius: 8px;
        }

        ul {
            list-style: none;
            padding: 0;
            margin: 1rem 0 0 0;
        }

        li {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .name {
            margin-left: 0.5rem;
        }
        
        .maps-features {
        	width: 40em;
        	height: 10vh;
        	margin: 0 auto;
        	background: #fff;
        	border: 1px solid #ddd;
        	position: relative;
        }

        a {
            display: block;
            background: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 0.5rem;
            text-decoration: none;
            color: black;
            transition: transform 0.5s ease, box-shadow 0.5s ease;
        }

        a:hover {
            transform: translateY(-10px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }

        /* Logout button styling */
        .logout-container {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
        }

        .logout-container a {
            display: inline-block;
            padding: 10px 20px;
            background: #dc3545;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }

        .logout-container a:hover {
            background: #c82333;
        }

  </style>
</head>
<body>

    <img src="../../media/bauhaus_logo_circle_black.png" id="background-logo" alt="Background Logo">

    <section>
        <div class="maps">
            <div class="maps-photo">
                <img src="../../media/bauhaus_logo.png" alt="Maps Illustration">
            </div>
            <div class="map-features">
                <ul>
                    <li>
                        <span id="contractors-icon"></span>
                        <a href="maps/contractors"><span class="name">Contractors</span></a>
                    </li>
                    <li>
                        <span id="awarding-bodies-icon"></span>
                        <a href="maps/awarding_bodies"><span class="name">Awarding Bodies</span></a>
                    </li>
                    <li>
                        <span id="dvbe-icon"></span>
                        <a href="maps/dvbe"><span class="name">DVBE</span></a>
                    </li>
                    <li>
                        <span id="planetbids-icon"></span>
                        <a href="maps/planetbids"><span class="name">Planetbids</span></a>
                    </li>
                    <li>
                        <span id="bidnet-icon"></span>
                        <a href="maps/bidnetdirect"><span class="name">Bidnet Direct</span></a>
                    </li>
                    <li>
                        <span id="samgov-icon"></span>
                        <a href="maps/sam_gov"><span class="name">SAM.gov</span></a>
                    </li>
                    <li>
                        <span id="piee-icon"></span>
                        <a href="maps/piee"><span class="name">PIEE</span></a>
                    </li>
                    <li>
                        <span id="projects-icon"></span>
                        <a href="maps/projects"><span class="name">Projects</span></a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="tabulations">
            <div class="tabulations-photo">
                <img src="../../media/bauhaus_logo.png" alt="Tabulations Illustration">
            </div>
            <div class="tabulations-features">
                <ul>
                    <li>
                        <span id="contractors-icon"></span>
                        <a href="tabulations/contractors"><span class="name">Contractors</span></a>
                    </li>
                    <li>
                        <span id="awarding-bodies-icon"></span>
                        <a href="tabulations/awarding_bodies"><span class="name">Awarding Bodies</span></a>
                    </li>
                    <li>
                        <span id="dvbe-icon"></span>
                        <a href="tabulations/dvbe"><span class="name">DVBE</span></a>
                    </li>
                    <li>
                        <span id="elbe-icon"></span>
                        <a href="tabulations/slbe_elbe"><span class="name">ELBE/ELBE</span></a>
                    </li>
                    <li>
                        <span id="planetbids-icon"></span>
                        <a href="tabulations/planetbids"><span class="name">Planetbids</span></a>
                    </li>
                    <li>
                        <span id="bidnet-icon"></span>
                        <a href="tabulations/bidnetdirect"><span class="name">Bidnet Direct</span></a>
                    </li>
                    <li>
                        <span id="samgov-icon"></span>
                        <a href="tabulations/sam_gov"><span class="name">SAM.gov</span></a>
                    </li>
                    <li>
                        <span id="piee-icon"></span>
                        <a href="tabulations/piee"><span class="name">PIEE</span></a>
                    </li>
                    <li>
                        <span id="projects-icon"></span>
                        <a href="tabulations/projects"><span class="name">Projects</span></a>
                    </li>
                </ul>
            </div>
        </div>
    </section>



</body>
</html>
