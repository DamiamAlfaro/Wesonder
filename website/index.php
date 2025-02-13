<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Wesonder"/>
    <meta name="description" content="WESONDER Map Display"/>
    <link rel="icon" href="pictures/" type="image/x-icon"/>
    <link rel="icon" type="image/png" href="media/bauhaus_logo_transparent.png"/>
    <link href="style0212.css" rel="stylesheet" type="text/css">



    <title>Wesonder</title>

</head>
<body>


    <img src="media/bauhaus_logo_circle_black.png" id="background-logo" alt="Background Logo">


    <main>

        <div id="first_section">
            <h1>Wesonder</h1>
            <div id="nav_links">
                <a href="payments/public/signup.php">Sign Up</a>
                <a href="login/">Login</a>
            </div>
            <div id="section_logo">
                <img src="media/bauhaus_logo_circle_black.png" alt="Section Logo">
            </div>
        </div>


        <div id="video_container">
            <section id="california_video">
                <video autoplay loop muted playsinline>
                    <source src="media/wesonder_reduced_r1.mp4" type="video/mp4">
                </video>
            </section>
            <div id="overlay_text">
                Mapping<br>
                the next<br>
                opportunity.
            </div>
        </div>


        <section id="new_section">
            <div class="content-slider">
                <div class="slide active">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline preload="auto">
                            <source src="media/contractors_illustration_r1.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Explore new Contractors</h4>
                        <p>Discover new potential partners, suppliers, and subcontractors, 
                        leading to new initiatives tailored to your interests and goals.</p>
                    </div>
                </div>
                <div class="slide">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/awarding_body_illustration_r1.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Find Awarding Bodies</h4>
                        <p>Also known as "Owners". Each marker includes the name, address, email address, and most importantly: the direct website
                        to each owner. Owners issue new work on a daily basis.</p>
                    </div>
                </div>
                <div class="slide">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/active_bids_sam_r1.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Locate Active Bids</h4>
                        <p>Bids are a crucial source of work, here we map all Federal and Public Works active bids from the top 4 construction bidding platforms in California: SAM.gov, Planetbids, Bidnet Direct, and PIEE. </p>
                    </div>
                </div>
                <div class="slide">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/contractors_tabulation.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Tabulate Contractors</h4>
                        <p>You can also search for Contractors using specific parameters, such as County, License Number, License Type, 
                        Name, Address, among others.</p>
                    </div>
                </div>
                <div class="slide">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/planetbids_tabulation.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Classify Active Bids </h4>
                        <p>Active Bids are available via tabulation as well, which can be classified by County, Awarding Body, Date, 
                        NAICS Code, among others. </p>
                    </div>
                </div>

                <button class="nav-button left" onclick="changeSlide(-1)">&#10094;</button>
                <button class="nav-button right" onclick="changeSlide(1)">&#10095;</button>
            </div>
        </section>

        <div id="wesonder_functionality">
            
            <h1>How does Wesonder work?</h1>

            <section id="independent_section">
                <div class="independent-content">
                    <h2>Wesonder utilizes a diverse repertoire of reliable publicly available sources:</h2>
                    <div id="independent-section-images">
                        <a href="https://sam.gov/" target="_blank"><img src="media/sam_gov_logo_transparent.png"></a>
                        <a href="https://www.bidnetdirect.com/" target="_blank"><img src="media/bidnetdirect_logo.png"></a>
                        <a href="https://www.dir.ca.gov/" target="_blank"><img src="media/dir_logo.png"></a>
                        <a href="https://home.planetbids.com/" target="_blank"><img src="media/planetbids_logo.png"></a>
                        <a href="https://piee.eb.mil/" target="_blank"><img src="media/piee_logo.png"></a>
                        <a href="https://caleprocure.ca.gov/pages/public-search.aspx" target="_blank"><img src="media/caleprocure_logo.png"></a>
                        <a href="https://dot.ca.gov/programs/civil-rights/dvbe" target="_blank"><img src="media/dvbe_logo.png"></a>
                        <a href="https://www.cslb.ca.gov/" target="_blank"><img src="media/cslb_logo.png"></a>
                        <a href="https://www.ca.gov/" target="_blank"><img src="media/ca_gov_logo.png"></a>
                    </div>
                    <h2>Wesonder thereby serves as the hub for state-of-the-art technologies aiming to support all people participating
                    in the construction industry. </h2>
                </div>
            </section>
        </div>

        <div id="wesonder-last-section">
            <h1>From Construction Estimators 👨🏿‍💼 to Project Managers 🧑🏽‍💼, </h1>
            <h1>From Foremen 👷 to Chief Executives 👩🏻‍💼, </h1>
            <h1>From Government Officials 👨🏼‍💼 to Architectural Designers 🧑🏻‍🎨, </h1> 
            <h1>Wesonder serves equally for everyone 🌎. </h1>

            <!-- New Section Split into Two Halves -->
            <section id="last-section">
                <!-- Left Side (Text) -->
                <div class="last-section-text">
                    <h2><i>"A fountain of Construction Knowledge"</i></h2>
                    <p>Wesonder offers access to Contractors of any License Type, Small Local Business Enterprises (SLBE) firms, Emerging Local Business Enterprises (ELBE) firms, Disable Veteran Business Enterprises (DVBE) firms, Small Businesses (SB) firms, more than <strong>+400,000</strong> commercial enterprises all throughout California.</p>
                    <p>Here you can also procure active bids from Planetbids, Bidnetdirect, as well as Federal Opportunities from SAM.gov and PIEE. Combined there is more than <strong>+250</strong> new bids on a weekly basis throughout California.</p>
                    <p>Lastly, as an additional feature, here you find more than <strong>+8000</strong> Awarding Bodies (Owners) and their location, as well as the record of more than <strong>+300,000</strong> construction Projects from 2018 throughout California.</p>
                </div>

                <!-- Right Side (Image) -->
                <div class="last-section-image">
                    <figure>
                        <img src="media/habitat_57.jpg" alt="Habitat 57, Quebec">
                        <figcaption>Habitat 67, Cité du Havre, Quebec, Canada</figcaption>
                    </figure>
                </div>

            </section>
        </div>
        
    </main>


    <footer id="wesonder-footer">
        <div class="footer-content">
            <div class="footer-logo">
                <img src="media/bauhaus_logo_circle_black.png" alt="Wesonder Logo">
            </div>
            <div class="footer-links">
                <a href="payments/public/signup.php">Sign Up</a>
            </div>
            <div class="footer-info">
                <p><a href="mailto:support@wesonder.com">support@wesonder.com</a></p>
            </div>
            <div class="damiam-alfaro">
                A piece by <a href="https://damiamalfaro.com/" target="_blank">Damiam Alfaro</a>
                <p>Copyright &copy; 2025 Damiam Alfaro</p>
            </div>
        </div>
    </footer>


    <script type="text/javascript" src="script0209-1.js"></script>


</body>
</html>