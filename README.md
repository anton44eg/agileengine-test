# Build

Python 3.6+ required

`pip install -r requirements.txt`

# Run

Mandatory env settings:

API_KEY

Optional env settings:

REFRESH_PERIOD (10 by default)
HTTP_HOST (127.0.0.1 by default)
HTTP_PORT (8080 by default)

`export API_KEY=YOUR_API_KEY`
`python main.py`

# Test

`curl http://localhost:8080/search/Bustling%20Dark`