# NoName Announcement Monitor

This Python script monitors the NoName daily announcement at https://witha.name/data/last.json for specified keywords and sends alerts via Pushover if any are found.

## Files
- `readNoName.py`: Main Python script for monitoring and alerting.
- `keywords.csv`: Comma-separated list of keywords to search for in the announcement.

## Usage
1. Edit `keywords.csv` to include the keywords you want to monitor (e.g., company names, domains, IPs).
2. Run the script:
   ```bash
   python3 readNoName.py
   ```
3. If a keyword is found, a warning is printed and a Pushover notification is sent.

## Requirements
- Python 3
- `requests` library (install with `pip install requests`)

## Pushover Setup
The script uses Pushover for notifications. You need to set your own `app_token` and `user_key` in the script for notifications to work.

## Customization
- To change keywords, edit `keywords.csv`.
- To change notification behavior, modify the `report_pushover` function in the script.

## License
MIT License
