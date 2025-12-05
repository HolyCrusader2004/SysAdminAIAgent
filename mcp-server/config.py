import os

class Config:
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))

    AUTH_HOST: str = os.getenv("AUTH_HOST", "keycloak")
    AUTH_PORT: int = int(os.getenv("AUTH_PORT", "8080"))
    AUTH_REALM: str = os.getenv("AUTH_REALM", "master")

    OAUTH_CLIENT_ID: str = os.getenv("OAUTH_CLIENT_ID", "mcp_server")
    OAUTH_CLIENT_SECRET: str = os.getenv("OAUTH_CLIENT_SECRET", "i94YxgUaNqoqLsNo3pUjZoKDwd5b41Bx")

    MCP_SCOPE: str = os.getenv("MCP_SCOPE", "mcp:tools")
    TRANSPORT: str = os.getenv("TRANSPORT", "streamable-http")
    MOUNT_PATH: str = os.getenv("MOUNT_PATH", "/mcp")

    @property
    def server_url(self) -> str:
        return f"http://{self.HOST}:{self.PORT}{self.MOUNT_PATH}"

    @property
    def auth_base_url(self) -> str:
        return f"http://{self.AUTH_HOST}:{self.AUTH_PORT}/realms/{self.AUTH_REALM}"

        
config = Config()