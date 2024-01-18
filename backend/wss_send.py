import asyncio
import websockets
import api
async def main():
    async with websockets.serve(api.sendtoFront,"localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())