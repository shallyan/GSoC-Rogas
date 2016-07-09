function drawGraph(tab_index, graph_content)
{
    var graph_type = graph_content.graph_type;
    var graph_nodes = graph_content.nodes;
    var graph_edges = graph_content.edges;

    var height = 400;
    var width = $("#rg_result" + tab_index).width();
    var min_zoom = 0.1;
    var max_zoom = 2.0;

    var svg = d3.select("#graph" +  tab_index)
                .append("svg")
                .attr({"height": height, "width": width});
    var zoom = d3.behavior.zoom().scaleExtent([min_zoom,max_zoom])
    var g = svg.append("g");
    svg.style("cursor","move");

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

    var svg_edges = g.selectAll("line")
                        .data(graph_edges)
                        .enter()
                        .append("line")
                        .style("stroke", function(edge){
                            return color_scale(edge.color % 20);
                        })
                        .style("stroke-width",function(edge){
                            return edge.width;
                        });
    
            
    var linear_scale = d3.scale.linear()
                         .domain([0, 1])
                         .range([5, 200]);

    var svg_nodes = g.selectAll("node")
                        .data(graph_nodes)
                        .enter()
                        .append("g")
                        .call(force.drag);

    var node_imgs = svg_nodes.append("path")
                        .attr("d", d3.svg.symbol()
                            .size(function(node){
                                return Math.PI*Math.pow(linear_scale(node.size), 2); 
                            })
                            .type('circle'))
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
    svg.attr({"height": height, "width": width});

    force.on("tick", function(){
        svg_nodes.attr("transform", function(node) { return "translate(" + node.x + "," + node.y + ")"; });
        svg_texts.attr("transform", function(node) { return "translate(" + node.x + "," + node.y + ")"; });

         svg_edges.attr("x1",function(edge){ return edge.source.x; })
                  .attr("y1",function(edge){ return edge.source.y; })
                  .attr("x2",function(edge){ return edge.target.x; })
                  .attr("y2",function(edge){ return edge.target.y; });
         
         svg_nodes.attr("cx",function(node){ return node.x; })
                  .attr("cy",function(node){ return node.y; });
    });
}

