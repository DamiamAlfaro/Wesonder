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

document.addEventListener("scroll", () => {
    const logo = document.getElementById("background-logo");
    const scrollY = window.scrollY;

    // Adjust the scroll speed factor (lower = smoother, subtle movement)
    const speedFactor = 0.1;  // Adjust this for more or less movement

    // Apply a smooth parallax effect
    logo.style.transform = `translate(-50%, ${scrollY * speedFactor}px)`;
});


document.addEventListener("DOMContentLoaded", () => {
    const newSection = document.getElementById("new_section");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                newSection.classList.add("visible"); // Trigger the animation
                observer.unobserve(newSection);      // Stop observing after animation (optional)
            }
        });
    }, {
        threshold: 0.65 // Trigger when xx% is visible
    });

    observer.observe(newSection);
});


document.addEventListener('DOMContentLoaded', () => {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const navButtons = document.querySelectorAll('.nav-button');
    let isAnimating = false; // Lock variable to prevent rapid clicks

    slides[currentSlide].classList.add('active');

    function changeSlide(direction) {
        if (isAnimating) return; // Exit if animation is in progress
        isAnimating = true;      // Lock animation

        const previousSlide = slides[currentSlide];
        const slideOutClass = direction === 1 ? 'slide-out-left' : 'slide-out-right';

        previousSlide.classList.add(slideOutClass);

        setTimeout(() => {
            previousSlide.classList.remove('active', slideOutClass);
            currentSlide = (currentSlide + direction + slides.length) % slides.length;
            slides[currentSlide].classList.add('active');

            isAnimating = false; // Unlock after animation completes
        }, 800); // Match this to your CSS transition duration (0.8s)
    }

    navButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const direction = e.target.classList.contains('left') ? -1 : 1;
            changeSlide(direction);
        });
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const newSection = document.getElementById("new_section");
    const wesonderFunctionality = document.getElementById("wesonder_functionality");
    const wesonderLastSection = document.getElementById("wesonder-last-section");  // Add this line

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible"); // Trigger the animation
                observer.unobserve(entry.target);      // Stop observing after animation (optional)
            }
        });
    }, {
        threshold: 0.65 // Trigger when 60% is visible
    });

    observer.observe(newSection);
    observer.observe(wesonderFunctionality);
    observer.observe(wesonderLastSection);  // Add this line to observe the last section
});
