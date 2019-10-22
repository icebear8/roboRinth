import asyncio
import json
import websockets

from graphmap import GraphMap, Edge
from position import Position


class WebSocketServer:
    def __init__(self):
        self.__message_queues = []
        self.__server = websockets.serve(self.__handle_connection, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(self.__server)

    def send_update(self, robo_map: GraphMap, current_position: Position):
        def format_pos(position: Position):
            return {
                "x": position.x,
                "y": position.y,
            }

        def format_edge(edge: Edge):
            return {
                "node1": format_pos(edge.node1.position),
                "node2": format_pos(edge.node2.position),
                "color": edge.color.to_html(),
            }

        self.__send({
            "edges": [format_edge(edge) for edge in robo_map.get_all_edges()],
            "position": format_pos(current_position),
        })

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
