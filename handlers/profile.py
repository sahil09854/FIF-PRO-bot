from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import ensure_user, get_user, get_user_players
from database.players import RARITY_EMOJI

async def profile_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    db_user = get_user(user.id)
    players = get_user_players(user.id)

    total = db_user['wins'] + db_user['losses'] + db_user['draws']
    win_rate = (db_user['wins'] / total * 100) if total > 0 else 0

    rarity_count = {}
    for p in players:
        rarity_count[p['rarity']] = rarity_count.get(p['rarity'], 0) + 1

    best = max(players, key=lambda x: x['rating']) if players else None

    text = f"""
👤 *{user.first_name}'s Profile*
━━━━━━━━━━━━━━━━━━━━━
💰 *Coins:* {db_user['coins']}
🃏 *Players:* {len(players)}

⚽ *Match Record:*
🏆 Wins: {db_user['wins']}
❌ Losses: {db_user['losses']}
🤝 Draws: {db_user['draws']}
📊 Win Rate: {win_rate:.1f}%

🗂️ *Collection:*
👑 Icons: {rarity_count.get('ICON', 0)}
⭐ Gold Rare: {rarity_count.get('GOLD_RARE', 0)}
🥇 Gold: {rarity_count.get('GOLD', 0)}
🥈 Silver: {rarity_count.get('SILVER', 0)}
🥉 Bronze: {rarity_count.get('BRONZE', 0)}
"""
    if best:
        emoji = RARITY_EMOJI.get(best['rarity'], '⚽')
        text += f"\n🌟 *Best Player:* {emoji} {best['name']} ⭐{best['rating']}"

    text += "\n━━━━━━━━━━━━━━━━━━━━━"
    keyboard = [
        [InlineKeyboardButton("👥 My Squad", callback_data="team_view"),
         InlineKeyboardButton("📦 Open Packs", callback_data="pack_menu")],
        [InlineKeyboardButton("⚔️ Battle!", callback_data="battle_menu")]
    ]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
