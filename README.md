# Roberto - Personal Website

Source code for my personal website. This is primarily a static website built using HTML, CSS, and JavaScript.

Python is used for dynamically populating specific pages (Blog index, Publications, Talks) from content files and templates.

## Pages

* **About:** Personal introduction.
* **Thoughts:** Blog section with posts generated from HTML files.
* **Publications:** Dynamically generated list from a YAML file.
* **Talks:** Dynamically generated list from a YAML file.
* **Vitae:** Displays the CV.

## Folder Structure

```
.
├── css/                         # CSS stylesheets 
│   └── style.css
├── js/                          # JavaScript files
│   ├── blog-filter.js
│   ├── blog-metadata.js
│   ├── footer.js
│   └── tooltip.js
├── python/                      # Python scripts 
│   ├── blog.py
│   └── build_content.py
├── templates/                   # HTML templates used by Python scripts
│   ├── blog_post_template.html
│   ├── blog_template.html
│   ├── publications_template.html
│   └── talks_template.html
├── posts/                       # Individual blog post HTML files
│   ├── YYYYMMDD_post-title-1.html
│   └── ...
├── content/                     # Data files for dynamic content
│   ├── publications.yaml
│   └── talks.yaml
├── files/                       # Static files like CV
│   └── ...
├── static/ 
│   ├── fonts/
│   └── icons/
├── index.html                   # Main landing page
├── blog.html                    # Blog index page 
├── publications.html            # Publications page 
├── talks.html                   # Talks page
└── vitae.html                   # Vitae page
```

## Content Management

* **Publications:** Edit `content/publications.yaml`. Run `python python/build_content.py` afterwards.
* **Talks:** Edit `content/talks.yaml`. Run `python python/build_content.py` afterwards. This script will automatically split the talks between upcoming and past depending on the date, so it might be useful to run it periodically.
* **Blog Posts:**
    1.  Create a new HTML file in the `posts/` directory (e.g., `YYYYMMDD_post-title.html`).
    2.  Use `templates/blog_post_template.html` as a starting point. Fill in the required metadata in the `<head>` section (`title`, `date`, `tags`, `description`, Open Graph tags).
    3.  Write the post content within the `<article>` tags.
    4.  Run `python python/blog.py` to update `blog.html`.
* **Other Pages:** Directly edit the corresponding HTML files (e.g., `index.html`, `vitae.html`).