import re

def config_type(text):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()

def get_api_version_from_urn(urn: str) -> str:
    matches = re.search(r"_(\d+_\d+).", urn)
    if matches:
        return matches.group(1)
    return "2025_1"
