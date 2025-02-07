<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Wesonder"/>
    <meta name="description" content="WESONDER Map Display"/>
    <link rel="icon" href="pictures/" type="image/x-icon"/>
    <link rel="icon" type="image/png" href="media/bauhaus_logo_transparent.png"/>
    <link href="style.css" rel="stylesheet" type="text/css">


    <title>Wesonder</title>

</head>
<body>

    <img src="media/bauhaus_logo_circle_black.png" id="background-logo" alt="Background Logo">

    <nav id="navbar">
        <a href="#" id="signup-link">Sign Up</a>
    </nav>
    <main>
        
        <div id="video_container">
            <section id="california_video">
                <video autoplay loop muted playsinline>
                    <source src="media/wesonder_reduced_r1.mp4" type="video/mp4">
                </video>

            </section>
            <div id="overlay_logo">
                <img src="media/bauhaus_logo_transparent.png">
            </div>
            <div id="overlay_text">
                Wesonder<br>
                <br>

                Mapping<br>
                the next<br>
                opportunity.
            </div>
        </div>


        <section id="new_section">
            <div class="content-slider">
                <div class="slide active">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
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
            
            <h1>How does Wesonder Work?</h1>

            <section id="independent_section">
                <div class="independent-content">
                    <h2>Wesonder utilizes a diverse repertoire of reliable sources:</h2>
                    <img src="media/sam_gov_logo_transparent.png" width="250" height="250">
                    <img src="media/bidnetdirect_logo.png" width="250" height="250">
                    <img src="media/dir_logo.png" width="250" height="250">
                    <br>
                    <img src="media/planetbids_logo.png" width="250" height="250">
                    <img src="media/piee_logo.png" width="250" height="250">
                    <img src="media/caleprocure_logo.png" width="250" height="250">
                    <br>
                    <img src="media/dvbe_logo.png" width="250" height="250">
                    <img src="media/cslb_logo.png" width="250" height="250">
                    <img src="media/ca_gov_logo.png" width="250" height="250">
                    <p></p>
                </div>
            </section>
        </div>




        
    </main>

    <script type="text/javascript" src="script.js"></script>


</body>
</html>