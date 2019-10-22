import asyncio
import json
import websockets

from map import Map, Edge


class WebSocketServer:
    def __init__(self):
        self.__message_queues = []
        self.__server = websockets.serve(self.__handle_connection, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(self.__server)

    def send_update(self, robo_map: Map):
        def format_entry(entry: Edge):
            return {
                "node1": {
                    "x": entry.node1.position.x,
                    "y": entry.node1.position.y,
                },
                "node2": {
                    "x": entry.node2.position.x,
                    "y": entry.node2.position.y,
                }
            }

        self.__send([format_entry(entry) for entry in robo_map.get_all_edges()])

    def __send(self, message):
        async def do_send():
            for queue in self.__message_queues:
                await queue.put(message)
        asyncio.get_event_loop().create_task(do_send())

    async def __handle_connection(self, websocket: websockets.WebSocketServerProtocol, path: str):
        queue = asyncio.Queue()
        self.__message_queues.append(queue)

        try:
            while True:
                message = await queue.get()
                await websocket.send(json.dumps(message))
        except websockets.ConnectionClosed:
            pass
        finally:
            self.__message_queues.remove(queue)
