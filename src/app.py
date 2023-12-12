from setup import app
from blueprints.cli_bp import db_commands
from blueprints.users_bp import user_bp
from blueprints.diaries_bp import diaries_bp
from blueprints.meeting_bp import meetings_bp
from blueprints.groups_bp import groups_bp
from blueprints.entities_bp import entities_bp
from blueprints.events_bp import events_bp


app.register_blueprint(db_commands)
app.register_blueprint(user_bp)
app.register_blueprint(diaries_bp)
app.register_blueprint(meetings_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(entities_bp)
app.register_blueprint(events_bp)

print(app.url_map)
