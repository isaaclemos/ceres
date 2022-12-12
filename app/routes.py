from mvc_flask import Router

Router.get("/", "auth#index")
Router.post('/login','auth#login')
Router.get("/logout", "auth#logout")


user = Router.namespace("/user")
user.post('/station/<int:id>/et', "evapo#et_info")
user.get('/station/<int:id>/et/<date_filter>', 'evapo#et_info_today')
user.get('', 'user#index')
user.get('/station', 'station#station')
user.get('/profile', 'user#profile')
user.post('/profile/update', 'user#profile_update')

admin = Router.namespace('/admin')
admin.get('/user','admin#user_show')
admin.post('/user','admin#user_create')
admin.get('/user/<int:id>/edit','admin#user_edit')
admin.post('/user/<int:id>/delete','admin#user_update')
admin.get('/user/<int:id>/delete','admin#user_delete')

admin.get('/user/<int:user_id>/station','admin#stations_by_user')
admin.post('/user/<int:user_id>/station/create', 'admin#station_create')
admin.get('/user/<int:user_id>/station/<int:station_id>/edit', 'admin#station_edit')
admin.post('user/<int:user_id>/station/<int:station_id>/update', 'admin#station_update')
admin.get('/user/<int:user_id>/station/<int:station_id>/delete', 'admin#station_delete')

api = Router.namespace('/api/v1')
api.post('/', 'twosource#api_v1')
api.get('/<name>','evapo#show_image')

