py -m venv env
CALL env\Scripts\activate
cd app
flask --app __init__:create_app() run
pause