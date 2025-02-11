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
            width: 80%;
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
  </style>
</head>
<body>

    <img src="../../media/bauhaus_logo_circle_black.png" id="background-logo" alt="Background Logo">

    <section>
        <div class="maps">
            <div class="maps-photo">
                <img src="../media/bauhaus_logo.png" alt="Maps Illustration">
            </div>
            <div class="map-features">
                <ul>
                    <li>
                        <span id="contractors-icon"></span>
                        <span class="name">Contractors</span>
                    </li>
                    <li>
                        <span id="awarding-bodies-icon"></span>
                        <span class="name">Awarding Bodies</span>
                    </li>
                    <li>
                        <span id="dvbe-icon"></span>
                        <span class="name">DVBE</span>
                    </li>
                    <li>
                        <span id="planetbids-icon"></span>
                        <span class="name">Planetbids</span>
                    </li>
                    <li>
                        <span id="bidnet-icon"></span>
                        <span class="name">Bidnet Direct</span>
                    </li>
                    <li>
                        <span id="samgov-icon"></span>
                        <span class="name">SAM.gov</span>
                    </li>
                    <li>
                        <span id="piee-icon"></span>
                        <span class="name">PIEE</span>
                    </li>
                    <li>
                        <span id="projects-icon"></span>
                        <span class="name">Projects</span>
                    </li>
                </ul>
            </div>
        </div>
        <div class="tabulations">
            <div class="tabulations-photo">
                <img src="../media/bauhaus_logo.png" alt="Tabulations Illustration">
            </div>
            <div class="tabulations-features">
                <ul>
                    <li>
                        <span id="contractors-icon"></span>
                        <span class="name">Contractors</span>
                    </li>
                    <li>
                        <span id="awarding-bodies-icon"></span>
                        <span class="name">Awarding Bodies</span>
                    </li>
                    <li>
                        <span id="dvbe-icon"></span>
                        <span class="name">DVBE</span>
                    </li>
                    <li>
                        <span id="elbe-icon"></span>
                        <span class="name">ELBE/ELBE</span>
                    </li>
                    <li>
                        <span id="planetbids-icon"></span>
                        <span class="name">Planetbids</span>
                    </li>
                    <li>
                        <span id="bidnet-icon"></span>
                        <span class="name">Bidnet Direct</span>
                    </li>
                    <li>
                        <span id="samgov-icon"></span>
                        <span class="name">SAM.gov</span>
                    </li>
                    <li>
                        <span id="piee-icon"></span>
                        <span class="name">PIEE</span>
                    </li>
                    <li>
                        <span id="projects-icon"></span>
                        <span class="name">Projects</span>
                    </li>
                </ul>
            </div>
        </div>
    </section>

</body>
</html>
