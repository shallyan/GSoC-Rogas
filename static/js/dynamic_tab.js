$(function () {
    var tab_index = 1;
    $('#query_add a[role="button"]').on('click', function () { 
        //insert one query at the last of query tabs
        $('ul#query_tab li:last-child').before('<li id="query' + tab_index + '"><a href="#query_content' + tab_index + '" data-toggle="tab"> <strong> Query' + tab_index + ' </strong> <button type="button" class="btn btn-warning btn-xs" onclick="removeTab(' + tab_index + ');"><span class="glyphicon glyphicon-remove"></span></button></a></li>');

        //insert one query content(the input panel) into the tab content
        $('div#query_tab_content > div:last-child').after('\
            <div class="tab-pane fade" id="query_content' + tab_index + '">\
                <div class="panel-body">\
                    <form class="form-horizontal" id="query_form' + tab_index + '" method="post" action="/query">\
                        <div class="form-group has-success">\
                            <div class="col-md-11">\
                                <textarea id="query_text' + tab_index + '" class="form-control" rows="1" placeholder="Input query here" onclick=initExpanding(' + tab_index + ')></textarea>\
                            </div>\
                            <div class="col-md-1">\
                                <button id="query_btn' + tab_index + '" type="button" onclick=runQuery(' + tab_index + ') class="btn btn-success">\
                                    <span class="glyphicon glyphicon-expand"></span>\
                                </button>\
                            </div>\
                        </div>\
                    </form>\
                </div>\
            </div>');

        tab_index += 1;
    });
});

function initExpanding(tab_index)
{
    $('#query_content' + tab_index + ' textarea').expanding();
    $('#query_content' + tab_index + ' textarea').select();
}

function removeTab(tab_index) 
{
    //remove tab from query tabs
    $('ul#query_tab > li#query' + tab_index).fadeOut(300, function () { 
        $(this).remove(); 
    });

    //remove tab content
    $('div#query_tab_content div#query_content' + tab_index).remove();

    //show first tab
    $('#query_tab a:first').tab('show') ;

    return false;
}

function prepareResult(tab_index)
{
    //set up button disabled
    $('#query_btn' + tab_index).prop('disabled', true);

    //remove result panel firstly
    if ($('#rg_result' + tab_index).length > 0) {
        $('#rg_result' + tab_index).remove();
    }

    //add loading progress
    if ($('#query_progress' + tab_index).length == 0) {
        $('#query_form' + tab_index).after('\
            <div class="progress" id="query_progress' + tab_index + '">\
              <div class="progress-bar progress-bar-striped active" role="progressbar" style="width: 0%">\
              </div>\
              loading\
            </div>');
    }

    loadingAnimation(tab_index);
}

function runQuery(tab_index) 
{
    prepareResult(tab_index);

    var query_str = $('#query_text' + tab_index).val();
    var args = {'query': query_str, 'tab_index': tab_index};

    $.ajax({url: '/query', data: $.param(args), dataType: 'json', type: 'POST',
        success: querySuccess, error: queryError
    });
}

function loadingAnimation(tab_index)
{
    if ($('#query_progress' + tab_index).length > 0) {
        $('#query_progress' + tab_index + ' .progress-bar').attr('style', 'width: 0%');

        $('#query_progress' + tab_index + ' .progress-bar').animate({
            width: "100%"
        }, 5500, function(){
            loadingAnimation(tab_index);
        });
    }
}

function querySuccess(response)
{
    var tab_index = response.tab_index;
    //remove loading progress
    $('#query_progress' + tab_index).remove();
    //enable run button
    $('#query_btn' + tab_index).prop('disabled', false);

    var result_type = response.result.type;
    var result_content = response.result.content;

    var insert_html = ''
    if (result_type != "string")
    {
        var table_content = result_content.table;
        //relation tab
        insert_html = '\
            <!-- result tab: Relations/Graphs -->\
            <div class="panel panel-info" id="rg_result' + tab_index + '">\
                <div class="panel-heading">\
                    <ul id="result_tab" class="nav nav-pills">\
                        <li class="active">\
                            <a href="#relation' + tab_index + '" data-toggle="tab">\
                                <span class="glyphicon glyphicon-th"></span> <strong> Relations </strong>\
                            </a>\
                        </li>';

        //if the type is table_graph, add graph tab
        if (result_type == "table_graph")
        {
            insert_html += '\
                        <li>\
                            <a href="#graph' + tab_index + '" data-toggle="tab">\
                                <span class="glyphicon glyphicon-picture"></span> <strong> Graphs </strong>\
                            </a>\
                        </li>';
        }

        insert_html += '\
                    </ul>\
                </div>\
                <div id=result_tab_content" class="tab-content">';

        if (result_type == "table_graph")
        {
            var graph_content = result_content.graph;
            var graph_name = graph_content.name;
            var graph_operator = graph_content.operator;
            var graph_type = graph_content.graph_type;

            if (graph_operator == "rank")
            {
                insert_html += '\
                    <div class="tab-pane fade" id="graph' + tab_index + '"> \
                    </div>';
            }
            else {
                insert_html += '\
                    <div class="tab-pane fade" id="graph' + tab_index + '"> \
                        <div>\
                            <span>Here are graphs!</span>\
                        </div>\
                        <div>\
                            <span>GraphName: ' + graph_name + '</span>\
                        </div>\
                        <div>\
                            <span>GraphType: ' + graph_type + '</span>\
                        </div>\
                        <div>\
                            <span>GraphOperator: ' + graph_operator + '</span>\
                        </div>\
                    </div>';
            }
        }
        insert_html += '\
                    <div class="tab-pane fade in active" id="relation' + tab_index + '">\
                        <div class="table-responsive" id="div_table' + tab_index + '">\
                            <table class="table table-bordered table-hover table-striped">\
                                <thead id="table_head' + tab_index + '">\
                                    <tr class="active">';

        var column_list = table_content.column_list;
        for (var col_index = 0; col_index < column_list.length; ++col_index)
            insert_html += '<th>' + column_list[col_index] + '</th>';
        insert_html += '\
                                    </tr>\
                                </thead>';

        insert_html += generateTableBodyHTML(tab_index, table_content);

        insert_html += '\
                            </table>\
                        </div> <!-- table-->';

        insert_html += generatePagerHTML(tab_index, table_content);

        insert_html += '\
                    </div> <!-- relation tab-->\
                </div>\
            </div>';
    }
    else {
        insert_html = '<div style="display: none" id="rg_result' + tab_index + '">\
                           <div class="alert alert-info" role="alert">\
                               <p>' + result_content + '</p>\
                           </div>\
                       </div>';
    }

    $('#query_form' + tab_index).after(insert_html);

    $('#rg_result' + tab_index).hide();
    $('#rg_result' + tab_index).fadeIn();

    if (result_type == "table_graph")
    {
        var graph_content = result_content.graph;
        drawGraph(tab_index, graph_content);
    }
}

function drawGraph(tab_index, graph_content)
{
    var graph_operator = graph_content.operator;

    if (graph_operator == "rank")
    {
        var graph_type = graph_content.graph_type;
        var graph_nodes = graph_content.nodes;
        var graph_edges = graph_content.edges;


        var height = 400;
        var width = $("#rg_result" + tab_index).width();

        var svg = d3.select("#graph" +  tab_index)
                    .append("svg")
                    .attr({"height": height, "width": width});

        
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
                             .range([5, 100]);

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
                            .attr("dx", 20)
                            .attr("dy", 5)
                            .text(function(d){
                                return d.value;
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

function queryError(response)
{
    console.log("ERROR:", response)
    alert("There is something wrong: can't connect to server, " + response);

    $('button').prop('disabled', false);
}

function loadingNewPage(tab_index, query_id, is_next) 
{
    //set up button disabled
    $('#query_btn' + tab_index).prop('disabled', true);

    var args = {'query_id': query_id, 'tab_index': tab_index, 'is_next': is_next};

    $.ajax({url: '/load_result', data: $.param(args), dataType: 'json', type: 'POST',
        success: queryNewPageSuccess, error: queryError
    });
}

function generateTableBodyHTML(tab_index, table_content)
{
    var row_content = table_content.row_content;
    var table_body_html = '<tbody id="table_body' + tab_index + '">';
    for (var row_index = 0; row_index < row_content.length; ++row_index)
    {
        if (row_index % 2 == 0)
            table_body_html += '<tr>';
        else
            table_body_html += '<tr class="info">';
        for (var col_index = 0; col_index < row_content[row_index].length; ++col_index)
            table_body_html += '<td>' + row_content[row_index][col_index] + '</td>';
        table_body_html += '<tr>';
    }

    table_body_html += '</tbody>';
    return table_body_html;
}

function generatePagerHTML(tab_index, table_content)
{
    pager_html = '';
    var is_begin = table_content.is_begin;
    var is_end = table_content.is_end;
    if (is_end == 0 || is_begin == 0)
    {
        pager_html += '\
                    <nav id="pager' + tab_index + '">\
                        <ul class="pager">'
            
        var query_id = table_content.query_id;
        if (is_begin == 0)
            pager_html += '\
                             <li class="previous"><a role="button" onclick="loadingNewPage(' + tab_index + ', ' + query_id + ', 0); return false" ><span>&larr;</span> Previous </a></li>';
        if (is_end == 0)
            pager_html += '\
                             <li class="next"><a role="button" onclick="loadingNewPage(' + tab_index + ', ' + query_id + ', 1); return false" > Next <span>&rarr;</span></a></li>';
        pager_html += '\
                        </ul>\
                    </nav>';
    }
    return pager_html;
}

function queryNewPageSuccess(response)
{
    var tab_index = response.tab_index;
    //enable run button
    $('#query_btn' + tab_index).prop('disabled', false);

    $('#table_body' + tab_index).remove();
    $('#pager' + tab_index).remove();

    var result_type = response.result.type;
    if (result_type != "table")
        alert("There is something wrong: invalid result type");

    var result_content = response.result.content;
    var table_content = result_content.table;

    var table_body_html = generateTableBodyHTML(tab_index, table_content);
    var pager_html = generatePagerHTML(tab_index, table_content);

    $('#table_head' + tab_index).after(table_body_html);
    $('#div_table' + tab_index).after(pager_html);

    $('#table_body' + tab_index).hide();
    $('#table_body' + tab_index).fadeIn();
}
