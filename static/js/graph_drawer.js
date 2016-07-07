function drawGraph(tab_index, graph_content)
{
    var graph_type = graph_content.graph_type;
    var graph_nodes = graph_content.nodes;
    var graph_edges = graph_content.edges;

    var height = 400;
    var width = $("#rg_result" + tab_index).width();

    var svg = d3.select("#graph" +  tab_index)
                .append("svg")
                .attr({"height": height, "width": width});

    //convert id to index from 0 
    var nodeIdIndexMap = d3.map();
    for (var index = 0; index < graph_nodes.length; ++index)
        nodeIdIndexMap.set(graph_nodes[index].id, index);

    for (var index = 0; index < graph_edges.length; ++index)
    {
        graph_edges[index].source = nodeIdIndexMap.get(graph_edges[index].source);
        graph_edges[index].target = nodeIdIndexMap.get(graph_edges[index].target);
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

    var svg_edges = svg.selectAll("line")
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
                         .range([5, 50]);

    var svg_nodes = svg.selectAll("circle")
                        .data(graph_nodes)
                        .enter()
                        .append("circle")
                        .attr("r",function(node){
                            return linear_scale(node.size);
                        })
                        .style("fill",function(node){
                            return color_scale(node.color % 20);
                        })
                        .call(force.drag);

    var svg_texts = svg.selectAll("text")
                        .data(graph_nodes)
                        .enter()
                        .append("text")
                        .style("fill", "black")
                        .attr("dx", 10)
                        .attr("dy", 5)
                        .text(function(node){
                            return node.id;
                        });

    force.on("tick", function(){
         svg_edges.attr("x1",function(edge){ return edge.source.x; })
                  .attr("y1",function(edge){ return edge.source.y; })
                  .attr("x2",function(edge){ return edge.target.x; })
                  .attr("y2",function(edge){ return edge.target.y; });
         
         svg_nodes.attr("cx",function(node){ return node.x; })
                  .attr("cy",function(node){ return node.y; });

         svg_texts.attr("x", function(text){ return text.x; })
                  .attr("y", function(text){ return text.y; });
    });
}

