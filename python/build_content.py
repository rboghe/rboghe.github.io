import yaml
from datetime import datetime
from typing import List, Dict, Any, Optional

# --- Configuration ---
OWNER_NAME = "Roberto Boghetti"
GOOGLE_SCHOLAR_ID = "FWBzV0cAAAAJ" 
PUBS_YAML = "content/publications.yaml"
TALKS_YAML = "content/talks.yaml"
PUBS_TEMPLATE = "templates/publications_template.html" 
TALKS_TEMPLATE = "templates/talks_template.html" 
PUBS_HTML_OUT = "publications.html"
TALKS_HTML_OUT = "talks.html"
# Define link order
LINK_ORDER = ['pdf', 'preprint', 'doi', 'code', 'slides', 'video', 'poster', 'url', 'bibtex'] 

### Helper Functions ###
def load_yaml(filename: str) -> Optional[Any]:
    """Loads data from a YAML file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Use safe_load
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found: {filename}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {filename}: {e}")
        return None
    except IOError as e:
        print(f"Error reading file {filename}: {e}")
        return None
    

def format_authors(authors: List[str], owner_name: str) -> str:
    """Formats author list, highlighting the owner."""
    if not authors:
        return ""
    formatted: List[str] = []
    for author in authors:
        # Strip whitespace for accurate comparison
        if author.strip() == owner_name.strip():
            formatted.append(f"<strong>{author.strip()}</strong>")
        else:
            formatted.append(author.strip())

    # Joining logic
    if len(formatted) > 2:
        return ", ".join(formatted[:-1]) + ", and " + formatted[-1]
    elif len(formatted) == 2:
        return " and ".join(formatted)
    else: # Single author
        return formatted[0]


def generate_links_html(links_dict: Optional[Dict[str, str]]) -> str:
    """Generates HTML for the links section based on defined order."""
    html_parts: List[str] = []
    if not links_dict:
        return ""

    for key in LINK_ORDER:
        url = links_dict.get(key)
        # Ensure URL is not None and not just '#' or empty string
        if url and url.strip() and url != '#':
            display_text = "Cite" if key == 'bibtex' else key.upper()
            # Add target="_blank" and rel="noopener noreferrer" for external links
            html_parts.append(f'[<a href="{url}" target="_blank" rel="noopener noreferrer">{display_text}</a>]')

    # Join with a space for better readability
    return " ".join(html_parts)


def build_publications_html(data: Optional[List[Dict[str, Any]]], owner_name: str, scholar_id: str) -> Optional[str]:
    """Generates the publications.html content using a template."""
    if data is None:
        print("Error: No publication data provided.")
        return None

    # Sort publications: primarily by year descending, secondarily by title ascending
    data.sort(key=lambda x: (-int(x.get('year', 0)), x.get('title', '').lower()))

    pubs_by_year: Dict[str, List[Dict[str, Any]]] = {}
    for pub in data:
        # Use 'Unknown Year' if year is missing or invalid
        year_str = str(pub.get('year', 'Unknown Year'))
        if year_str not in pubs_by_year:
            pubs_by_year[year_str] = []
        pubs_by_year[year_str].append(pub)

    ### Generate HTML for publications list ###
    pubs_by_year_html_parts: List[str] = []
    # Iterate through years in descending order
    for year in sorted(pubs_by_year.keys(), reverse=True):
        pubs_by_year_html_parts.append(f"<h2>{year}</h2>")
        pubs_by_year_html_parts.append("<ul>")
        for pub in pubs_by_year[year]:
            authors_html = format_authors(pub.get('authors', []), owner_name)
            title = pub.get('title', 'Untitled')
            venue = pub.get('venue', '')
            # Get year here to include with venue, fallback to group year
            pub_year = pub.get('year', year)
            links_html = generate_links_html(pub.get('links', {}))

            # Build list item HTML
            list_item_parts = [f'<li>']
            if authors_html:
                list_item_parts.append(f'<p class="pub-authors">{authors_html}.</p>')
            list_item_parts.append(f'<p class="pub-title">{title}.</p>')
            if venue: # Only add venue if it exists
                list_item_parts.append(f'<p class="pub-venue">{venue} ({pub_year}).</p>')
            if links_html: # Only add links paragraph if there are links
                list_item_parts.append(f'<p class="pub-links">{links_html}</p>')
            list_item_parts.append('</li>')
            pubs_by_year_html_parts.append("\n".join(list_item_parts))

        pubs_by_year_html_parts.append("</ul>")

    pubs_by_year_html = "\n".join(pubs_by_year_html_parts)

    ### Generate Google Scholar Link ###
    scholar_link_html = ""
    if scholar_id:
        scholar_url = f"https://scholar.google.com/citations?user={scholar_id}"
        scholar_link_html = f'<p>Selected publications. For a full list, please see my <a href="{scholar_url}" target="_blank" rel="noopener noreferrer">Google Scholar profile</a>.</p>'
    else:
        # Fallback text if for any reason 'scholar_id' is not specified
        scholar_link_html = "<p>Selected publications.</p>" 

    ### Read Template ####
    try:
        with open(PUBS_TEMPLATE, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {PUBS_TEMPLATE}")
        return None
    except IOError as e:
        print(f"Error reading template file {PUBS_TEMPLATE}: {e}")
        return None


    ### Prepare Navigation Context ###
    nav_active = {'active_pubs': 'active'}
    nav_defaults = {'active_about': '', 'active_pubs': '', 'active_talks': '', 'active_blog': '', 'active_vitae': ''}
    nav_context = {**nav_defaults, **nav_active} # Merge

    ### Replace Placeholders ###
    final_html = template_content
    # Replace nav placeholders
    for key, value in nav_context.items():
        final_html = final_html.replace(f"{{{key}}}", value)
    # Replace content placeholders
    final_html = final_html.replace("{AUTHOR_NAME}", owner_name)
    final_html = final_html.replace("{GOOGLE_SCHOLAR_LINK_TEXT}", scholar_link_html)
    final_html = final_html.replace("{PUBLICATIONS_BY_YEAR}", pubs_by_year_html)

    return final_html


def build_talks_html(data: Optional[List[Dict[str, Any]]], owner_name: str) -> Optional[str]:
    """Generates the talks.html content using a template, separating upcoming and past talks."""
    if data is None:
        print("Error: No talks data provided.")
        return None

    # Get current date for comparison (ignoring time)
    today = datetime.now().date()

    upcoming_talks: List[Dict[str, Any]] = []
    past_talks: List[Dict[str, Any]] = []

    # Convert date strings and categorize talks
    for talk in data:
        try:
            # Ensure date is treated as string before parsing
            date_str = str(talk.get('date', ''))
            talk_date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            talk['date_obj'] = talk_date_obj # Store for later use if needed
            talk_date = talk_date_obj.date()

            # Compare talk date with today's date
            if talk_date >= today:
                upcoming_talks.append(talk)
            else:
                past_talks.append(talk)

        except ValueError:
            print(f"Warning: Invalid date format '{talk.get('date', '')}' for talk '{talk.get('title', 'Untitled')}'. Placing in Past.")
            # Assign a very old date to ensure it's sorted correctly in past talks
            talk['date_obj'] = datetime.min
            past_talks.append(talk)

    # Sort upcoming talks chronologically (soonest first)
    upcoming_talks.sort(key=lambda x: x['date_obj'])
    # Sort past talks reverse-chronologically (newest first)
    past_talks.sort(key=lambda x: x['date_obj'], reverse=True)

    ### Generate HTML for Upcoming Talks ###
    upcoming_talks_html_parts: List[str] = []
    if not upcoming_talks:
        upcoming_talks_html_parts.append("<p>No upcoming talks scheduled at the moment. Check back later!</p>")
    else:
        upcoming_talks_html_parts.append("<ul>")
        for talk in upcoming_talks:
            # Format date as "DD Month YYYY"
            date_str_formatted = talk['date_obj'].strftime('%d %B %Y')
            title = talk.get('title', 'Untitled Talk')
            event = talk.get('event', '')
            location = talk.get('location', '')
            links_html = generate_links_html(talk.get('links', {}))

            list_item_parts = [f'<li>']
            list_item_parts.append(f'<strong>{date_str_formatted}</strong>')
            list_item_parts.append(f'{title}')
            # Combine event and location in one paragraph
            event_location_parts = []
            if event:
                event_location_parts.append(f'<em>{event}</em>')
            if location:
                # Add separator only if event also exists
                separator = " - " if event else ""
                event_location_parts.append(f'<span class="talk-location">{separator}{location}</span>')
            if event_location_parts:
                list_item_parts.append(f'<p>{"".join(event_location_parts)}.</p>')

            if links_html: # Only add links paragraph if there are links
                list_item_parts.append(f'<p>{links_html}</p>')
            list_item_parts.append('</li>')
            upcoming_talks_html_parts.append("\n".join(list_item_parts))
        upcoming_talks_html_parts.append("</ul>")
    upcoming_talks_html = "\n".join(upcoming_talks_html_parts)


    ### Generate HTML for Past Talks ###
    past_talks_html_parts: List[str] = []
    if not past_talks:
        past_talks_html_parts.append("<p>No past talks listed yet.</p>")
    else:
        past_talks_html_parts.append("<ul>")
        for talk in past_talks:
            # Format date as "DD Month YYYY" or use original if invalid
            date_str_formatted = talk['date_obj'].strftime('%d %B %Y') if talk['date_obj'] != datetime.min else str(talk.get('date', 'Unknown Date'))
            title = talk.get('title', 'Untitled Talk')
            event = talk.get('event', '')
            location = talk.get('location', '')
            links_html = generate_links_html(talk.get('links', {}))

            list_item_parts = [f'<li>']
            list_item_parts.append(f'<strong>{date_str_formatted}</strong>')
            list_item_parts.append(f'{title}')
            # Combine event and location
            event_location_parts = []
            if event:
                event_location_parts.append(f'<em>{event}</em>')
            if location:
                separator = " - " if event else ""
                event_location_parts.append(f'<span class="talk-location">{separator}{location}</span>')
            if event_location_parts:
                list_item_parts.append(f'<p>{"".join(event_location_parts)}.</p>')

            if links_html:
                list_item_parts.append(f'<p>{links_html}</p>')
            list_item_parts.append('</li>')
            past_talks_html_parts.append("\n".join(list_item_parts))
        past_talks_html_parts.append("</ul>")
    past_talks_html = "\n".join(past_talks_html_parts)

    ### Read Template ###
    try:
        with open(TALKS_TEMPLATE, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"Error: Template file not found at {TALKS_TEMPLATE}")
        return None
    except IOError as e:
        print(f"Error reading template file {TALKS_TEMPLATE}: {e}")
        return None

    ### Prepare Navigation Context ###
    nav_active = {'active_talks': 'active'}
    nav_defaults = {'active_about': '', 'active_pubs': '', 'active_talks': '', 'active_blog': '', 'active_vitae': ''}
    nav_context = {**nav_defaults, **nav_active}

    ### Replace Placeholders ###
    final_html = template_content
    # Replace nav placeholders
    for key, value in nav_context.items():
        final_html = final_html.replace(f"{{{key}}}", value)
    # Replace content placeholders
    final_html = final_html.replace("{AUTHOR_NAME}", owner_name)
    final_html = final_html.replace("{UPCOMING_TALKS}", upcoming_talks_html)
    final_html = final_html.replace("{PAST_TALKS}", past_talks_html)

    return final_html


### Main Execution ###
if __name__ == "__main__":
    print("Building publications page...")
    pubs_data = load_yaml(PUBS_YAML)
    pubs_html = build_publications_html(pubs_data, OWNER_NAME, GOOGLE_SCHOLAR_ID)
    if pubs_html:
        try:
            with open(PUBS_HTML_OUT, 'w', encoding='utf-8') as f:
                f.write(pubs_html)
            print(f"Successfully generated {PUBS_HTML_OUT}")
        except IOError as e:
            print(f"Error writing file {PUBS_HTML_OUT}: {e}")
    else:
        print(f"Failed to generate {PUBS_HTML_OUT}")

    print("\nBuilding talks page...")
    talks_data = load_yaml(TALKS_YAML)
    talks_html = build_talks_html(talks_data, OWNER_NAME)
    if talks_html:
        try:
            with open(TALKS_HTML_OUT, 'w', encoding='utf-8') as f:
                f.write(talks_html)
            print(f"Successfully generated {TALKS_HTML_OUT}")
        except IOError as e:
            print(f"Error writing file {TALKS_HTML_OUT}: {e}")
    else:
        print(f"Failed to generate {TALKS_HTML_OUT}")
