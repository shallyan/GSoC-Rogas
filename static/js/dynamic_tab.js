$(function () {
    $('#query_tab a[href="#add_tab"]').on('click', function () { 
        var tab_index = ($('ul#query_tab li').length) - 1;

        $('ul#query_tab li:last-child').before('<li id="query' + tab_index + '"><a href="#query_content' + tab_index + '" data-toggle="tab"> <strong> Query' + tab_index + ' </strong> <button type="button" class="btn btn-warning btn-xs" onclick="removeTab(' + tab_index + ');"><span class="glyphicon glyphicon-remove"></span></button></a></li>');

        $('div#query_tab_content > div:last-child').after('<div class="tab-pane fade" id="query_content' + tab_index + '"><div class="panel-body"><form class="form-horizontal"><div class="form-group has-success"><div class="input-group col-md-12"><div class="input-group-addon">$</div><textarea class="form-control" rows="1" placeholder="Input query here"></textarea><span class="input-group-btn"><button class="btn btn-success" type="button"><span class="glyphicon glyphicon-expand"></span></button></span></div></div></form></div>');
    });
});

function removeTab(id) {
    $('ul#query_tab > li#query' + id).fadeOut(300, function () { 
        $(this).remove(); 
    });

    $('div#query_tab_content div#query_content' + id).remove();

    $('ul#query_tab > li').not('#query_add').not('#query' + id).each(function(i){ 
        var getAttr = $(this).attr('id').split('query');
        $('ul#query_tab li#query' + getAttr[1]).attr('id', 'query' + i); 

        $('div#query_tab_content div#query_content' + getAttr[1]).attr('id', 'query_content' + i);
    });

    return false;
}
