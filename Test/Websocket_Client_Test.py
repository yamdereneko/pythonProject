import asyncio
import websockets
import websockets.exceptions

async def hello():
    try:
        async with websockets.connect('ws://127.0.0.1:8765/light/off') as websocket:
            light_addr = '00-12-4b-01'
            await websocket.send(light_addr)
            recv_msg = await websocket.recv()
            print(recv_msg)
    except websockets.exceptions.ConnectionClosedError as e:
        print("connection closed error")
    except Exception as e:
        print(e)
asyncio.run(hello())

# async def hello():
#     try:
#         async with websockets.connect('wss://socket.nicemoe.cn') as websocket:
#             # light_addr = '00-12-4b-01'
#             # await websocket.send(light_addr)
#             recv_msg = await websocket.recv()
#             print(recv_msg)
#     except websockets.exceptions.ConnectionClosedError as e:
#         print("connection closed error")
#     except Exception as e:
#         print(e)
# asyncio.run(hello())