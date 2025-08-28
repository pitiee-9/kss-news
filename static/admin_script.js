// DOM Elements
        const videoForm = document.getElementById('videoForm');
        const notification = document.getElementById('notification');
        const deleteButtons = document.querySelectorAll('.delete-btn');

        // Show notification
        function showNotification(message, isSuccess = true) {
            notification.textContent = message;
            notification.className = isSuccess ? 'notification' : 'notification error';
            notification.style.display = 'block';
            
            setTimeout(() => {
                notification.style.display = 'none';
            }, 3000);
        }

        // Handle form submission
        videoForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form values
            const formData = new FormData(videoForm);
            
            try {
                const response = await fetch('/add_video', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showNotification(`"${formData.get('title')}" has been added successfully!`);
                    videoForm.reset();
                    
                    // Reload the page after a short delay to show the new video
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                } else {
                    showNotification(`Error: ${result.error}`, false);
                }
            } catch (error) {
                showNotification('Error adding video. Please try again.', false);
                console.error('Error:', error);
            }
        });

        // Handle delete buttons
        deleteButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const videoId = button.getAttribute('data-video-id');
                const videoTitle = button.closest('.video-card').querySelector('.video-title').textContent;
                
                if (confirm(`Are you sure you want to delete "${videoTitle}"?`)) {
                    try {
                        const response = await fetch(`/delete_video/${videoId}`, {
                            method: 'DELETE'
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            showNotification(`"${videoTitle}" has been deleted successfully!`);
                            
                            // Reload the page after a short delay
                            setTimeout(() => {
                                window.location.reload();
                            }, 1000);
                        } else {
                            showNotification(`Error: ${result.error}`, false);
                        }
                    } catch (error) {
                        showNotification('Error deleting video. Please try again.', false);
                        console.error('Error:', error);
                    }
                }
            });
        });