from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel.server import TransportSecuritySettings
import httpx, os, uvicorn

mcp = FastMCP(
    "reddit-search",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "reddit-mcp-feqr.onrender.com",
            "reddit-mcp-feqr.onrender.com:*"
        ]
    ),
    stateless_http=True
)

@mcp.tool()
async def search_reddit_posts(subreddit: str, query: str = "",
    after: str = "", before: str = "", limit: int = 25) -> str:
    """Search Reddit posts by subreddit, keyword, date range"""
    params = {"subreddit": subreddit, "limit": limit}
    if query: params["title"] = query
    if after: params["after"] = after
    if before: params["before"] = before
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(
            "https://arctic-shift.photon-reddit.com/api/posts/search",
            params=params)
        return r.text

@mcp.tool()
async def search_reddit_comments(subreddit: str, query: str = "",
    after: str = "", before: str = "", limit: int = 25) -> str:
    """Search Reddit comments by subreddit, keyword, date range"""
    params = {"subreddit": subreddit, "limit": limit}
    if query: params["body"] = query
    if after: params["after"] = after
    if before: params["before"] = before
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(
            "https://arctic-shift.photon-reddit.com/api/comments/search",
            params=params)
        return r.text

port = int(os.environ.get("PORT", 10000))
uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=port)
