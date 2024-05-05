// Example function to handle a button click event
function handleClick() {
    alert("Button clicked!");
}

// Add event listener to a button element with the id "myButton"
document.getElementById("myButton").addEventListener("click", handleClick);

// JavaScript code to handle the active navigation link
document.addEventListener("DOMContentLoaded", function() {
    // Get the current URL path using Django's template tag
    var currentPath = window.location.pathname;

    // Get the navigation link elements by their IDs
    var homeLink = document.getElementById('home-link');
    var politicsLink = document.getElementById('politics-link');
    var entertainmentLink = document.getElementById('entertainment-link');
    var fashionLink = document.getElementById('fashion-link');
    var sportsLink = document.getElementById('sports-link');
    var science_technologyLink = document.getElementById('science_technology-link');
    var lifestyleLink = document.getElementById('lifestyle-link');

    // Add similar variables for other navigation links

    // Check the current path and add the "active" class to the corresponding link
    if (currentPath === "{% url 'blog:home' %}") {
        homeLink.classList.add('active');
    } else if (currentPath === "{% url 'blog:category_post_list' category_name='politics' %}") {
        politicsLink.classList.add('active');
    } else if (currentPath === "{% url 'blog:category_post_list' category_name='entertainment' %}") {
        entertainmentLink.classList.add('active');
    } else if (currentPath === "{% url 'blog:category_post_list' category_name='fashion' %}") {
        fashionLink.classList.add('active');
    } else if (currentPath === "{% url 'blog:category_post_list' category_name='sports' %}") {
        sportsLink.classList.add('active');
    } else if (currentPath === "{% url 'blog:category_post_list' category_name='science_technology' %}") {
        science_technologyLink.classList.add('active');
    } else if (currentPath === "{% url 'blog:category_post_list' category_name='lifestyle' %}") {
        lifestyleLink.classList.add('active');
    }
    // Add similar conditions for other navigation links
});
function toggleReactions(reactionsId) {
    var reactionsContainer = document.getElementById(reactionsId);

    // Toggle the display of reaction options
    if (reactionsContainer.style.display === "none") {
        reactionsContainer.style.display = "block";
    } else {
        reactionsContainer.style.display = "none";
    }
}

// Close reaction options when clicking outside
window.onclick = function(event) {
    if (!event.target.matches('.reaction-btn')) {
        var reactionOptions = document.getElementsByClassName("reaction-options");
        for (var i = 0; i < reactionOptions.length; i++) {
            var openOptions = reactionOptions[i];
            if (openOptions.style.display === "block") {
                openOptions.style.display = "none";
            }
        }
    }
}

