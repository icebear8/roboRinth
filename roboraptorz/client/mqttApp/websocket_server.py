import asyncio
import json
import websockets

from Map import *
from Common import *

class Edge:
    def __init__(self):
        self.node1 = Point()
        self.node2 = Point()
        self.color = LineColor.Black

def colorToHtml(color):
    if color == LineColor.Black:
        return 'black'
    elif color == LineColor.Red:
        return 'red'
    else:
        return 'yellow'

class WebSocketServer:
    def __init__(self):
        self.__message_queues = []
        self.__server = websockets.serve(self.__handle_connection, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(self.__server)

    def send_update(self, robo_map: Map, current_position: Point):
        def format_pos(position: Point):
            return {
                "x": point.x,
                "y": point.y,
            }

        def format_edge(edge: Edge):
            return {
                "node1": format_pos(edge.node1),
                "node2": format_pos(edge.node2),
                "color": colorToHtml(edge.color),
            }
        edges = []
        for node in robo_map.mapPoints:
            for dir, color in node.availableDirections:
                newPoint = node.coord.move(dir)
                edge = Edge()
                edge.node1 = node.coord
                edge.node2 = newPoint
                edge.color = color
                edges.append(edge)

        self.__send({
            "edges": [format_edge(edge) for edge in edges],
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
