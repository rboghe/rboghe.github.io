document.addEventListener('DOMContentLoaded', () => {
    // Function to populate elements from meta tags
    const populateFromMeta = (metaName, targetSelector, formatter = (val => val)) => {
        const metaTag = document.querySelector(`meta[name="${metaName}"]`);
        const targetElement = document.querySelector(targetSelector);
        if (metaTag && metaTag.content && targetElement) {
            targetElement.textContent = formatter(metaTag.content); // Use textContent to avoid HTML injection
        }
    };

    // Populate Date
    populateFromMeta('date', '.post-meta-date', dateStr => {
        try {
            // Reformat date from YYYY-MM-DD to "Month Day, Year"
            const dateObj = new Date(dateStr + 'T00:00:00'); // Add time part for consistency
            return `Published on ${dateObj.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`;
        } catch (e) {
            return `Published on ${dateStr}`; // Fallback
        }
    });

    // Populate the main H1 heading on the page
    populateFromMeta('title', '.blog-post-full h1');
    
    // Populate Author (if meta tag exists and element exists)
    populateFromMeta('author', '.post-meta-author', author => `by ${author}`);

    // Populate Tags (if meta tag exists and element exists)
    const tagsMeta = document.querySelector('meta[name="tags"]');
    const tagsElement = document.querySelector('.post-meta-tags');
    if(tagsMeta && tagsMeta.content && tagsElement) {
        const tags = tagsMeta.content.split(',').map(tag => tag.trim()).filter(Boolean);
        // Clear existing content and rebuild
        tagsElement.innerHTML = 'Tags: '; // Start with label
        tags.forEach((tag, index) => {
            const span = document.createElement('span');
            span.className = 'tag-badge'; // Use the same style as blog index
            span.textContent = tag;
            tagsElement.appendChild(span);
            if (index < tags.length - 1) {
                tagsElement.appendChild(document.createTextNode(' ')); // Add space between tags
            }
        });
    }

    // Update document title
    const titleMeta = document.querySelector('meta[name="title"]');
    if (titleMeta && titleMeta.content) {
        document.title = `${titleMeta.content} - [Your Name]'s Blog`;
    }

});
