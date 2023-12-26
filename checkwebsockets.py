import asyncio
import websockets

async def test_websocket():
    async with websockets.connect("ws://localhost:8000/ws") as websocket:
        # Send a message
        await websocket.send("Hello, WebSocket!")

        # Receive and print the echoed message
        response = await websocket.recv()
        print(f"Received message: {response}")

asyncio.get_event_loop().run_until_complete(test_websocket())
