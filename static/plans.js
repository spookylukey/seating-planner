$(document).ready(function () {

    function showSolution (solutionData) {
        if (solutionData.solution != undefined) {
            var data = solutionData.solution;
            for (i in data) {
                console.log("Table:")
                var row = data[i];
                for (j in row) {
                    console.log(row[j]);
                }
                console.log("");
            }
        }
    }

    $("#find-solution").click(function() {
        var $tbl = $("#connections");
        var ht = $tbl.data('handsontable');
        var data = ht.getData();
        var connections = [];
        for (i in data) {
            var row = data[i];
            for (j in row) {
                var d = row[j];
                connections.push(d);
                connections.push(",")
            }
            connections.push("\n");
        }
        $.ajax({
            url: $SCRIPT_ROOT + "/find-solution/",
            dataType: 'json',
            type: 'POST',
            data: {
                connections: connections.join(""),
                tableSize: $('#table-size').val()
            },
            success: showSolution
        });

    });

});