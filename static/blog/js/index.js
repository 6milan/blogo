document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle reactions container visibility
    function toggleReactions(reactionsId) {
        var reactionsContainer = document.getElementById(reactionsId);
        reactionsContainer.style.display = (reactionsContainer.style.display === "none") ? "block" : "none";
    }

    // Event listener for toggling reactions container visibility
    document.querySelectorAll('.reaction-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            var reactionsId = this.dataset.reactionsId;
            toggleReactions(reactionsId);
        });
    });

    // Event listener for reacting to a post or comment
    document.querySelectorAll('.reaction-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            var objectId = this.dataset.objectId;
            var reactionType = this.dataset.reactionType;
            react(objectId, reactionType);
            this.classList.add('reacted');
            setTimeout(() => {
                this.classList.remove('reacted');
            }, 1000);
        });
    });

    // Function to send reaction data to the server
function react(objectId, reactionType) {
    var url;
    if (objectId.includes('post')) {
        url = '/blog/react_to_post/' + objectId.replace('post', '') + '/' + reactionType + '/';
    } else {
        url = '/blog/react_to_comment/' + objectId.replace('comment', '') + '/' + reactionType + '/';
    }

    var formData = new FormData();
    formData.append('reaction', reactionType);

    fetch(url, {
        method: 'POST',
        body: formData,
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        updateReactionCounts(data.counts);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



    // Function to get CSRF token
    function getCSRFToken() {
        var csrfToken = null;
        var cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            var cookiePair = cookie.trim().split('=');
            if (cookiePair[0] === 'csrftoken') {
                csrfToken = cookiePair[1];
            }
        });
        return csrfToken;
    }

    // Function to update reaction counts on the UI
    function updateReactionCounts(counts) {
        document.querySelectorAll('.reaction-count').forEach(span => {
            var reactionType = span.dataset.reactionType;
            span.textContent = counts[reactionType];
        });
    }
});

// Get all reaction buttons
const reactionBtns = document.querySelectorAll('.reaction-btn');

// Add click event listener to each reaction button
reactionBtns.forEach(button => {
    button.addEventListener('click', function() {
        // Toggle the visibility of emojis
        const emoji = this.querySelector('.emoji');
        emoji.style.display = emoji.style.display === 'none' ? 'inline-block' : 'none';
    });
});

// Function to toggle reply form visibility
function toggleReplyForm(commentId) {
    var replyForm = document.getElementById("reply-form-" + commentId);
    if (replyForm.style.display === "none") {
        replyForm.style.display = "block";
    } else {
        replyForm.style.display = "none";
    }
}

function toggleReplyForm(commentId) {
    var replySection = document.getElementById("reply-section-" + commentId);
    if (replySection.style.display === "none") {
        replySection.style.display = "block";
    } else {
        replySection.style.display = "none";
    }
}
