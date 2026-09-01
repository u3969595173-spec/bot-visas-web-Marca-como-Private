import requests

try:
    response = requests.get('https://capitaliberia.com', timeout=10)
    print("URL Final:", response.url)
    print("Status:", response.status_code)
    # Print the first 500 characters of the HTML to see what platform it is
    print("HTML:\n", response.text[:500])
except Exception as e:
    print("Error:", e)
