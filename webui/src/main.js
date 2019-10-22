import $ from 'jquery'
import _ from 'lodash'
import * as vis from 'vis-network'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import './main.css'

$(document).ready(function() {
    const data = {
        nodes: [],
        edges: [],
    };
    const options = {
        physics: {
            enabled: false,
        },
        interaction: {
            dragNodes: false,
        }
    };
    const container = $('#network');
    const network = new vis.Network(container[0], data, options);

    let websocket = new WebSocket('ws://localhost:8765');

    websocket.onmessage = function(msg) {
        const data = JSON.parse(msg.data);
        console.log(data);

        const nodeId = node => `${node.x}:${node.y}`;
        let new_nodes = [];
        let new_edges = [];
        for (const entry of data) {
            const edge = {
                from: nodeId(entry.node1),
                to: nodeId(entry.node2),
            };
            new_edges.push(edge);

            for (const node of [entry.node1, entry.node2]) {
                new_nodes.push({
                    id: nodeId(node),
                    label: nodeId(node),
                    x: node.x * 70,
                    y: node.y * 70,
                });
            }
        }
        new_nodes = _.uniqBy(new_nodes, node => node.id);
        network.setData({
            nodes: new_nodes,
            edges: new_edges,
        });
    };
});
