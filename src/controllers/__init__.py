from controllers.auth_controller import auth
from controllers.diaries_controller import diaries
from controllers.meetings_controller import meetings

registerable_controllers = [
    auth,
    diaries,
    meetings,
]