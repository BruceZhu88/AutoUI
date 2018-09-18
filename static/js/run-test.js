
$(document).ready(function(){

    $.ajax({url: 'run_test/load_case', type: 'GET', dataType: 'json'})
    .done(function(data){
        if (data.length == 0){return;}
        var files_name = data['files_name'];
        $('#select_case').empty();
        for (d in files_name) {
            $option = $( "<option />");
            $option.text(files_name[d]);
            $option.attr({"id": files_name[d], "style": "cursor:pointer; border-bottom: gray dashed thin;"});
            //$li.attr({"id":i,"style":"list-style-type:none"});
            $('#select_case').append($option);
        }
    });

    $.ajax({url: 'run_test/get_status', type: 'GET', dataType: 'json'})
    .done(function(data){
        if (data['status'] == ''){return;}
        $('.running_status_tr').empty();
        $tbody = $('#running_status_tbody');
        for (i in data['status']) {
            $tr = $("<tr class=\"running_status_tr\"></tr>");
            var row = data['status'][i];
            for (j in row) {
                if (j == 5 && row[j] != '') {
                    $td = $("<td><div class=\"cell\"><a href=\"report/"+row[j]+"\" target=\"_blank\">点击查看</a></div></td>");
                }
                else {
                    $td = $("<td><div class=\"cell\">"+row[j]+"</div></td>");
                }
                $tr.append($td);

            }
            $tbody.append($tr);
        }
    });

    $("#btn_run").click(function(event){
        var selectCase = $("#select_case").find("option:selected").text();
    	if (selectCase == ""){return;}
        $.ajax({url: "run_test/run_case", type: "POST", dataType: "json", data: {'case': selectCase}})
            .done(function(data){
                alert('开始执行测试');
                location.reload();
        	});
    });
});


