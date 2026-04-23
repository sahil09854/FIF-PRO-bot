from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import ensure_user, get_user, update_coins, update_match_result
from database.players import PLAYERS, RARITY_EMOJI
from database.simulation import simulate_match
import random
import asyncio

draft_sessions = {}

async def draft_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    text = """
⚔️ *5v5 Draft Battle*
━━━━━━━━━━━━━━━━━━━━━
Pick 5 players and battle a friend!
Winner gets *200 coins* 🏆
    """
    keyboard = [
        [InlineKeyboardButton("⚔️ Start New Draft", callback_data="draft_start")],
        [InlineKeyboardButton("🔗 Join Draft", callback_data="draft_join_prompt")]
    ]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def draft_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    data = query.data

    if data == "draft_menu":
        text = """
⚔️ *5v5 Draft Battle*
━━━━━━━━━━━━━━━━━━━━━
Pick 5 players and battle!
Winner gets *200 coins* 🏆
        """
        keyboard = [
            [InlineKeyboardButton("⚔️ Start New Draft", callback_data="draft_start")],
            [InlineKeyboardButton("🔗 Join Draft", callback_data="draft_join_prompt")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "draft_start":
        draft_id = str(random.randint(100000, 999999))
        draft_sessions[draft_id] = {
            "challenger_id": user.id,
            "challenger_name": user.first_name,
            "opponent_id": None,
            "challenger_picks": [],
            "opponent_picks": [],
            "status": "waiting"
        }
        text = f"""
✅ *Draft Created!*
━━━━━━━━━━━━━━━━━━━━━
Your Draft Code: *`{draft_id}`*
Share this with your friend!
        """
        keyboard = [[InlineKeyboardButton("🎯 Pick My Players", callback_data=f"draft_pick_{draft_id}_GK")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "draft_join_prompt":
        await query.edit_message_text("🔗 *Join a Draft*\n\nType the 6-digit code your friend gave you:", parse_mode="Markdown")
        context.user_data['waiting_for_draft_code'] = True

    elif data.startswith("draft_pick_"):
        parts = data.split("_")
        draft_id = parts[2]
        position = parts[3]
        await show_player_picker(query, user, draft_id, position)

    elif data.startswith("draft_select_"):
        parts = data.split("_")
        draft_id = parts[2]
        player_name = "_".join(parts[3:])
        await select_draft_player(query, user, draft_id, player_name, context)

    elif data.startswith("draft_simulate_"):
        draft_id = data.replace("draft_simulate_", "")
        await simulate_draft_match(query, draft_id)

async def show_player_picker(query, user, draft_id, position):
    session = draft_sessions.get(draft_id)
    if not session:
        await query.edit_message_text("❌ Draft not found!")
        return

    if position == "GK":
        players = [p for p in PLAYERS if p['position'] == 'GK'][:6]
        title = "🧤 Pick your GOALKEEPER:"
    else:
        outfield = [p for p in PLAYERS if p['position'] != 'GK']
        players = random.sample(outfield, min(6, len(outfield)))
        title = f"⚽ Pick player #{position}:"

    text = f"*{title}*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
    keyboard = []
    for p in players:
        emoji = RARITY_EMOJI.get(p['rarity'], '⚽')
        text += f"{emoji} *{p['name']}* — {p['position']} | ⭐{p['rating']}\n"
        keyboard.append([InlineKeyboardButton(
            f"{emoji} {p['name']} ({p['rating']})",
            callback_data=f"draft_select_{draft_id}_{p['name']}"
        )])

    await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def select_draft_player(query, user, draft_id, player_name, context):
    session = draft_sessions.get(draft_id)
    if not session:
        await query.edit_message_text("❌ Draft not found!")
        return

    is_challenger = session['challenger_id'] == user.id
    picks_key = 'challenger_picks' if is_challenger else 'opponent_picks'
    player = next((p for p in PLAYERS if p['name'] == player_name), None)
    if not player:
        await query.edit_message_text("❌ Player not found!")
        return

    session[picks_key].append(player)
    picks = session[picks_key]

    if len(picks) < 5:
        next_pos = str(len(picks) + 1)
        text = f"✅ *{player['name']}* selected!\n\nYour picks:\n"
        for p in picks:
            text += f"• {p['name']} ({p['position']}) ⭐{p['rating']}\n"
        text += f"\n🎯 Pick player #{len(picks) + 1}!"
        keyboard = [[InlineKeyboardButton("➡️ Next Player", callback_data=f"draft_pick_{draft_id}_{next_pos}")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        text = f"✅ *All 5 picked!*\n\nYour team:\n"
        for p in picks:
            emoji = RARITY_EMOJI.get(p['rarity'], '⚽')
            text += f"{emoji} {p['name']} ({p['position']}) ⭐{p['rating']}\n"

        if len(session['challenger_picks']) == 5 and len(session['opponent_picks']) == 5:
            text += "\n\n🔥 Both ready! BATTLE!"
            keyboard = [[InlineKeyboardButton("⚔️ SIMULATE!", callback_data=f"draft_simulate_{draft_id}")]]
        elif is_challenger:
            text += f"\n\n⏳ Waiting for opponent...\nCode: *{draft_id}*"
            keyboard = []
        else:
            text += "\n\n⏳ Waiting for challenger..."
            keyboard = []

        await query.edit_message_text(text, parse_mode="Markdown",
                                       reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None)

async def simulate_draft_match(query, draft_id):
    session = draft_sessions.get(draft_id)
    if not session:
        await query.edit_message_text("❌ Draft not found!")
        return

    await query.edit_message_text("⚽ *Match starting...*\n🎺 Players walking out...", parse_mode="Markdown")
    await asyncio.sleep(2)

    result = simulate_match(
        session['challenger_picks'],
        session['opponent_picks'],
        home_name=session.get('challenger_name', 'Challenger'),
        away_name=session.get('opponent_name', 'Opponent')
    )

    challenger_id = session['challenger_id']
    opponent_id = session.get('opponent_id')

    if result['winner'] == 'home':
        update_coins(challenger_id, 200)
        if opponent_id:
            update_match_result(challenger_id, opponent_id)
        result['commentary'] += "\n\n🏆 *+200 coins* to winner!"
    elif result['winner'] == 'away' and opponent_id:
        update_coins(opponent_id, 200)
        update_match_result(opponent_id, challenger_id)
        result['commentary'] += "\n\n🏆 *+200 coins* to winner!"
    else:
        update_coins(challenger_id, 50)
        if opponent_id:
            update_coins(opponent_id, 50)
            update_match_result(challenger_id, opponent_id, is_draw=True)
        result['commentary'] += "\n\n🤝 *+50 coins* each!"

    draft_sessions.pop(draft_id, None)
    await query.edit_message_text(result['commentary'], parse_mode="Markdown")
