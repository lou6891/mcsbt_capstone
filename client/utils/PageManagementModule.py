# References
# Forum from which the code is from:
# https://discuss.streamlit.io/t/how-to-hide-all-pages-before-login/32508/8

from streamlit.source_util import _on_pages_changed, get_pages

import json
from pathlib import Path

DEFAULT_PAGE = "Home.py"


def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

    return saved_default_pages


def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()


def show_all_pages():
    current_pages = get_pages(DEFAULT_PAGE)

    saved_pages = get_all_pages()

    missing_keys = set(saved_pages.keys()) - set(current_pages.keys())

    # Replace all the missing pages
    for key in missing_keys:
        current_pages[key] = saved_pages[key]

    _on_pages_changed.send()


def hide_page(page_name: str):
    current_pages = get_pages(page_name)

    for key, val in current_pages.items():
        if val["page_name"] == page_name:
            del current_pages[key]
            _on_pages_changed.send()
            break
