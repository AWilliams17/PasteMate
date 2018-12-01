from PasteMate.api import api
from PasteMate.api.resources import Ping, RegisterUser, LoginUser, RevokeAccess, RefreshUser, CurrentUser, \
    SubmitPaste, ViewPaste, ListPastes, EditPaste, DeletePaste

api.add_resource(Ping, '/api/test/ping')
api.add_resource(RegisterUser, '/api/user/register')
api.add_resource(LoginUser, '/api/user/login')
api.add_resource(RefreshUser, '/api/auth/refresh')
api.add_resource(CurrentUser, '/api/auth/current_user')
api.add_resource(RevokeAccess, '/api/auth/revoke')
api.add_resource(SubmitPaste, '/api/paste/submit')
api.add_resource(ViewPaste, '/api/paste/view/<string:paste_uuid>')
api.add_resource(EditPaste, '/api/paste/edit/<string:paste_uuid>')
api.add_resource(ListPastes, '/api/paste/list/<string:page>')
api.add_resource(DeletePaste, '/api/paste/delete/<string:paste_uuid>')
