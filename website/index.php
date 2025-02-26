<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <meta name="author" content="Wesonder"/>
    <meta name="description" content="WESONDER Map Display"/>
    <link rel="icon" href="pictures/" type="image/x-icon"/>
    <link rel="icon" type="image/png" href="media/bauhaus_logo_transparent.png"/>
    <link href="style0215-1.css" rel="stylesheet" type="text/css">



    <title>Wesonder</title>

</head>
<body>


    <!-- Background Images Container -->
    <div id="background-images">
        <img src="media/bauhaus_logo_circle_black.png" class="background-logo first-bg" alt="Background Logo">
        <img src="media/perhapsanother.jpg" class="background-logo second-bg" alt="Background Logo">
        <img src="media/anotheroneexample.jpg" class="background-logo third-bg" alt="Background Logo">
        <img src="media/josef_albers_art1.jpg" class="background-logo fourth-bg" alt="Background Logo">
        <img src="media/laszlo_moholy_art.jpg" class="background-logo fifth-bg" alt="Background Logo">
    </div>


    <main>

        <div id="first_section">
            <h1>Wesonder</h1>
            <div id="nav_links">
                <!-- Login & Sign Up Links -->
                <a href="#" id="login_btn">Login</a>
                <a href="payments/public/signup.php">Sign Up</a>
            </div>
            <div id="section_logo">
                <img src="media/bauhaus_logo_circle_black.png" alt="Section Logo">
            </div>
        </div>


        <!-- Hidden Login Modal -->
        <div id="login_modal" class="modal">
            <div class="modal_content">
                <span class="close">&times;</span>
                <h2>Login</h2>
                <form action="login.php" method="POST" id="login_form">
                    <input type="email" name="email" placeholder="Email" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Login</button>
                </form>
            </div>
        </div>

        <script>
            document.addEventListener("DOMContentLoaded", function () {
                const loginBtn = document.getElementById("login_btn");
                const modal = document.getElementById("login_modal");
                const closeBtn = document.querySelector(".close");

                // Ensure the modal is hidden when the page loads
                modal.style.display = "none";

                // Show modal when login link is clicked
                loginBtn.addEventListener("click", function (e) {
                    e.preventDefault();
                    modal.style.display = "flex"; // Show modal
                });

                // Close modal when close button is clicked
                closeBtn.addEventListener("click", function () {
                    modal.style.display = "none"; // Hide modal
                });

                // Close modal when clicking outside the box
                window.addEventListener("click", function (e) {
                    if (e.target === modal) {
                        modal.style.display = "none"; // Hide modal
                    }
                });
            });
        </script>

        

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
            <div class="stacked-cards">
                <div class="card">
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
                
                <div class="card">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/awarding_body_illustration_r1.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Find Awarding Bodies</h4>
                        <p>Each marker includes the name, address, email address, and website of each owner. Owners issue new work daily.</p>
                    </div>
                </div>

                <div class="card">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/active_bids_sam_r1.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Locate Active Bids</h4>
                        <p>Mapping all Federal and Public Works active bids from the top 4 construction bidding platforms in California.</p>
                    </div>
                </div>

                <div class="card">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/contractors_tabulation.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Tabulate Contractors</h4>
                        <p>Search for Contractors using specific parameters, such as County, License Number, and Name.</p>
                    </div>
                </div>

                <div class="card">
                    <div class="video-wrapper">
                        <video autoplay loop muted playsinline>
                            <source src="media/planetbids_tabulation.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div class="text-wrapper">
                        <h4>Classify Active Bids</h4>
                        <p>Active Bids are available via tabulation, which can be classified by County, Awarding Body, Date, NAICS Code, and more.</p>
                    </div>
                </div>
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
                <p><a href="tos/">Terms of Service</a></p>
            </div>
        </div>
    </footer>


    <script type="text/javascript" src="script0215-1.js"></script>


</body>
</html>