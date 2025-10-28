import discord
from discord.ext import tasks, commands
import requests
from bs4 import BeautifulSoup
import re
from keep_alive import keep_alive  # ✅ Giữ bot sống 24/24

TOKEN = "NHẬP_TOKEN_BOT_DISCORD_VÀO_ĐÂY"  # 🔹 Thay bằng token bot của bạn
CHANNEL_ID = 1432358007471210549# ID kênh Discord muốn gửi code

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
last_codes = set()

# ======== HÀM LẤY CODE HONKAI ========

def get_latest_codes():
    """Lấy code Honkai Star Rail mới nhất từ Hoyolab"""
    url = "https://www.hoyolab.com/article_list/35/2"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    codes = set()
    for article in soup.find_all("a", href=True):
        found = re.findall(r"\b[A-Z0-9]{10,}\b", article.get_text())
        for code in found:
            if len(code) >= 10:
                codes.add(code)
    return codes


# ======== KIỂM TRA CODE MỚI ========

@tasks.loop(minutes=30)
async def check_codes():
    global last_codes
    new_codes = get_latest_codes()
    diff = new_codes - last_codes
    if diff:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("🎁 **Code Honkai Star Rail mới!**\n" + "\n".join(diff))
        last_codes = new_codes


# ======== SỰ KIỆN BOT ========

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")
    check_codes.start()


# ======== CHẠY BOT 24/24 ========
keep_alive()  # ✅ Giữ cho Replit luôn bật
bot.run(TOKEN)
