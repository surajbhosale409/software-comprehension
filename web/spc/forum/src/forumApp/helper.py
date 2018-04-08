from string import Template
import os

TEMPLATE_DIR = os.path.dirname(__file__)

def render_from_string(template_string, mapping):
    template = Template(template_string)
    result = template.safe_substitute(mapping)
    
    return result.encode()

def render(templatename, mapping):
    tpath = os.path.join(TEMPLATE_DIR, templatename)
    if not os.path.exists(tpath):
        return b"Error processing template"

    with open(tpath, 'r') as template:
        body = template.read().replace('\t', '').replace('\n', '')

    return render_from_string(body, mapping)
