import os
import dotenv
import uvicorn
import discord
from discord.ext.ipc import Client
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from backend import DiscordAuth, db


# Hier die Daten aus dem Developer-Portal einfügen
# env vars
dotenv.load_dotenv()
CLIENT_ID = int(os.getenv("CLIENT_ID"))
CLIENT_SECRET = str(os.getenv("CLIENT_SECRET"))
REDIRECT_URI = "http://161.97.81.181:8000/callback"
LOGIN_URL = "https://discord.com/api/oauth2/authorize?client_id=1156661228047958107&redirect_uri=http%3A%2F%2F161.97.81.181%3A8000%2Fcallback&response_type=code&scope=identify%20email%20guilds%20guilds.members.read%20messages.read"


app = FastAPI()
app.mount("/static", StaticFiles(directory="./src/frontend/static"), name="static")
templates = Jinja2Templates(directory="./src/frontend")

ipc = Client(secret_key="yasuna")
api = DiscordAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

@app.on_event("startup")
async def on_startup():
    await api.setup()
    await db.setup()


@app.get("/")
async def home(request: Request):
    guild_count = await ipc.request("guild_count")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "count": guild_count.response,
            "login_url": LOGIN_URL
        }
    )


@app.get("/callback")
async def callback(code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    result = await api.get_token_response(data)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid Auth Code")

    token, refresh_token, expires_in = result
    user = await api.get_user(token)
    user_id = user.get("id")
    user_email = user.get('email')
    
    print(user)

    session_id = await db.add_session(token, refresh_token, expires_in, user_id, user_email)

    response = RedirectResponse(url="/guilds")
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return response


@app.get("/guilds")
async def guilds(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="no auth")

    session = await db.get_session(session_id)
    token, refresh_token, token_expires_at, user_id, user_email = session

    user = await api.get_user(token)
    user_guilds: list[dict] = await api.get_guilds(token)
    
    perms = []
    
    for guild in user_guilds:
        guild["url"] = "/server/" + str(guild["id"])

        if guild["icon"]:
            guild["icon"] = "https://cdn.discordapp.com/icons/" + guild["id"] + "/" + guild["icon"]
        else:
            guild["icon"] = "https://cdn.discordapp.com/embed/avatars/0.png"

        is_admin = discord.Permissions(int(guild["permissions"])).administrator
        if is_admin or guild["owner"]:
            perms.append(guild)
            
    perms_without_bot = []
    perms_with_bot = []

    for guild in perms:
        stats = await ipc.request("guild_stats", guild_id=int(guild["id"]))
        print(f"Guild {guild['id']} stats: {stats.response}")
        if stats.response is not None and stats.response != 'None':
            perms_with_bot.append(guild)
            
        if stats.response is None or stats.response == 'None':
            perms_without_bot.append(guild)

    print(perms_with_bot)
    print(perms_without_bot)
    print(perms)
            
    return templates.TemplateResponse(
        "guilds.html",
        {
            "request": request,
            "global_name": user["global_name"],
            "guilds_with_bot": perms_with_bot,
            "guilds_without_bot": perms_without_bot
        }
    )
    
@app.get("/server/{guild_id}")
async def server(request: Request, guild_id: int):
    session_id = request.cookies.get("session_id")
    if not session_id or not await db.get_session(session_id):
        raise HTTPException(status_code=401, detail="no auth")

    stats = await ipc.request("guild_stats", guild_id=guild_id)

    return templates.TemplateResponse(
        "server.html",
        {
            "request": request,
            "stats": stats.response,
            "id": guild_id,
        }
    )

if __name__ == '__main__':
    # uvicorn.run(app, host="161.97.81.181", port=8000)
    uvicorn.run("web:app", host="161.97.81.181", port=8000, reload=True)
    