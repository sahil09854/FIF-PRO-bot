from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import ensure_user, get_user

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    db_user = get_user(user.id)

    text = f"""
⚽ *Welcome to FIF-PRO Bot!* ⚽
━━━━━━━━━━━━━━━━━━━━━
Hey *{user.first_name}*! Ready to build your dream squad? 🔥

💰 *Coins:* {db_user['coins']}
🏆 *Record:* {db_user['wins']}W / {db_user['losses']}L / {db_user['draws']}D

━━━━━━━━━━━━━━━━━━━━━
*Commands:*
📦 /pack — Open player packs
👥 /team — View your squad
⚔️ /draft — 5v5 Draft battle
🥊 /battle — 1v1 Dream team battle
👤 /profile — Your stats
━━━━━━━━━━━━━━━━━━━━━
🎁 *New players get 500 coins FREE!*
    """

    keyboard = [
        [InlineKeyboardButton("📦 Open Pack", callback_data="pack_menu"),
         InlineKeyboardButton("👥 My Team", callback_data="team_view")],
        [InlineKeyboardButton("⚔️ Draft Battle", callback_data="draft_menu"),
         InlineKeyboardButton("🥊 1v1 Battle", callback_data="battle_menu")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile_view")]
    ]

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
