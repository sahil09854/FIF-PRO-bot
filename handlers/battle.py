from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db import ensure_user, get_user, get_user_players, update_coins, update_match_result
from database.simulation import simulate_match
import random
import asyncio

battle_sessions = {}

async def battle_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    text = """
🥊 *1v1 Dream Team Battle*
━━━━━━━━━━━━━━━━━━━━━
Battle using your best squad!
Winner gets *300 coins* 🏆
    """
    keyboard = [
        [InlineKeyboardButton("⚔️ Challenge Someone", callback_data="battle_start")],
        [InlineKeyboardButton("🔗 Join Battle", callback_data="battle_join_prompt")]
    ]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

def get_best_team(user_id):
    players = get_user_players(user_id)
    if not players:
        return []
    gks = sorted([p for p in players if p['position'] == 'GK'], key=lambda x: x['rating'], reverse=True)
    outfield = sorted([p for p in players if p['position'] != 'GK'], key=lambda x: x['rating'], reverse=True)
    team = []
    if gks:
        team.append(gks[0])
    team.extend(outfield[:4])
    if not gks:
        team = sorted(players, key=lambda x: x['rating'], reverse=True)[:5]
    return team[:5]

async def battle_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    data = query.data

    if data == "battle_menu":
        text = """
🥊 *1v1 Dream Team Battle*
━━━━━━━━━━━━━━━━━━━━━
Use your best squad to battle!
Winner gets *300 coins* 🏆
        """
        keyboard = [
            [InlineKeyboardButton("⚔️ Challenge Someone", callback_data="battle_start")],
            [InlineKeyboardButton("🔗 Join Battle", callback_data="battle_join_prompt")]
        ]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "battle_start":
        my_team = get_best_team(user.id)
        if len(my_team) < 3:
            await query.edit_message_text(
                "❌ *Not enough players!*\n\nOpen packs first! 📦",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📦 Open Packs", callback_data="pack_menu")]])
            )
            return

        battle_id = str(random.randint(100000, 999999))
        battle_sessions[battle_id] = {
            "challenger_id": user.id,
            "challenger_name": user.first_name,
            "challenger_team": my_team,
            "opponent_id": None,
            "opponent_name": None,
            "opponent_team": [],
            "status": "waiting"
        }

        team_text = "\n".join([f"• {p['name']} ({p['position']}) ⭐{p['rating']}" for p in my_team])
        text = f"""
✅ *Battle Created!*
━━━━━━━━━━━━━━━━━━━━━
Battle Code: *`{battle_id}`*

*Your Team:*
{team_text}

📤 Share code with opponent!
        """
        await query.edit_message_text(text, parse_mode="Markdown")

    elif data == "battle_join_prompt":
        await query.edit_message_text("🔗 *Join Battle*\n\nType the 6-digit battle code:", parse_mode="Markdown")
        context.user_data['waiting_for_battle_code'] = True

    elif data.startswith("battle_simulate_"):
        battle_id = data.replace("battle_simulate_", "")
        await simulate_battle(query, battle_id)

async def join_battle(update: Update, context: ContextTypes.DEFAULT_TYPE, battle_id: str):
    user = update.effective_user
    ensure_user(user.id, user.username or user.first_name)
    session = battle_sessions.get(battle_id)

    if not session:
        await update.message.reply_text("❌ Battle not found!")
        return
    if session['challenger_id'] == user.id:
        await update.message.reply_text("❌ Can't join your own battle!")
        return
    if session['opponent_id']:
        await update.message.reply_text("❌ Battle already full!")
        return

    my_team = get_best_team(user.id)
    if len(my_team) < 3:
        await update.message.reply_text("❌ Not enough players! Open packs first. 📦")
        return

    session['opponent_id'] = user.id
    session['opponent_name'] = user.first_name
    session['opponent_team'] = my_team
    session['status'] = 'ready'

    team_text = "\n".join([f"• {p['name']} ({p['position']}) ⭐{p['rating']}" for p in my_team])
    text = f"✅ *Joined Battle!*\n━━━━━━━━━━━━━━━━━━━━━\n*Your Team:*\n{team_text}\n\n🔥 Let's FIGHT!"
    keyboard = [[InlineKeyboardButton("⚔️ SIMULATE!", callback_data=f"battle_simulate_{battle_id}")]]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def simulate_battle(query, battle_id):
    session = battle_sessions.get(battle_id)
    if not session:
        await query.edit_message_text("❌ Battle not found!")
        return

    await query.edit_message_text("🏟️ *Match starting...*\n⚽ Players warming up...", parse_mode="Markdown")
    await asyncio.sleep(2)

    result = simulate_match(
        session['challenger_team'],
        session['opponent_team'],
        home_name=session['challenger_name'],
        away_name=session.get('opponent_name', 'Opponent')
    )

    challenger_id = session['challenger_id']
    opponent_id = session.get('opponent_id')

    if result['winner'] == 'home':
        update_coins(challenger_id, 300)
        if opponent_id:
            update_match_result(challenger_id, opponent_id)
        result['commentary'] += f"\n\n🏆 *+300 coins* to {session['challenger_name']}!"
    elif result['winner'] == 'away' and opponent_id:
        update_coins(opponent_id, 300)
        update_match_result(opponent_id, challenger_id)
        result['commentary'] += f"\n\n🏆 *+300 coins* to {session['opponent_name']}!"
    else:
        update_coins(challenger_id, 75)
        if opponent_id:
            update_coins(opponent_id, 75)
            update_match_result(challenger_id, opponent_id, is_draw=True)
        result['commentary'] += "\n\n🤝 *+75 coins* each!"

    battle_sessions.pop(battle_id, None)
    await query.edit_message_text(result['commentary'], parse_mode="Markdown")
