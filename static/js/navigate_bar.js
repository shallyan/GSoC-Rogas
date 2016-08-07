function updateConfig()
{
    var cluster_node_max_num = $('#cluster_node_max_num').val();
    var ranked_node_max_num = $('#ranked_node_max_num').val();
    var path_max_num = $('#path_max_num').val();
    var node_min_size = $('#node_min_size').val();
    var node_max_size = $('#node_max_size').val();
    var node_default_size = $('#node_default_size').val();
    var edge_min_width = $('#edge_min_width').val();
    var edge_max_width = $('#edge_max_width').val();
    var unhighlight_opacity = $('#unhighlight_opacity').val();

    if (cluster_node_max_num < 0 || ranked_node_max_num < 0 || path_max_num < 0 || node_min_size < 0 || node_max_size < 0 ||
        node_default_size < 0 || edge_min_width < 0 || edge_max_width < 0 || unhighlight_opacity < 0)
    {
        alert("Parameters can't be negative");
        return;
    }

    if (unhighlight_opacity > 1.0)
    {
        alert("UNHIGHLIGHT_OPACITY can't be larger than 1.0");
        return;
    }

    if (node_min_size >= node_max_size)
    {
        alert("NODE_MIN_SIZE must be smaller than NODE_MAX_SIZE");
        return;
    }

    if (edge_min_width >= edge_max_width)
    {
        alert("EDGE_MIN_WIDTH must be smaller than EDGE_MAX_WIDTH");
        return;
    }

    var config_obj= {'CLUSTER_NODE_MAX_NUM': cluster_node_max_num,
                     'RANK_NODE_MAX_NUM': ranked_node_max_num,
                     'PATH_MAX_NUM': path_max_num,
                     'NODE_MIN_SIZE': node_min_size,
                     'NODE_MAX_SIZE': node_max_size,
                     'NODE_DEFAULT_SIZE': node_default_size,
                     'EDGE_MIN_WIDTH': edge_min_width,
                     'EDGE_MAX_WIDTH': edge_max_width,
                     'UNHIGHLIGHT_OPACITY': unhighlight_opacity
                    };
    var config_str = JSON.stringify(config_obj);
    var args = {'config': config_str};

    $.ajax({url: '/config', data: $.param(args), dataType: 'json', type: 'POST',
        success: configSuccess, error: configError 
    });
}

function configSuccess(response)
{
    alert("Update setting successfully");
}

function configError(response)
{
    alert("Can't connect to the backend server");
}
