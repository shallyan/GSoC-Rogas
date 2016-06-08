$(function () {
    var info_types = new Array();
    info_types[0] = "relation";
    info_types[1] = "graph";

    for (i = 0;i < info_types.length; i++)
    {
        $('#database_' + info_types[i]).collapse('show');

        $('#label_' + info_types[i] + '_panel button#add_' + info_types[i] + '_label').on('click', '', info_types[i], addLabel);
    }
});

function addLabel(event)
{
    var info_type = event.data;
    var table_name = $('input#' + info_type + '_input').val();

    if (table_name.length == 0)
    {
        $('#label_' + info_type + '_panel hr#' + info_type + '_sep_line').after('<div id="' + info_type + '_message" class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert"> &times;</span></button><strong>Warning!</strong> Empty input! </div>');
    }
    else
    {
        $('#' + info_type + '_message').remove(); 

        $('#label_' + info_type + '_panel hr#' + info_type + '_sep_line').before('<button type="button" class="btn btn-default btn-xs" > ' + table_name + ' <a onclick="removeLabel(this);" href="#label"> <span class="glyphicon glyphicon-remove-sign"></span></a>');
    }
}

function removeLabel(label) {
    label.parentNode.remove();
    return false;
}
