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
        const updateData = JSON.parse(msg.data);
        console.log(updateData);

        const nodeId = node => `${node.x}:${node.y}`;

        let edges = [];
        for (const edgeData of updateData.edges) {
            const edge = {
                from: nodeId(edgeData.node1),
                to: nodeId(edgeData.node2),
            };
            edges.push(edge);
        }

        let nodes = [];
        for (const edgeData of updateData.edges) {
            for (const nodeData of [edgeData.node1, edgeData.node2]) {
                const node = {
                    id: nodeId(nodeData),
                    label: nodeId(nodeData),
                    x: nodeData.x * 70,
                    y: nodeData.y * 70,
                };

                if (nodeData.x === updateData.position.x && nodeData.y === updateData.position.y) {
                    node.color = 'red';
                }

                nodes.push(node);
            }
        }
        nodes = _.uniqBy(nodes, node => node.id);

        network.setData({
            nodes: nodes,
            edges: edges,
        });
    };
});
