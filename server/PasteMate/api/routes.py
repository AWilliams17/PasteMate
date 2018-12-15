"""
Defines all API endpoints in the server.
"""
from PasteMate.api import api
from PasteMate.api.resources.user import (LoginUser, RegisterUser, CurrentUser, RefreshUser,
                                          RevokeAccess, UpdateEmail, UpdatePassword, DeleteUser,
                                          ResetPasswordFormSend, ResetPasswordFormReceive)
from PasteMate.api.resources.paste import SubmitPaste, GetPaste, UpdatePaste, DeletePaste, ListPastes

api.add_resource(RegisterUser, '/api/user/register')
api.add_resource(LoginUser, '/api/user/login')
api.add_resource(RefreshUser, '/api/auth/refresh')
api.add_resource(CurrentUser, '/api/auth/current_user')
api.add_resource(RevokeAccess, '/api/auth/revoke')
api.add_resource(UpdateEmail, '/api/user/update_email')
api.add_resource(UpdatePassword, '/api/user/update_password')
api.add_resource(ResetPasswordFormSend, '/api/user/reset_password')
api.add_resource(ResetPasswordFormReceive, '/api/user/reset_password_finalize')
api.add_resource(DeleteUser, '/api/user/delete')
api.add_resource(SubmitPaste, '/api/paste/submit')
api.add_resource(GetPaste, '/api/paste/get/<string:paste_uuid>')
api.add_resource(UpdatePaste, '/api/paste/update/<string:paste_uuid>')
api.add_resource(ListPastes, '/api/paste/list/<string:page>')
api.add_resource(DeletePaste, '/api/paste/delete/<string:paste_uuid>')
