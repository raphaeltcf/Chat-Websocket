import random
import asyncio

games = {}

async def start_game(username, websocket, db):
    if username in games:
        await websocket.send_text("🛑 Você já está jogando!")
        return

    games[username] = {"credits": 10, "bet": None, "number": None}
    await websocket.send_text("🎰 Bem-vindo ao jogo! você tem 10 creditos. Digite '/bet valor' para apostar.")

    await asyncio.sleep(60)
    await websocket.send_text("⏰ Tempo esgotado! O jogo vai começar.")
    await evalue_game()

async def place_bet(username, value, number, websocket):
    if username not in games:
        await websocket.send_text("🛑 Você não está em um jogo!")
        return

    games[username]["bet"] = value
    games[username]["number"] = number
    await websocket.send_text(f"✅ Você fez uma aposta de {value} creditos para o número {number}")

async def evaluate_game():
    if not games:
        return

    winning_number = random.randint(0, 30)
    winners = [user for user in games if games[user]["number"] == winning_number]

    if winners:
        prize = sum(games[user]["bet"] for user in winners) / len(winners)
        for user in winners:
            games[user]["credits"] += prize
            await notify_all(f"🏆 {user} venceu! Número sorteado: {winning_number}")

    games.clear()
