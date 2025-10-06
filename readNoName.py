import os
import requests
import http.client
import urllib

url = "https://witha.name/data/last.json"

def read_keywords_from_csv(filepath):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the CSV file
    full_path = os.path.join(script_dir, filepath)
    
    try:
        with open(full_path, 'r') as f:
            line = f.readline()
        return [kw.strip() for kw in line.split(',') if kw.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find {filepath} in {script_dir}")
        print("Please ensure keywords.csv exists in the same directory as the script.")
        return []


def _find_matching_record(obj, keyword_lower):
    """Recursively search obj (dict/list) and return the first dict that contains the keyword in any string value."""
    if isinstance(obj, dict):
        # If any string value contains the keyword, return this dict
        for v in obj.values():
            if isinstance(v, str) and keyword_lower in v.lower():
                return obj
        # Recurse into values
        for v in obj.values():
            if isinstance(v, (dict, list)):
                found = _find_matching_record(v, keyword_lower)
                if found:
                    return found
    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                found = _find_matching_record(item, keyword_lower)
                if found:
                    return found
            elif isinstance(item, str) and keyword_lower in item.lower():
                # Found a string match inside a list; can't extract fields from a string, return None
                return None
    return None


def _find_all_matching_records(obj, keyword_lower):
    """Recursively search obj (dict/list) and return a list of dicts that contain the keyword in any string value."""
    results = []

    def recurse(o):
        if isinstance(o, dict):
            # If any string value contains the keyword, add this dict
            for v in o.values():
                if isinstance(v, str) and keyword_lower in v.lower():
                    results.append(o)
                    break
            # Recurse into values
            for v in o.values():
                if isinstance(v, (dict, list)):
                    recurse(v)
        elif isinstance(o, list):
            for item in o:
                if isinstance(item, (dict, list)):
                    recurse(item)
                # strings inside lists that match are not associated with a dict to extract fields from

    recurse(obj)
    return results


def fetch_and_search(url, keywords):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_text = response.text
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Try to parse JSON for structured field extraction
    parsed = None
    try:
        parsed = response.json()
    except Exception:
        parsed = None

    found_any = False
    for keyword in keywords:
        if keyword.lower() in data_text.lower():
            # Attempt to locate all matching records in parsed JSON so we can extract fields
            matches = []
            if parsed is not None:
                matches = _find_all_matching_records(parsed, keyword.lower())

            if matches:
                print(f"Warning: Found '{keyword}' in NoName daily announcement! ({len(matches)} occurrence(s))")
                for idx, record in enumerate(matches, start=1):
                    ip = record.get('ip') or record.get('ipv4') or record.get('address')
                    field_type = record.get('type')
                    method = record.get('method')
                    port = record.get('port')
                    path = record.get('path') or record.get('url')

                    # Build list of present fields only
                    details = []
                    if ip is not None and str(ip).strip() != "":
                        details.append(f"  ip: {ip}")
                    if field_type is not None and str(field_type).strip() != "":
                        details.append(f"  type: {field_type}")
                    if method is not None and str(method).strip() != "":
                        details.append(f"  method: {method}")
                    if port is not None and str(port).strip() != "":
                        details.append(f"  port: {port}")
                    if path is not None and str(path).strip() != "":
                        details.append(f"  path: {path}")

                    if details:
                        print(f"Occurrence {idx}:")
                        for line in details:
                            print(line)
            else:
                # No structured matches found; print a generic warning only
                print(f"Warning: Found '{keyword}' in NoName daily announcement!")

            found_any = True
            # Keep Pushover behavior unchanged (one notification per keyword found)
            report_pushover(keyword)

    if not found_any:
        print("No relevant keywords found.")

def report_pushover(keyword):
    message = f"Alert: Found keyword '{keyword}' in NoName daily announcement"
    # Prefer environment variables. Accept both uppercase and lowercase names
    app_token = os.environ.get('PUSHOVER_APP_TOKEN') or os.environ.get('pushover_app_token')
    user_key = os.environ.get('PUSHOVER_USER_KEY') or os.environ.get('pushover_user_key')

    if not app_token or not user_key:
        print("Pushover credentials not set in environment; skipping notification.")
        return

    try:
        # Use host and port separately to avoid host string issues
        conn = http.client.HTTPSConnection("api.pushover.net", 443)
        conn.request(
            "POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": app_token,
                "user": user_key,
                "message": message,
            }),
            {"Content-type": "application/x-www-form-urlencoded"}
        )
        # Always read the response so we can detect errors. Only print body when debugging.
        response = conn.getresponse()
        body = response.read().decode(errors='replace')
        # If debug enabled, print the response status and body (do NOT print credentials)
        if os.environ.get('PUSHOVER_DEBUG'):
            print(f"Pushover response: {response.status} {response.reason}")
            print(body)
        if response.status != 200:
            print(f"Pushover API returned non-200 status: {response.status} {response.reason}")
        conn.close()
    except Exception as e:
        print(f"Error sending Pushover notification: {e}")

if __name__ == "__main__":
    keywords = read_keywords_from_csv("keywords.csv")
    if not keywords:
        print("No keywords found. Exiting.")
        exit(1)
    fetch_and_search(url, keywords)
