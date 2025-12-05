from typing import Any
import base64

from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.shared.auth_utils import check_resource_allowed, resource_url_from_server_url


class IntrospectionTokenVerifier(TokenVerifier):
    """Token verifier that uses OAuth 2.0 Token Introspection (RFC 7662)."""

    def __init__(
        self,
        introspection_endpoint: str,
        server_url: str,
        client_id: str,
        client_secret: str,
    ):
        self.introspection_endpoint = introspection_endpoint
        self.server_url = server_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.resource_url = resource_url_from_server_url(server_url)
        

    async def verify_token(self, token: str) -> AccessToken | None:
        """Verify token via introspection endpoint."""
        import httpx

        if not self.introspection_endpoint.startswith(("http://", "https://")):
            return None

        timeout = httpx.Timeout(10.0, connect=5.0)
        limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)

        async with httpx.AsyncClient(
            timeout=timeout,
            limits=limits,
            verify=False,  
        ) as client:
            try:
                auth_string = f"{self.client_id}:{self.client_secret}"
                auth_bytes = auth_string.encode('ascii')
                base64_auth = base64.b64encode(auth_bytes).decode('ascii')
                
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {base64_auth}"
                }
                
                form_data = {
                    "token": token,
                }
                
                response = await client.post(
                    self.introspection_endpoint,
                    data=form_data,
                    headers=headers,
                )

                if response.status_code != 200:
                    return None

                data = response.json()
                
                if not data.get("active", False):
                    return None
        
                scopes = []
                scope_value = data.get("scope")
                if scope_value:
                    if isinstance(scope_value, str):
                        scopes = scope_value.split()
                    elif isinstance(scope_value, list):
                        scopes = scope_value
                
                client_id = data.get("client_id") or data.get("azp") or "unknown"
                
                return AccessToken(
                    token=token,
                    client_id=client_id,
                    scopes=scopes,
                    expires_at=data.get("exp"),
                    resource=data.get("aud"),
                )

            except Exception as e:
                return None

    def _validate_resource(self, token_data: dict[str, Any]) -> bool:
        """Validate token was issued for this resource server.
        """
        if not self.server_url or not self.resource_url:
            return True  

        aud: list[str] | str | None = token_data.get("aud")
        
        if aud is None:
            return True  
        
        if isinstance(aud, list):
            result = any(self._is_valid_resource(a) for a in aud)
            return result
        if isinstance(aud, str):
            result = self._is_valid_resource(aud)
            return result
        
        return False

    def _is_valid_resource(self, resource: str) -> bool:
        """Check if the given resource matches our server."""
        try:
            result = check_resource_allowed(self.resource_url, resource)
            return result
        except Exception as e:
            return False