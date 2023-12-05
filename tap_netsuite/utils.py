import re

def config_type(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()