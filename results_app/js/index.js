$('#users-table').on('click-row.bs.table', function (row, $element, field) {
    let user_id = $element['user_id'];
    $.ajax({
        type: "GET",
        url: "/api/answers/" + user_id,
        dataType: "json",
        success: function (data) {
            $('#answers-table').bootstrapTable({
                data: data,
            });
            $('#answers-table').bootstrapTable('load', data);
        }
    })
});