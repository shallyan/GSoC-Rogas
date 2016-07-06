function drawGraph(tab_index, graph_content)
{
    var graph_operator = graph_content.operator;
    var graph_type = graph_content.graph_type;
    var graph_nodes = graph_content.nodes;
    var graph_edges = graph_content.edges;

    if (graph_operator == "rank"){ 

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
                  .linkDistance(50)
                  .charge(-400);	

    force.start();	

    var svg_edges = svg.selectAll("line")
                        .data(graph_edges)
                        .enter()
                        .append("line")
                        .style("stroke","#ccc")
                        .style("stroke-width",1);
    
    var color = d3.scale.category20();
            
    var linear_scale = d3.scale.linear()
                         .domain([0, 1])
                         .range([5, 200]);

    var svg_nodes = svg.selectAll("circle")
                        .data(graph_nodes)
                        .enter()
                        .append("circle")
                        .attr("r",function(d){
                            return linear_scale(d.value);
                        })
                        .style("fill",function(d,i){
                            return color(i);
                        })
                        .call(force.drag);

    var svg_texts = svg.selectAll("text")
                        .data(graph_nodes)
                        .enter()
                        .append("text")
                        .style("fill", "black")
                        .attr("dx", 10)
                        .attr("dy", 5)
                        .text(function(d){
                            return d.id;
                        });

    force.on("tick", function(){
         svg_edges.attr("x1",function(d){ return d.source.x; })
                  .attr("y1",function(d){ return d.source.y; })
                  .attr("x2",function(d){ return d.target.x; })
                  .attr("y2",function(d){ return d.target.y; });
         
         svg_nodes.attr("cx",function(d){ return d.x; })
                  .attr("cy",function(d){ return d.y; });

         svg_texts.attr("x", function(d){ return d.x; })
                  .attr("y", function(d){ return d.y; });
    });
    }
}

