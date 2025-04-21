from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.utils.deprecation import MiddlewareMixin

class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = [settings.LOGIN_URL, '/admin/']

        if any(request.path.startswith(path) for path in excluded_paths):
            return

        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_time = timezone.now()

            if last_activity:
                try:
                    last = timezone.datetime.fromisoformat(last_activity)
                    inactive = current_time - last

                    if inactive > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                        auth_logout(request)
                        return redirect(f"{settings.LOGIN_URL}?session_expired=true")
                except ValueError:
                    request.session['last_activity'] = current_time.isoformat()

            request.session['last_activity'] = current_time.isoformat()
