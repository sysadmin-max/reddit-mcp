from mcp.server.fastmcp import FastMCP
import httpx, os, uvicorn

render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
mcp = FastMCP("reddit-search", allowed_hosts=[render_host, "localhost", "127.0.0.1"])

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
