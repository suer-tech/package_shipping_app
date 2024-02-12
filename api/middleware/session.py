import secrets
import string

from starlette.requests import Request


class SessionMiddleware:
    def __init__(
        self,
        session_cookie_name: str = "session_id",
        request_state_session_id_name: str = "user_session_id",
        session_id_length: int = 10,
    ):
        self.session_cookie_name = session_cookie_name
        self.session_id_length = session_id_length
        self.request_state_session_id_name = request_state_session_id_name

    def generate_session_id(self):
        characters = string.ascii_letters + string.digits

        session_id = "".join(
            secrets.choice(characters) for _ in range(self.session_id_length)
        )

        return session_id

    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get(self.session_cookie_name)

        if not session_id:
            session_id = self.generate_session_id()

        request.scope[self.request_state_session_id_name] = session_id
        response = await call_next(request)

        response.set_cookie(self.session_cookie_name, session_id)
        return response

    def get_current_session_id(self, request: Request):
        return request.scope[self.request_state_session_id_name]


session_middleware = SessionMiddleware()
