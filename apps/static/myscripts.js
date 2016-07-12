$('.panel-heading').click(function () {
    $(this).next().next().toggle();
});

function gg(obj) {
    var hostName = $(obj).parent().parent().find('td').eq(1).html();
    var log_path = $(obj).parent().parent().find('td').eq(2).html();
    var project = $(obj).parent().parent().find('td').eq(3).html();
    var startTime = $('input').eq(0).val();
    var endTime = $('input').eq(1).val();

    $.ajax({
        type: "POST",
        url: "http://localhost:5000/dl",
        data: JSON.stringify({"project": project, "hostName": hostName, "log_path": log_path, "startTime": startTime, "endTime": endTime}),
        contentType: "application/json;charset=utf-8",
        dataType: "json",
        success: function (data) {
        }
    })

}
