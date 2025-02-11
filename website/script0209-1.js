document.addEventListener("scroll", () => {
    const logo = document.getElementById("background-logo");
    const scrollY = window.scrollY;

    // Adjust the scroll speed factor (lower = smoother, subtle movement)
    const speedFactor = 0.1;  // Adjust this for more or less movement

    // Apply a smooth parallax effect
    logo.style.transform = `translate(-50%, ${scrollY * speedFactor}px)`;
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
    const wesonderLastSection = document.getElementById("wesonder-last-section");
    const headings = wesonderLastSection.querySelectorAll("h1");

    // Hide all headings initially
    headings.forEach(heading => {
        heading.dataset.text = heading.textContent;  // Save the original text in a data attribute
        heading.textContent = "";                   // Clear the text initially
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                typeHeadings(headings);             // Start typing effect
                observer.unobserve(wesonderLastSection);  // Stop observing after the first trigger
            }
        });
    }, {
        threshold: 0.15  // Trigger when 60% of the section is visible
    });

    observer.observe(wesonderLastSection);
});

// Typing effect function
function typeHeadings(headings) {
    let index = 0;

    function typeHeading() {
        if (index < headings.length) {
            const heading = headings[index];
            const text = heading.dataset.text;     // Retrieve the saved original text
            heading.classList.add("typing");       // Add typing cursor
            typeText(heading, text, 0);            // Start typing each heading
            index++;
        }
    }

    function typeText(element, text, charIndex) {
        const characters = Array.from(text);  // Properly splits text into full characters, including emojis

        if (charIndex < characters.length) {
            element.textContent += characters[charIndex];
            setTimeout(() => typeText(element, text, charIndex + 1), 35);  // Typing speed
        } else {
            element.classList.remove("typing");    // Remove cursor after typing
            setTimeout(typeHeading, 400);          // Delay before typing the next heading
        }
    }


    typeHeading();  // Start typing the first heading
}

