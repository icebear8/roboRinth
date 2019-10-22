import $ from 'jquery'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css'
import * as vis from 'vis-network'
import './main.css'

$(document).ready(function() {
    // create an array with nodes
    const nodes = new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]);

    // create an array with edges
    const edges = new vis.DataSet([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5}
    ]);

    // create a network
    const container = $('#network');

    // provide the data in the vis format
    const data = {
        nodes: nodes,
        edges: edges,
    };
    const options = {};

    // initialize your network!
    const network = new vis.Network(container[0], data, options);
});
