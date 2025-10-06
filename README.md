# NoName Announcement Monitor

This Python script monitors the NoName daily announcement at https://witha.name/data/last.json for specified keywords and sends alerts via Pushover if any are found.

## Features
- **Structured Data Extraction**: Parses JSON data and extracts relevant fields (IP, type, method, port, path) from matching records
- **Multiple Match Detection**: Shows all occurrences of keywords with detailed information
- **Environment Variable Support**: Uses environment variables for Pushover credentials (safer than hardcoded values)
- **Robust File Handling**: Automatically finds keywords.csv relative to script location
- **Error Handling**: Graceful handling of missing files and network errors

## Files
- `readNoName.py`: Main Python script for monitoring and alerting.
- `keywords.csv`: Comma-separated list of keywords to search for in the announcement.
- `requirements.txt`: Python dependencies list.

## Usage
1. Edit `keywords.csv` to include the keywords you want to monitor (e.g., company names, domains, IPs).
2. Set up Pushover credentials (optional):
   ```bash
   export PUSHOVER_APP_TOKEN="your_app_token"
   export PUSHOVER_USER_KEY="your_user_key"
   ```
3. Run the script:
   ```bash
   python3 readNoName.py
   ```
4. If a keyword is found, a warning is printed with detailed information and a Pushover notification is sent (if configured).

## Requirements
- Python 3
- `requests` library (install with `pip install -r requirements.txt`)

## Pushover Setup
The script uses Pushover for notifications. Set the following environment variables:
- `PUSHOVER_APP_TOKEN`: Your Pushover application token
- `PUSHOVER_USER_KEY`: Your Pushover user key

Optional debug environment variable:
- `PUSHOVER_DEBUG`: Set to any value to enable debug output for Pushover responses

If credentials are not set, the script will still run but skip notifications.

## Output Format
When keywords are found, the script displays:
- Keyword that was matched
- Number of occurrences
- For each occurrence (if structured data is available):
  - IP address
  - Type
  - Method
  - Port
  - Path/URL

## Customization
- To change keywords, edit `keywords.csv`.
- To modify notification behavior, edit the `report_pushover` function in the script.
- To change extracted fields, modify the field extraction logic in `fetch_and_search` function.

## License
MIT License
