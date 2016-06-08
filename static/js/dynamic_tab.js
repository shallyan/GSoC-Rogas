$(function () {
    var tab_index = 1;
    $('#query_tab a[href="#add_tab"]').on('click', function () { 
        //insert one query at the last of query tabs
        $('ul#query_tab li:last-child').before('<li id="query' + tab_index + '"><a href="#query_content' + tab_index + '" data-toggle="tab"> <strong> Query' + tab_index + ' </strong> <button type="button" class="btn btn-warning btn-xs" onclick="removeTab(' + tab_index + ');"><span class="glyphicon glyphicon-remove"></span></button></a></li>');

        //insert one query content(the input panel) into the tab content
        $('div#query_tab_content > div:last-child').after('<div class="tab-pane fade" id="query_content' + tab_index + '"><div class="panel-body"><form class="form-horizontal"><div class="form-group has-success"><label class="col-md-1 control-label">$</label><div class="col-md-10"><textarea class="form-control" rows="1" placeholder="Input query here" onclick=initExpanding(' + tab_index + ')></textarea></div><button class="btn btn-success" type="button"><span class="glyphicon glyphicon-expand"></span></button></div></form></div>');

        tab_index += 1;
    });
});

function initExpanding(tab_index)
{
    $('#query_content' + tab_index + ' textarea').expanding();
}

function removeTab(tab_index) {
    //remove tab from query tabs
    $('ul#query_tab > li#query' + tab_index).fadeOut(300, function () { 
        $(this).remove(); 
    });

    //remove tab content
    $('div#query_tab_content div#query_content' + tab_index).remove();

    $('#query_tab a:first').tab('show') ;

    return false;
}
