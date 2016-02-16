#Get Gists for Given User

A small Python script that downloads the gists for the given user (that optionally starts with the given prefix) into target folder. The sample usage is illustrated in the `run_example.py` file.

##Example
```
import os
import get_gists as get_gists

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PAGES_DIR = os.path.join(CURRENT_DIR, 'pages')

get_gists.run('<username>', PAGES_DIR, "_blog-post_")
```