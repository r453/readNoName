import requests
import http.client
import urllib

url = "https://witha.name/data/last.json"

def read_keywords_from_csv(filepath):
    with open(filepath, 'r') as f:
        line = f.readline()
    return [kw.strip() for kw in line.split(',') if kw.strip()]

def fetch_and_search(url, keywords):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    found = False
    for keyword in keywords:
        if keyword.lower() in data.lower():
            print(f"Warning: Found '{keyword}' in NoName daily announcement!")
            found = True
            report_pushover(keyword)
    if not found:
        print("No relevant keywords found.")

def report_pushover(keyword):
    message = f"Alert: Found keyword '{keyword}' in NoName daily announcement"
    app_token = "changeme"
    user_key = "changeme"
    try:
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST", "/1/messages.json",
            urllib.parse.urlencode({
                "token": app_token,
                "user": user_key,
                "message": message,
            }),
            {"Content-type": "application/x-www-form-urlencoded"}
        )
        # response = conn.getresponse() # For debugging purposes
        # print(response.read().decode())
    except Exception as e:
        print(f"Error sending Pushover notification: {e}")

if __name__ == "__main__":
    keywords = read_keywords_from_csv("keywords.csv")
    fetch_and_search(url, keywords)
