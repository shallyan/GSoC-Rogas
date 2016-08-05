function updateConfig()
{
    var configObj= {'CLUSTER_NODE_MAX_NUM': 20};
    var config_str = JSON.stringify(configObj);
    var args = {'config': config_str};

    $.ajax({url: '/config', data: $.param(args), dataType: 'json', type: 'POST',
        success: configSuccess, error: configSuccess 
    });
}

function configSuccess()
{
}
