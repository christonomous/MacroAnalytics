document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');
    const progressBar = document.getElementById('progressBar');
    const currentDate = document.getElementById('currentDate');

    // Set current date
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    currentDate.textContent = new Date().toLocaleDateString(undefined, options);

    // Fetch and render the markdown
    fetch('ARTICLE.md')
        .then(response => {
            if (!response.ok) throw new Error('Article not found');
            return response.text();
        })
        .then(text => {
            // Clean up paths for images if necessary
            // Since our ARTICLE.md uses file:/// paths or assets/
            // We should ensure they work in a web environment.
            // If the user serves the root, assets/ will work.
            const cleanedText = text.replace(/file:\/\/\/.*?\/assets\//g, 'assets/');

            content.innerHTML = marked.parse(cleanedText);

            // Initialize Mermaid
            mermaid.initialize({ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' });
            mermaid.run();

            // Add custom logic for progress bar
            window.addEventListener('scroll', updateProgress);
        })
        .catch(err => {
            content.innerHTML = `<div class="error">
                <h3>System Alert</h3>
                <p>Unable to load the Paradox data. Please ensure you are running a local server.</p>
                <code style="display: block; margin-top: 1rem; padding: 1rem; background: #fee2e2; border-radius: 8px;">${err.message}</code>
            </div>`;
        });

    function updateProgress() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + "%";
    }
});
