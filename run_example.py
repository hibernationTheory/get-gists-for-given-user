import os
import get_gists as get_gists

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PAGES_DIR = os.path.join(CURRENT_DIR, 'pages')

get_gists.run('<username>', PAGES_DIR, "_blog-post_")