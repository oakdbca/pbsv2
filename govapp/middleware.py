"""DBCA Django Project Middleware."""

from typing import Callable

from dbca_utils.middleware import SSOLoginMiddleware
from django import http

GetResponseFunction = Callable[[http.HttpRequest], http.HttpResponse]


class CacheControl:
    """DBCA Cache Control Middleware."""

    def __init__(self, get_response: GetResponseFunction) -> None:
        """Instantiates the CacheControl middleware.

        Args:
            get_response (GetResponseFunction): The 'get_response' function
                injected by Django at middleware load-time.
        """
        # Set the `get_response` method.
        self.get_response = get_response

    def __call__(self, request: http.HttpRequest) -> http.HttpResponse:
        """Handles the functionality of the middleware.

        Args:
            request (http.HttpRequest): HTTP request to handle.

        Returns:
            http.HttpResponse: The handled response.
        """
        # Retrieve the response to the request
        response = self.get_response(request)

        # Check the request path
        if request.path[:5] == "/api/":
            # Do not cache /api/ calls
            response["Cache-Control"] = "private, no-store"

        elif request.path[:8] == "/static/":
            # Cache all /static/ calls for 1 day  <-- lowered to 60 seconds for development purposes
            response["Cache-Control"] = "public, max-age=60"

        elif request.path[:7] == "/media/":
            # Cache all /media/ calls for 1 day  <-- lowered to 60 seconds for development purposes.
            response["Cache-Control"] = "public, max-age=60"

        else:
            # Ignore other paths
            pass

        # Return handled response
        return response


class PBSV2SSOLoginMiddleware(SSOLoginMiddleware):
    """Overide the SSOLoginMiddleware to set or delete the session variablers that
    are required by webtemplate_dbca. TODO: Remove this once Jason has updated
    the dbca_utils SSOLoginMiddleware."""

    def process_request(self, request):
        if request.path.startswith("/logout"):
            del request.session["is_authenticated"]
            del request.session["user_obj"]

        super().process_request(request)

        if request.user.is_authenticated:
            request.session["is_authenticated"] = True
            user_obj = {
                "user_id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "is_staff": request.user.is_staff,
            }
            request.session["user_obj"] = user_obj


class MissingDataNagScreenMiddleware:
    """TODO: If there is mandatory user profile information that must be entered before the user can
    use the application then use this, otherwise delete."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
