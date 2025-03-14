import asyncio
import websockets

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8765
clients = set()

async def handle_client(websocket, path=None):  # `path` devient optionnel
    """Gère la connexion avec un client"""
    clients.add(websocket)
    print(f"✅ Nouveau client connecté. Total clients : {len(clients)}")

    try:
        async for message in websocket:
            print(f"📩 Message reçu : {message}")

            # Envoie la commande à tous les clients connectés
            for client in clients:
                if client != websocket:
                    await client.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("❌ Client déconnecté")

    finally:
        clients.remove(websocket)
        print(f"🗑️ Client supprimé. Clients restants : {len(clients)}")

async def start_server():
    """Lance le serveur WebSocket"""
    async with websockets.serve(handle_client, SERVER_IP, SERVER_PORT) as server:
        print(f"🚀 Serveur WebSocket lancé sur ws://{SERVER_IP}:{SERVER_PORT}")
        await asyncio.Future()  # Garde le serveur actif

asyncio.run(start_server())