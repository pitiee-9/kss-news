// Parse the video data from the script tag
        const videoData = JSON.parse(document.getElementById('video-data').textContent);
        
        // DOM Elements
        const videoModal = document.getElementById('videoModal');
        const videoPlayer = document.getElementById('videoPlayer');
        const videoTitle = document.getElementById('videoTitle');
        const closeVideoBtn = document.getElementById('closeVideoBtn');
        const videoCards = document.querySelectorAll('.video-card');
        const watchButtons = document.querySelectorAll('.watch-btn');

        // Open video modal when a video card is clicked
        videoCards.forEach(card => {
            card.addEventListener('click', () => {
                const videoId = parseInt(card.getAttribute('data-video-id'));
                playVideo(videoId);
            });
        });

        // Also handle watch buttons
        watchButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const videoId = parseInt(button.getAttribute('data-video-id'));
                playVideo(videoId);
            });
        });

        // Close video modal
        closeVideoBtn.addEventListener('click', () => {
            videoModal.style.display = 'none';
            videoPlayer.pause();
            videoPlayer.src = ''; // Reset the video source
        });

        // Close modal when clicking outside
        window.addEventListener('click', (event) => {
            if (event.target === videoModal) {
                videoModal.style.display = 'none';
                videoPlayer.pause();
                videoPlayer.src = ''; // Reset the video source
            }
        });

        // Function to play a video
        function playVideo(videoId) {
            const video = videoData.find(v => v.id === videoId);
        
            if (video) {
                videoTitle.textContent = `${video.title} (${video.year})`;
                videoPlayer.src = `/video/${video.filename}`;
                videoModal.style.display = 'flex';
                
                // Load the video source
                videoPlayer.load();
                
                // Play the video
                const playPromise = videoPlayer.play();
                
                if (playPromise !== undefined) {
                    playPromise.catch(error => {
                        console.error('Auto-play was prevented:', error);
                    });
                }
            } else {
                console.error('Video not found with ID:', videoId);
            }
        }