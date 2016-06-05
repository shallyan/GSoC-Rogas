$(function () {
    $('#query_tab a[href="#add_tab"]').on('click', function () { 
        //get current tab index, start from 0
        //minus - 1 because last tab is "Add New Tab"
        var tab_index = ($('ul#query_tab li').length) - 1;

        //insert one query at the last of query tabs
        $('ul#query_tab li:last-child').before('<li id="query' + tab_index + '"><a href="#query_content' + tab_index + '" data-toggle="tab"> <strong> Query' + tab_index + ' </strong> <button type="button" class="btn btn-warning btn-xs" onclick="removeTab(' + tab_index + ');"><span class="glyphicon glyphicon-remove"></span></button></a></li>');

        //insert one query content(the input panel) into the tab content
        $('div#query_tab_content > div:last-child').after('<div class="tab-pane fade" id="query_content' + tab_index + '"><div class="panel-body"><form class="form-horizontal"><div class="form-group has-success"><div class="input-group col-md-12"><div class="input-group-addon">$</div><textarea class="form-control" rows="1" placeholder="Input query'+tab_index+' here"></textarea><span class="input-group-btn"><button class="btn btn-success" type="button"><span class="glyphicon glyphicon-expand"></span></button></span></div></div></form></div>');
    });
});

function removeTab(id) {
    //remove tab from query tabs
    $('ul#query_tab > li#query' + id).fadeOut(300, function () { 
        $(this).remove(); 
    });

    //remove tab content
    $('div#query_tab_content div#query_content' + id).remove();

    //modify other tabs' id
    $('ul#query_tab > li').not('#query_add').not('#query' + id).each(function(i){ 
        var getAttr = $(this).attr('id').split('query');
        var origin_id = getAttr[1];
        $('ul#query_tab li#query' + origin_id).attr('id', 'query' + i);

        var tabContent = '<strong> Query' + i + '</strong>'; 
        if (i != 0) {
            tabContent += '<button type="button" class="btn btn-warning btn-xs" onclick="removeTab(' + i + ');"><span class="glyphicon glyphicon-remove"></span></button>';
        }
        $('ul#query_tab a[href="#query_content' + origin_id + '"]').html(tabContent).attr('href', '#query_content' + i);
        $('div#query_tab_content div#query_content' + origin_id).attr('id', 'query_content' + i);
    });

    $('#query_tab a:first').tab('show') ;

    return false;
}
