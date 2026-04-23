import random

COMMENTARY_EVENTS = {
    "goal_home": [
        "⚽ GOAAAAL! {player} smashes it into the net! The crowd goes WILD!",
        "🔥 {player} with a STUNNING finish! What a goal!",
        "💥 INCREDIBLE! {player} scores from distance! The keeper had no chance!",
        "🌪️ {player} dribbles past THREE defenders and slots it home!",
        "⚡ LIGHTNING FAST counter attack ends with {player} tapping it in!",
        "🎯 Corner kick — {player} rises HIGHEST and heads it in!",
        "👑 WORLD CLASS finish from {player}! Unstoppable!",
    ],
    "goal_away": [
        "⚽ GOAAAAL for the away side! {player} levels it up!",
        "😱 {player} sneaks in at the back post! Easy finish!",
        "💣 {player} hits it first time — THUNDERBOLT into the top corner!",
        "🔄 Quick throw-in, quick pass, {player} finishes coolly!",
        "🎪 What a team move! {player} is there to tap home!",
    ],
    "miss": [
        "😬 {player} blazes it OVER the bar! What a miss!",
        "🙈 {player} hits the post! So close!",
        "😤 Great save! The keeper tips {player}'s shot around the post!",
        "🤦 {player} one-on-one with the keeper... and shoots STRAIGHT at him!",
        "😮 VAR check... no goal. {player} was offside by a WHISKER!",
    ],
    "foul": [
        "🟨 Yellow card! Reckless tackle in midfield.",
        "😡 Heated argument between the players! Referee steps in!",
        "🟥 RED CARD! That was a terrible challenge!",
        "🩹 Player down injured... physio rushes on.",
    ],
    "save": [
        "🧤 WHAT A SAVE! The goalkeeper denies a certain goal!",
        "🧱 The keeper stands TALL! Brilliant stop!",
        "🦅 Goalkeeper off his line quickly — smothers the chance!",
    ]
}

MINUTE_EVENTS = [15, 23, 34, 38, 45, 52, 61, 68, 74, 82, 88, 90]

def get_random_player_name(team_players):
    if team_players:
        return random.choice(team_players)['name']
    return "Unknown Player"

def simulate_match(home_team_players, away_team_players, home_name="Home", away_name="Away"):
    home_strength = sum(p['rating'] for p in home_team_players) / len(home_team_players) if home_team_players else 70
    away_strength = sum(p['rating'] for p in away_team_players) / len(away_team_players) if away_team_players else 70

    total_strength = home_strength + away_strength
    home_prob = min(0.75, (home_strength / total_strength) * 1.05)
    away_prob = 1 - home_prob

    home_score = 0
    away_score = 0
    commentary = []

    commentary.append(f"🏟️ *KICK OFF!* {home_name} vs {away_name}")
    commentary.append(f"📊 Strengths — {home_name}: *{home_strength:.1f}* | {away_name}: *{away_strength:.1f}*\n")

    for minute in MINUTE_EVENTS:
        event_roll = random.random()

        if event_roll < 0.35:
            if random.random() < (home_prob * 0.7 + 0.15):
                home_score += 1
                player = get_random_player_name([p for p in home_team_players if p['position'] != 'GK'])
                msg = random.choice(COMMENTARY_EVENTS["goal_home"]).format(player=player)
                commentary.append(f"⏱️ *{minute}'* — {msg}")
                commentary.append(f"📊 *{home_name} {home_score} — {away_score} {away_name}*\n")
            else:
                player = get_random_player_name([p for p in home_team_players if p['position'] != 'GK'])
                msg = random.choice(COMMENTARY_EVENTS["miss"]).format(player=player)
                commentary.append(f"⏱️ *{minute}'* — {msg}")

        elif event_roll < 0.65:
            if random.random() < (away_prob * 0.7 + 0.15):
                away_score += 1
                player = get_random_player_name([p for p in away_team_players if p['position'] != 'GK'])
                msg = random.choice(COMMENTARY_EVENTS["goal_away"]).format(player=player)
                commentary.append(f"⏱️ *{minute}'* — {msg}")
                commentary.append(f"📊 *{home_name} {home_score} — {away_score} {away_name}*\n")
            else:
                player = get_random_player_name([p for p in away_team_players if p['position'] != 'GK'])
                msg = random.choice(COMMENTARY_EVENTS["miss"]).format(player=player)
                commentary.append(f"⏱️ *{minute}'* — {msg}")

        elif event_roll < 0.75:
            commentary.append(f"⏱️ *{minute}'* — {random.choice(COMMENTARY_EVENTS['save'])}")
        else:
            commentary.append(f"⏱️ *{minute}'* — {random.choice(COMMENTARY_EVENTS['foul'])}")

        if minute == 45:
            commentary.append(f"\n🔔 *HALF TIME!* {home_name} {home_score} — {away_score} {away_name}\n")

    commentary.append(f"\n🔔 *FULL TIME!*")
    commentary.append(f"🏆 *{home_name} {home_score} — {away_score} {away_name}*")

    if home_score > away_score:
        winner = "home"
        commentary.append(f"\n🎉 *{home_name} WINS!*")
    elif away_score > home_score:
        winner = "away"
        commentary.append(f"\n🎉 *{away_name} WINS!*")
    else:
        winner = "draw"
        commentary.append(f"\n🤝 *IT'S A DRAW!*")

    return {"home_score": home_score, "away_score": away_score, "winner": winner, "commentary": "\n".join(commentary)}
