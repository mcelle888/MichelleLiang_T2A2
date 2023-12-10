from controllers.auth_controller import auth
from controllers.diaries_controller import diaries
from controllers.meetings_controller import meetings
from controllers.entities_controller import entities

registerable_controllers = [
    auth,
    diaries,
    meetings,
    entities,
]