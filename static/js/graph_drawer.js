function drawGraph(tab_index, graph_content)
{
    var graph_type = graph_content.graph_type;
    var isDirectedGraph = (graph_type == "digraph");

    var graph_nodes = graph_content.nodes;
    var graph_edges = graph_content.edges;

    var height = 400;
    var width = $("#rg_result" + tab_index).width();
    var min_zoom = 0.1;
    var max_zoom = 2.0;
    var min_radius = 5;
    var max_radius = 200;

    var svg = d3.select("#graph" +  tab_index)
                .append("svg")
                .attr("height", height)
                .attr("width", width)
                .style("cursor","move");

    var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom]);

    //convert id to index from 0 
    var node_id_index_map = d3.map();
    for (var index = 0; index < graph_nodes.length; ++index)
        node_id_index_map.set(graph_nodes[index].id, index);

    for (var index = 0; index < graph_edges.length; ++index)
    {
        graph_edges[index].source = node_id_index_map.get(graph_edges[index].source);
        graph_edges[index].target = node_id_index_map.get(graph_edges[index].target);
    }

    var force = d3.layout.force()
                  .nodes(graph_nodes)
                  .size([width, height])
                  .links(graph_edges)	
                  .charge(-400)	
                  .linkDistance(function(edge){
                      return edge.length;
                  });
    force.start();	

    var color_scale = d3.scale.category20();

    if (isDirectedGraph)
    {
        svg.append("defs")
           .selectAll("marker")
           .data(["end"])
           .enter()
           .append("marker")
           .attr("id", String)
           .attr("viewBox", "0 0 12 12")
           .attr("markerWidth", 12)
           .attr("markerHeight", 12)
           .attr("refX", 10)
           .attr("refY", 6)
           .attr("orient", "auto")
           .style("fill", color_scale(0))
           .append("path")
           .attr("d", "M2,2 L10,6 L2,10 L6,6 L2,2");
    }

    var g = svg.append("g");
    
    var svg_edges = g.selectAll("path")
                        .data(graph_edges)
                        .enter()
                        .append("path")
                        .attr("d", function(edge){
                            return "M" + edge.source.x + "," + edge.source.y + " L" + edge.target.x + "," + edge.target.y;
                        })
                        .style("stroke", function(edge){
                            return color_scale(edge.color % 20);
                        })
                        .style("stroke-width",function(edge){
                            return edge.width;
                        })
                        .attr("marker-end","url(#end)");
    
    var linear_scale = d3.scale.linear()
                         .domain([0, 1])
                         .range([min_radius, max_radius]);

    var svg_nodes = g.selectAll("node")
                        .data(graph_nodes)
                        .enter()
                        .append("g")
                        .call(force.drag);

    var node_imgs = svg_nodes.append("circle")
                        .attr("r", function(node){
                            return linear_scale(node.size); 
                        })
                        .style("fill", function(node){
                            return color_scale(node.color % 20);
                        });

    var svg_texts = g.selectAll("text")
                        .data(graph_nodes)
                        .enter()
                        .append("text")
                        .style("fill", "black")
                        .attr("dx", function(node){
                            return linear_scale(node.size);
                        })
                        .attr("dy", 5)
                        .text(function(node){
                            return node.id;
                        });

    svg_nodes.on("mousedown", function(d){
        d3.event.stopPropagation();
    });

    zoom.on("zoom", function(){
        g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
    });

    svg.call(zoom);   

    force.on("tick", function(){
        svg_nodes.attr("transform", function(node) { return "translate(" + node.x + "," + node.y + ")"; });
        svg_texts.attr("transform", function(text) { return "translate(" + text.x + "," + text.y + ")"; });
        svg_edges.attr("d",function(edge){
            var dx = edge.target.x - edge.source.x;
            var dy = edge.target.y - edge.source.y;
            var dr = Math.sqrt(dx * dx + dy * dy);

            var offset_x = 0; 
            var offset_y = 0;
            if (dr > min_radius && isDirectedGraph)
            {
                offset_x = dx * linear_scale(edge.target.size) / dr;
                offset_y = dy * linear_scale(edge.target.size) / dr;
            }

            return "M" + edge.source.x + "," + edge.source.y + "L" + (edge.target.x - offset_x) + "," + (edge.target.y - offset_y);
        });
    });
}

