document.addEventListener('DOMContentLoaded', () => {
    const filterContainer = document.querySelector('.tag-filter-container');
    const filterButtons = document.querySelectorAll('.tag-filter-button');
    const postArticles = document.querySelectorAll('.blog-posts-list .post-preview');

    if (!filterContainer || filterButtons.length === 0 || postArticles.length === 0) {
        // console.log('Blog filtering elements not found.');
        return; // Exit if essential elements are missing
    }

    filterContainer.addEventListener('click', (event) => {
        if (!event.target.matches('.tag-filter-button')) {
            return; // Ignore clicks that aren't on a button
        }

        const clickedButton = event.target;
        const filterTag = clickedButton.getAttribute('data-filter-tag').toLowerCase(); // Ensure lowercase

        // Update active button state
        filterButtons.forEach(button => {
            button.classList.remove('active');
        });
        clickedButton.classList.add('active');

        // Filter articles
        postArticles.forEach(article => {
            const articleTags = article.getAttribute('data-tags'); // Space-separated lowercase tags

            if (filterTag === 'all' || (articleTags && articleTags.split(' ').includes(filterTag))) {
                article.style.display = ''; // Show article
                // Ensure the divider after the article is also shown if needed
                const divider = article.nextElementSibling;
                if(divider && divider.matches('hr.post-divider')) {
                    divider.style.display = '';
                }

            } else {
                article.style.display = 'none'; // Hide article
                // Ensure the divider after the article is also hidden
                const divider = article.nextElementSibling;
                if(divider && divider.matches('hr.post-divider')) {
                    divider.style.display = 'none';
                }
            }
        });
    });
});