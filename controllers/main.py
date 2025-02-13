from odoo import http
from odoo.http import request
import werkzeug

class AutoAuthController(http.Controller):

    @http.route('/web/login', type='http', auth="none")
    def auto_auth(self, **kwargs):
        # Check if a session_id is provided in the query parameters
        session_id = request.params.get('session_id')
        if session_id:
            # Validate the session ID
            session = request.session
            session.sid = session_id
            session.authenticate(request.session.db, request.session.login, request.session.password)

            # If the session is valid, set the session ID in the cookies
            if session.uid:
                response = werkzeug.utils.redirect('/web')
                response.set_cookie('session_id', session_id)
                return response

        # If no session_id is provided or it's invalid, show the default login page
        return request.render('web.login', {})