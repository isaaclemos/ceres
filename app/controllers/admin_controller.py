from flask import abort
from flask_login import current_user, login_required

from app.controllers.station_controller import StationController
from app.controllers.user_controller import UserController

class AdminController:
    before_action=['check_admin'] 
    
    def __init__(self) -> None:
        self.user_controller = UserController()   
        self.station_controller = StationController()
    
    @login_required
    def check_admin(self):
        if not current_user.is_admin:
            return abort(403)

    def user_show(self):        
       return self.user_controller.user_show()
        

    def user_create(self):
       return self.user_controller.create()

    def user_edit(self,id):
        return self.user_controller.edit(id)
    
    def user_update(self,id):
        return self.user_controller.update(id)

    def user_delete(self, id):
        return self.user_controller.delete(id)


    def stations_by_user(self,user_id):
        return self.station_controller.stations_by_user(user_id)

    def station_create(self,user_id):
        return self.station_controller.create(user_id)
    
    def station_edit(self, station_id, user_id):
        return self.station_controller.edit(id=station_id,user_id=user_id)
    
    def station_update(self, user_id, station_id):
        return self.station_controller.update(id=station_id)

    def station_delete(self,user_id, station_id):
        return self.station_controller.delete(id=station_id)
    