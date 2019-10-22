import $ from 'jquery'
import _ from 'lodash'
import * as vis from 'vis-network'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import './main.css'

let websocket = null;
let network = null;

$(document).ready(function() {
    initNetwork();
    initWebSocket();
});

function initNetwork() {
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
    network = new vis.Network(($('#network'))[0], data, options);
}

function initWebSocket() {
    websocket = new WebSocket('ws://localhost:8765');
    websocket.onmessage = function(msg) {
        const updateData = JSON.parse(msg.data);
        console.log(updateData);

        network.setData({
            nodes: getNodes(updateData),
            edges: getEdges(updateData),
        });
    };
}

function getNodes(updateData) {
    let nodes = [];
    for (const edgeData of updateData.edges) {
        for (const nodeData of [edgeData.node1, edgeData.node2]) {
            const node = {
                id: getNodeId(nodeData),
                label: getNodeId(nodeData),
                x: nodeData.x * 70,
                y: nodeData.y * 70,
            };

            if (nodeData.x === updateData.position.x && nodeData.y === updateData.position.y) {
                node.color = 'red';
            }

            nodes.push(node);
        }
    }
    return _.uniqBy(nodes, node => node.id);
}

function getEdges(updateData) {
    let edges = [];
    for (const edgeData of updateData.edges) {
        const edge = {
            from: getNodeId(edgeData.node1),
            to: getNodeId(edgeData.node2),
            color: 'black',
        };
        edges.push(edge);
    }
    return edges;
}

function getNodeId(nodeData) {
    return `${nodeData.x}:${nodeData.y}`;
}
