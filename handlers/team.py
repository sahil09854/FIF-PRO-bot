from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import ensure_user, get_user_players
from database.players import RARITY_EMOJI

async def team_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await show_team_message(update.message, user)

async def show_team_message(message, user):
    players = get_user_players(user.id)
    if not players:
        text = "👥 *My Squad*\n━━━━━━━━━━━━━━━━━━━━━\nNo players yet!\n\nOpen packs to get started! 📦"
        keyboard = [[InlineKeyboardButton("📦 Open Packs", callback_data="pack_menu")]]
        await message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    players_sorted = sorted(players, key=lambda x: x['rating'], reverse=True)
    text = f"👥 *Your Squad* ({len(players)} players)\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    pos_emoji = {'GK': '🧤', 'DEF': '🛡️', 'MID': '⚙️', 'FWD': '⚡'}

    for pos in ['GK', 'DEF', 'MID', 'FWD']:
        pos_players = [p for p in players_sorted if p['position'] == pos]
        if pos_players:
            text += f"*{pos_emoji[pos]} {pos}:*\n"
            for p in pos_players[:4]:
                emoji = RARITY_EMOJI.get(p['rarity'], '⚽')
                text += f"  {emoji} {p['name']} ⭐{p['rating']}\n"
            text += "\n"

    avg = sum(p['rating'] for p in players_sorted) / len(players_sorted)
    text += f"━━━━━━━━━━━━━━━━━━━━━\n📊 *Avg Rating:* {avg:.1f}"
    keyboard = [
        [InlineKeyboardButton("📦 Open Packs", callback_data="pack_menu"),
         InlineKeyboardButton("🥊 Battle!", callback_data="battle_menu")]
    ]
    await message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def team_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    data = query.data

    if data == "team_view":
        players = get_user_players(user.id)
        if not players:
            text = "👥 *My Squad*\n━━━━━━━━━━━━━━━━━━━━━\nNo players yet!\n\nOpen packs! 📦"
            keyboard = [[InlineKeyboardButton("📦 Open Packs", callback_data="pack_menu")]]
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
            return

        players_sorted = sorted(players, key=lambda x: x['rating'], reverse=True)
        text = f"👥 *Your Squad* ({len(players)} players)\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        pos_emoji = {'GK': '🧤', 'DEF': '🛡️', 'MID': '⚙️', 'FWD': '⚡'}

        for pos in ['GK', 'DEF', 'MID', 'FWD']:
            pos_players = [p for p in players_sorted if p['position'] == pos]
            if pos_players:
                text += f"*{pos_emoji[pos]} {pos}:*\n"
                for p in pos_players[:4]:
                    emoji = RARITY_EMOJI.get(p['rarity'], '⚽')
                    text += f"  {emoji} {p['name']} ⭐{p['rating']}\n"
                text += "\n"

        keyboard = [
            [InlineKeyboardButton("📦 Open Packs", callback_data="pack_menu"),
             InlineKeyboardButton("🥊 Battle!", callback_data="battle_menu")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "team_full":
        players = get_user_players(user.id)
        players_sorted = sorted(players, key=lambda x: x['rating'], reverse=True)
        text = f"📋 *Full Squad*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
        for p in players_sorted:
            emoji = RARITY_EMOJI.get(p['rarity'], '⚽')
            text += f"{emoji} *{p['name']}* [{p['position']}] ⭐{p['rating']}\n"
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="team_view")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
