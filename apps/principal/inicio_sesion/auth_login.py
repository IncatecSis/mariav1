from django.contrib import messages
from django.utils import timezone
import datetime

MAX_ATTEMPTS = 3
BLOCK_TIME = 30 

def initialize_login_attempts(session):
    session.setdefault('failed_attempts', 0)
    session.setdefault('blocked_until', None)


def is_user_blocked(session):
    blocked_until = session.get('blocked_until')
    if blocked_until:
        blocked_until = datetime.datetime.fromisoformat(blocked_until)
        remaining_time = (blocked_until - timezone.now()).total_seconds()
        
        if remaining_time > 0:
            return True, int(remaining_time)

        session['failed_attempts'] = 0
        session['blocked_until'] = None
    return False, 0

def handle_failed_attempt(session):
    session['failed_attempts'] = session.get('failed_attempts', 0) + 1
    if session['failed_attempts'] >= MAX_ATTEMPTS:
        blocked_until = timezone.now() + datetime.timedelta(seconds=BLOCK_TIME)
        session['blocked_until'] = blocked_until.isoformat()
        return True, BLOCK_TIME

    remaining_attempts = MAX_ATTEMPTS - session['failed_attempts']
    return False, remaining_attempts

def clear_session_expiration_cookie(request, response):
    if '/admin' in request.path:
        return response
    
    if request.COOKIES.get('session_expired') == 'true' or request.session.get('session_expired'):
        response.delete_cookie('session_expired')
        request.session.pop('session_expired', None)
        messages.warning(request, 'Se cerró la sesión por inactividad...😕')
    return response
