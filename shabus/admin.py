from flask import request, redirect, abort, url_for
from flask_admin.contrib import sqla
from flask_security import current_user
from flask_admin import AdminIndexView, expose

def is_superuser():
    if not current_user.is_active() or not current_user.is_authenticated():
        return False

    return current_user.has_role("superuser")

class ProtectedAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        # Logged in as a superuser?
        if is_superuser():
            return super(ProtectedAdminIndexView, self).index()
        # Logged in but not a superuser?
        if current_user.is_authenticated():
            abort(403)
        # User is not logged in.
        return redirect(url_for("security.login", next=request.path))


class ProtectedModelView(sqla.ModelView):
    def is_accessible(self):
        return is_superuser()

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated():
                abort(403)
            else:
                return redirect(url_for("security.login", next=request.path))
