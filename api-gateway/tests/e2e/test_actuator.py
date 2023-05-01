"""
Test for actuator endpoints
"""
from starlette.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY


class TestActuator:
    """
    Tests for actuator endpoints.
    """

    LIVELINESS_PATH = "/health"
    READINESS_PATH = "/readiness"

    def test_root_redirect_to_docs_permanently(self, test_client):
        """
        GIVEN a FastAPI application
        WHEN the root path is requested (GET)
        THEN it is redirected to the docs path
        """
        # when
        response = test_client.get("/").history[0]

        # then
        assert response.status_code == HTTP_301_MOVED_PERMANENTLY
        assert response.headers["location"] == "/docs"

    def test_health_check(self, test_client):
        """
        GIVEN a FastAPI application
        WHEN the health check path is requested (GET)
        THEN it returns a 200 status code
        """
        # when
        response = test_client.get(self.LIVELINESS_PATH)

        # then
        assert response.status_code == HTTP_200_OK

    def test_readiness_check(self, test_client):
        """
        GIVEN a FastAPI application
        WHEN the readiness check path is requested (GET)
        THEN it returns a 200 status code
        """
        # when
        response = test_client.get(self.READINESS_PATH)

        # then
        assert response.status_code == HTTP_200_OK
