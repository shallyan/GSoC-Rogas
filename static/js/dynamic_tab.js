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
                                <button type="button" onclick=runQuery(' + tab_index + ') class="btn btn-success"><span class="glyphicon glyphicon-expand"></span>\
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

function removeTab(tab_index) {
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

function runQuery(tab_index) {
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

    loading(tab_index);

    var query_str = $('#query_text' + tab_index).val();
    var args = {'query': query_str, 'tab_index': tab_index};

    $.ajax({url: '/query', data: $.param(args), dataType: 'json', type: 'POST',
        success: querySuccess, error: queryError
    });
}

function loading(tab_index)
{
    if ($('#query_progress' + tab_index).length > 0) {
        $('#query_progress' + tab_index + ' .progress-bar').attr('style', 'width: 0%');

        $('#query_progress' + tab_index + ' .progress-bar').animate({
            width: "100%"
        }, 5500, function(){
            loading(tab_index);
        });
    }
}

function querySuccess(response)
{
    var tab_index = response.tab_index;
    //remove loading progress
    $('#query_progress' + tab_index).remove();

    var result_type = response.result.type;
    var result_content = response.result.content;

    var insert_html = ''
    if (result_type == "table")
    {
        insert_html = '\
            <!-- result tab: Relations/Graphs -->\
            <div class="panel panel-info" style="display: none" id="rg_result' + tab_index + '">\
                <div class="panel-heading">\
                    <ul id="result_tab" class="nav nav-pills">\
                        <li class="active">\
                            <a href="#relation' + tab_index + '" data-toggle="tab">\
                                <span class="glyphicon glyphicon-th"></span> <strong> Relations </strong>\
                            </a>\
                        </li>\
                        <li>\
                            <a href="#graph' + tab_index + '" data-toggle="tab">\
                                <span class="glyphicon glyphicon-picture"></span> <strong> Graphs </strong>\
                            </a>\
                        </li>\
                    </ul>\
                </div>\
                <div id=result_tab_content" class="tab-content">\
                    <div class="tab-pane fade" id="graph' + tab_index + '"> \
                        <span>Here are graphs!</span>\
                    </div>\
                    <div class="tab-pane fade in active" id="relation' + tab_index + '">\
                        <div class="table-responsive">\
                            <table class="table table-bordered table-hover table-striped">\
                                <thead>\
                                    <tr class="active">';

                var column_list = result_content.column_list;
                for (var col_index = 0; col_index < column_list.length; ++col_index)
                    insert_html += '<th>' + column_list[col_index] + '</th>';
                insert_html += '\
                                    </tr>\
                                </thead>\
                                <tbody>';
                var row_content = result_content.row_content;
                for (var row_index = 0; row_index < row_content.length; ++row_index)
                {
                    insert_html += '<tr>';
                    for (var col_index = 0; col_index < row_content[row_index].length; ++col_index)
                        insert_html += '<td>' + row_content[row_index][col_index] + '</td>';
                    insert_html += '<tr>';
                }
                insert_html += '</tbody>\
                            </table>\
                        </div> <!-- table-->\
                    </div> <!-- relation tab-->\
                </div>\
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
    $('#rg_result' + tab_index).fadeIn();
}

function queryError(response)
{
    console.log("ERROR:", response)
    alert("There is something wrong: can't connect to server" + response);
}
