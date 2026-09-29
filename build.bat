cd /d %~dp0
py -m pip freeze > requirements.txt
py unify_build_html.py
py update_conf.py
py run_build_html.py
py make_pages_site.py
py make_readme.py
