import json
import os

from jupyterhub.services.auth import HubOAuthenticated, HubOAuthCallbackHandler
from tornado import httpclient, ioloop, web
from tornado.gen import maybe_future


API_URL = os.environ.get("JUPYTERHUB_API_URL", "")
API_TOKEN = os.environ.get("JUPYTERHUB_API_TOKEN", "")
SERVICE_PORT = int(os.environ.get("THEBE_SERVICE_PORT", "10101"))
COOKIE_SECRET = os.environ.get("THEBE_COOKIE_SECRET")
if not COOKIE_SECRET:
    COOKIE_SECRET = os.urandom(32)


class HubClientMixin(HubOAuthenticated):
    """Base handler that knows how to talk to the Hub API."""

    def initialize(self, client):
        self.http = client
        super().initialize()

    @property
    def username(self):
        """Get username from current_user after authentication."""
        user = self.current_user
        if user:
            return user.get("name")
        return None

    def _require_username(self):
        if not self.username:
            raise web.HTTPError(403, "User not authenticated")
        return self.username

    async def hub_request(self, path, method="GET", body=None):
        token = API_TOKEN
        headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json",
        }
        request = httpclient.HTTPRequest(
            url=f"{API_URL}{path}",
            method=method,
            headers=headers,
            body=body if body is not None else None,
        )
        return await self.http.fetch(request, raise_error=False)

    def write_error(self, status_code, **kwargs):
        message = kwargs.get("exc_info", ("", "", ""))[1]
        self.finish({"error": str(message), "status": status_code})


class StatusHandler(HubClientMixin, web.RequestHandler):
    @web.authenticated
    async def get(self):
        # Ensure the browser receives an _xsrf cookie scoped at '/'
        _ = self.xsrf_token
        username = self._require_username()
        resp = await self.hub_request(f"/users/{username}")
        if resp.code >= 400:
            self.set_status(resp.code)
            self.finish({"error": resp.body.decode("utf-8")})
            return
        data = json.loads(resp.body.decode("utf-8"))
        server = data.get("servers", {}).get("", {})
        ready = bool(server.get("ready"))
        self.finish({"ready": ready, "server_url": server.get("url")})


class SpawnHandler(HubClientMixin, web.RequestHandler):
    @web.authenticated
    async def post(self):
        username = self._require_username()
        resp = await self.hub_request(
            f"/users/{username}/server",
            method="POST",
            body="{}",
        )
        self.set_status(resp.code)
        if resp.code in (201, 202):
            self.finish({"status": "spawning"})
        else:
            self.finish({"error": resp.body.decode("utf-8"), "status": resp.code})


class RootHandler(web.RequestHandler):
    """Simple health check handler - no OAuth required."""
    def get(self):
        self.finish({"service": "thebe-proxy", "status": "ok"})


def make_app():
    client = httpclient.AsyncHTTPClient()
    # With base_url='/', services are at /services/thebe-proxy/
    # ConfigProxy forwards the full path, so we match it
    prefix = r"/services/thebe-proxy"
    handlers = [
        # Root handler for health checks (no OAuth)
        (rf"{prefix}/?", RootHandler),
        (r"/?", RootHandler),
        # OAuth callback handler (required for HubOAuthenticated)
        (rf"{prefix}/oauth_callback", HubOAuthCallbackHandler),
        (r"/oauth_callback", HubOAuthCallbackHandler),
        # Status/spawn handlers (require @web.authenticated)
        (rf"{prefix}/status", StatusHandler, {"client": client}),
        (rf"{prefix}/spawn", SpawnHandler, {"client": client}),
        # Direct access (for internal testing)
        (r"/status", StatusHandler, {"client": client}),
        (r"/spawn", SpawnHandler, {"client": client}),
    ]
    settings = {
        "cookie_secret": COOKIE_SECRET if isinstance(COOKIE_SECRET, str) else COOKIE_SECRET,
        "xsrf_cookies": True,
        "xsrf_cookie_kwargs": {"path": "/"},
    }
    return web.Application(handlers, **settings)


def main():
    if not API_URL or not API_TOKEN:
        raise RuntimeError("JUPYTERHUB_API_URL and JUPYTERHUB_API_TOKEN must be set")
    app = make_app()
    app.listen(SERVICE_PORT)
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
