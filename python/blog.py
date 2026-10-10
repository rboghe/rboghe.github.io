import os
import glob
from bs4 import BeautifulSoup, element 
from datetime import datetime
import re
from typing import List, Dict, Optional, Any, Tuple

POSTS_DIR = "posts"
TEMPLATE_PATH = "templates/blog_template.html"
OUTPUT_HTML = "blog.html"
EXCERPT_LENGTH = 20  # Number of words for the excerpt
BLOG_TITLE = "Blog / Thoughts - Roberto Boghetti"
SITE_NAME = "Roberto Boghetti" # Define name for OG title


def clean_text_for_word_count(text: str) -> str:
    """Removes extra whitespace for accurate word counting."""
    text = re.sub(r'\s+', ' ', text) # Replace multiple spaces/newlines with single space
    return text.strip()


def create_excerpt(html_content: str, length: int) -> str:
    """
    Generates an HTML excerpt from the main article content, preserving
    paragraph tags and structure up to the specified word length.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    output_paragraphs = [] # Store HTML strings of paragraphs to include
    current_word_count = 0

    # Find the main article content area first
    article_tag = soup.find('article', class_='blog-post-full')
    content_source = article_tag if article_tag else soup # Fallback

    # Find all paragraph tags within the content source
    paragraphs = content_source.find_all('p')

    for p in paragraphs:
        # Ensure p is actually a Tag object
        if not isinstance(p, element.Tag):
            continue

        ### Skip metadata paragraphs ###
        p_class = p.get('class', [])
        # Get text without extra spaces for checking metadata patterns accurately
        p_text_check = p.get_text(strip=True).lower()
        if 'post-meta' in p_class or \
            p_text_check.startswith('published on') or \
            p_text_check.startswith('by ') or \
            p_text_check.startswith('tags:'):
            continue 

        ### Process content paragraph ###
        # Get clean text just for word counting
        p_text_for_count = clean_text_for_word_count(p.get_text())
        p_words = p_text_for_count.split()
        paragraph_word_count = len(p_words)

        if paragraph_word_count == 0: # Skip empty paragraphs
            continue

        # How many more words can we take?
        words_needed = length - current_word_count

        # If this whole paragraph fits (or is the first one)
        if words_needed >= paragraph_word_count:
            output_paragraphs.append(str(p)) # Add the full paragraph HTML
            current_word_count += paragraph_word_count
        else:
            # This paragraph needs truncation
            if words_needed > 0:
                # Take the needed words and add ellipsis
                truncated_text = ' '.join(p_words[:words_needed]) + "..."

                # Create a new paragraph tag with the truncated content
                # Preserve original classes if any
                new_p = soup.new_tag("p", **{'class': p.get('class', [])})
                new_p.string = truncated_text # Assign the truncated text
                output_paragraphs.append(str(new_p))
                current_word_count += words_needed # Reached the limit exactly
            # Else (words_needed <= 0), don't add this paragraph
            break 

    ### Construct the final HTML output ###
    if not output_paragraphs:
        return "<p>...</p>" # No content found

    final_html = "\n".join(output_paragraphs)

    return final_html


def parse_post(filepath: str) -> Optional[Dict[str, Any]]:
    """Extracts metadata and content from a post HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content: str = f.read()

        soup: BeautifulSoup = BeautifulSoup(content, 'html.parser')
        metadata: Dict[str, Any] = {}

        title_tag = soup.find('meta', {'name': 'title'})
        date_tag = soup.find('meta', {'name': 'date'})
        tags_tag = soup.find('meta', {'name': 'tags'})

        metadata['title'] = title_tag['content'] if title_tag else 'Untitled Post'
        metadata['filepath'] = filepath

        # Date parsing 
        date_str = date_tag['content'] if date_tag else None
        if date_str:
            try:
                metadata['date_obj'] = datetime.strptime(date_str, '%Y-%m-%d')
                metadata['date_str'] = metadata['date_obj'].strftime('%B %d, %Y')
            except ValueError:
                print(f"Warning: Invalid date format '{date_str}' in {filepath}. Using file mod time.")
                metadata['date_obj'] = datetime.fromtimestamp(os.path.getmtime(filepath))
                metadata['date_str'] = metadata['date_obj'].strftime('%B %d, %Y')
        else:
            print(f"Warning: Missing date meta tag in {filepath}. Using file mod time.")
            metadata['date_obj'] = datetime.fromtimestamp(os.path.getmtime(filepath))
            metadata['date_str'] = metadata['date_obj'].strftime('%B %d, %Y')

        # Tag parsing
        tags_data = []
        if tags_tag and tags_tag.get('content'):
            raw_tags_list = tags_tag['content'].split(',')
            for raw_tag in raw_tags_list:
                original_tag = raw_tag.strip()
                if original_tag: # Avoid empty tags
                    lower_tag = original_tag.lower()
                    tags_data.append({'original': original_tag, 'lower': lower_tag})
        metadata['tags'] = tags_data # Store list of dictionaries

        metadata['excerpt'] = create_excerpt(content, EXCERPT_LENGTH)

        # Return metadata
        return metadata

    except Exception as e:
        print(f"Error parsing file {filepath}: {e}")
        return None


def build_blog_html(posts_data: List[Dict[str, Any]]) -> str:
    """Generates the blog.html content using a template."""

    posts_data.sort(key=lambda p: p['date_obj'], reverse=True)

    # Collect unique tags: Store lowercase -> original mapping
    # This handles potential casing inconsistencies
    unique_tags_map = {}
    for post in posts_data:
        for tag_dict in post['tags']: 
            # Map lower to original
            unique_tags_map[tag_dict['lower']] = tag_dict['original'] 

    # Sort based on the lowercase keys for consistent order
    sorted_lowercase_tags = sorted(unique_tags_map.keys())

    ### Generate HTML Parts ###
    # Tag Buttons
    tag_buttons_html_parts: List[str] = []
    for lower_tag in sorted_lowercase_tags:
        display_tag = unique_tags_map[lower_tag] # Get original casing from map
        button_text = display_tag.replace("-", " ")
        tag_buttons_html_parts.append(
            f'<button class="tag-filter-button" data-filter-tag="{lower_tag}">{button_text}</button>'
            )
        
    # Join with newline and indentation
    tag_buttons_html = "\n                ".join(tag_buttons_html_parts) 

    # Post List Items
    posts_list_html_parts: List[str] = []
    for i, post in enumerate(posts_data):
        tags_html_parts = []
        lower_tags_for_article = [] # For the data-tags attribute
        for tag_dict in post['tags']:
            display_tag = tag_dict['original'].replace("-", " ") # Use original casing for display
            lower_tag = tag_dict['lower']
            tags_html_parts.append(f'<span class="tag-badge" data-tag="{lower_tag}">{display_tag}</span>')
            lower_tags_for_article.append(lower_tag) # Collect lowercase tags

        tags_html = "".join(tags_html_parts)
        data_tags_attr = " ".join(lower_tags_for_article) # Ensure data-tags uses lowercase

        article_html = f"""
                <article class="post-preview" data-tags="{data_tags_attr}">
                    <h2><a href="{post['filepath']}">{post['title']}</a></h2>
                    <p class="post-meta">Published on {post['date_str']}</p>
                    <div class="post-tags">{tags_html}</div>
                    <div class="post-excerpt">
                        {post['excerpt']}
                    </div>
                    <p><a href="{post['filepath']}">Read more &rarr;</a></p>
                </article>"""
        posts_list_html_parts.append(article_html)
        # Add divider except after the last post
        if i < len(posts_data) - 1:
            posts_list_html_parts.append('                <hr class="post-divider">')


    posts_list_html = "\n".join(posts_list_html_parts)

    ### Read Template and Replace Placeholders ###
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {TEMPLATE_PATH}")
        return "<html><body>Error: Blog template not found.</body></html>"

    # Replace placeholders
    final_html = template_content.replace("{BLOG_TITLE}", BLOG_TITLE)
    final_html = final_html.replace("{TAG_BUTTONS}", tag_buttons_html)
    final_html = final_html.replace("{POSTS_LIST}", posts_list_html)

    return final_html


if __name__ == "__main__":
    print("Processing posts and building blog index...")
    all_posts_data = []
    processed_files_count = 0
    # Find all .html files in the posts directory
    post_files = glob.glob(os.path.join(POSTS_DIR, "*.html"))

    if not post_files:
        print("No posts found in directory:", POSTS_DIR)
    else:
        print(f"Found {len(post_files)} potential post files.")
        for filepath in post_files:
            print(f"Processing: {filepath}")
            metadata = parse_post(filepath)
            if metadata:
                all_posts_data.append(metadata)
                processed_files_count += 1
            else:
                print(f"Failed to parse {filepath}.")

    if not all_posts_data:
        print("No posts were successfully processed to build the index.")
        final_html = "<html><body>No posts found or processed successfully.</body></html>"
    else:
        # Generate the final HTML for blog.html using collected metadata
        print(f"Building index with {len(all_posts_data)} successfully processed posts.")
        final_html: str = build_blog_html(all_posts_data)

    # Write to output file
    try:
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Successfully generated {OUTPUT_HTML} with data from {len(all_posts_data)} posts.")
        if processed_files_count > 0:
            print(f"Successfully updated OG tags in {processed_files_count} post files.")

    except IOError as e:
        print(f"Error writing index file {OUTPUT_HTML}: {e}")
