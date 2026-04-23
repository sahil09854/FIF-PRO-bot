from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import ensure_user, get_user, update_coins, add_player_to_user
from database.players import PACK_TYPES, get_player_by_rarity, RARITY_EMOJI
import asyncio

async def open_pack_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    db_user = get_user(user.id)
    text = f"""
📦 *Pack Store*
━━━━━━━━━━━━━━━━━━━━━
💰 Your coins: *{db_user['coins']}*

🥉 *Bronze Pack* — 100 coins
🥈 *Silver Pack* — 250 coins
🥇 *Gold Pack* — 500 coins
💎 *Elite Pack* — 1000 coins
━━━━━━━━━━━━━━━━━━━━━
    """
    keyboard = [
        [InlineKeyboardButton("🥉 Bronze — 100", callback_data="pack_open_bronze"),
         InlineKeyboardButton("🥈 Silver — 250", callback_data="pack_open_silver")],
        [InlineKeyboardButton("🥇 Gold — 500", callback_data="pack_open_gold"),
         InlineKeyboardButton("💎 Elite — 1000", callback_data="pack_open_elite")]
    ]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def pack_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    data = query.data

    if data == "pack_menu":
        db_user = get_user(user.id)
        text = f"""
📦 *Pack Store*
━━━━━━━━━━━━━━━━━━━━━
💰 Your coins: *{db_user['coins']}*

🥉 *Bronze Pack* — 100 coins
🥈 *Silver Pack* — 250 coins
🥇 *Gold Pack* — 500 coins
💎 *Elite Pack* — 1000 coins
━━━━━━━━━━━━━━━━━━━━━
        """
        keyboard = [
            [InlineKeyboardButton("🥉 Bronze — 100", callback_data="pack_open_bronze"),
             InlineKeyboardButton("🥈 Silver — 250", callback_data="pack_open_silver")],
            [InlineKeyboardButton("🥇 Gold — 500", callback_data="pack_open_gold"),
             InlineKeyboardButton("💎 Elite — 1000", callback_data="pack_open_elite")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("pack_open_"):
        pack_type = data.replace("pack_open_", "")
        await open_pack(query, user, pack_type)

async def open_pack(query, user, pack_type):
    pack = PACK_TYPES.get(pack_type)
    if not pack:
        await query.edit_message_text("❌ Invalid pack type.")
        return

    db_user = get_user(user.id)
    if db_user['coins'] < pack['cost']:
        await query.edit_message_text(
            f"❌ Not enough coins!\nYou need *{pack['cost']}* but have *{db_user['coins']}*.",
            parse_mode="Markdown"
        )
        return

    update_coins(user.id, -pack['cost'])
    await query.edit_message_text(f"🎁 Opening {pack['name']}...\n✨ *Shuffling players...*", parse_mode="Markdown")
    await asyncio.sleep(1.5)

    pulled_players = []
    for rarity in pack['rarities']:
        player = get_player_by_rarity(rarity)
        pulled_players.append(player)
        add_player_to_user(user.id, player)

    result = f"🎉 *{pack['name']} Opened!*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    for p in pulled_players:
        emoji = RARITY_EMOJI.get(p['rarity'], '⚽')
        result += f"{emoji} *{p['name']}* — {p['position']} | ⭐{p['rating']}\n"
        result += f"   ⚡{p['pace']} 🎯{p['shooting']} 🎨{p['dribbling']} 💪{p['physical']}\n\n"

    db_user_after = get_user(user.id)
    result += f"━━━━━━━━━━━━━━━━━━━━━\n💰 Coins left: *{db_user_after['coins']}*"

    keyboard = [
        [InlineKeyboardButton("📦 Open Another", callback_data="pack_menu"),
         InlineKeyboardButton("👥 My Team", callback_data="team_view")]
    ]
    await query.edit_message_text(result, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
