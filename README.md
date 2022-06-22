# pledgx

This is the Flask + MySQL API component of the test assignment (part 2)

- - -

## Installation

**Ensure that MySQL server is running!**

1. Clone the repository
2. Enter your MySQL server credentials in pledgx_api/secrets.json
	* Only the development_secrets is used in this test. Production credentials, as well as the switch in server.py are there to illustrate scalability
3. Create a virtual environment
	* `python3 -m venv venv`
4. Activate the virtual environment
	* ex.: `source /pledgx_api/venv/bin/activate`
5. Install requirements
	* `pip install -r /pledgx_api/requirements.txt`
6. Export Flask app
	* `export FLASK_APP=server`
7. Run test server
	* `flask run`