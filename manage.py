from flask import Flask, render_template
from config import session_key, app_config, mongo_config
from Controllers import PageRoutes, ErrorRoutes

app = Flask(__name__)

@app.errorhandler(405)
def redirect(e):
    return render_template("grid.html")
# app settings
app.secret_key = session_key
app.static_folder = app_config['ROOT_PATH'] + '/Views/static'
app.template_folder = app_config['ROOT_PATH'].split('Controllers')[0] + '/Views/templates'
app.register_error_handler(405, redirect)


# blueprints init
blueprints = [
    PageRoutes.mod,
    ErrorRoutes.mod
]
for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host="localhost", port=5010, debug=True)
