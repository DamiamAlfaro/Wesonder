let lastScrollPosition = 0;
let hasScrolledToMax = false; // Tracks if the user reached maxScroll

document.addEventListener("scroll", function () {
    requestAnimationFrame(() => {
        let videoContainer = document.getElementById("video_container");
        let navbar = document.getElementById("navbar");

        let scrollPosition = window.scrollY;
        let maxScroll = 350; // The amount of scroll required for navbar to appear

        let minWidth = 90; // Minimum width in vw when scrolled down
        let minHeight = 90; // Minimum height in vh when scrolled down
        let maxBorderRadius = 1; // Maximum rounding effect

        // Ensure scrollPosition is within bounds [0, maxScroll]
        let scrollPercentage = Math.min(scrollPosition / maxScroll, 1);

        // Smooth transition values
        let newWidth = 100 - scrollPercentage * (100 - minWidth); 
        let newHeight = 100 - scrollPercentage * (100 - minHeight);
        let newBorderRadius = scrollPercentage * maxBorderRadius;

        // Apply video styles
        videoContainer.style.width = `${newWidth}vw`;
        videoContainer.style.height = `${newHeight}vh`;
        videoContainer.style.borderRadius = `${newBorderRadius}vw`;
        videoContainer.style.margin = "0 auto"; // Keeps centered

        // Navbar logic: Show only after reaching maxScroll
        if (scrollPosition >= maxScroll) {
            hasScrolledToMax = true;
            navbar.classList.add("visible"); // Show navbar
        } else if (hasScrolledToMax) {
            navbar.classList.add("visible"); // Keep navbar visible once revealed
        } else {
            navbar.classList.remove("visible"); // Hide navbar if maxScroll not reached
        }
    });
});
