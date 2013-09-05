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
        var tableSize = $('#table-size').val();
        if (! tableSize.match(/^\d+$/)) {
            alert("Please enter an integer for table size");
            return;
        }
        tableSize = parseInt(tableSize, 10);
        var nameCount = connectionsMatrix.getData().length - 1;
        if (tableSize >= nameCount) {
            alert("Tables must be smaller than the number of people");
            return;
        }

        $.ajax({
            url: $SCRIPT_ROOT + "/find-solution/",
            dataType: 'json',
            type: 'POST',
            data: {
                connections: getRawConnectionsData(),
                tableSize: tableSize
            },
            success: showSolution
        });

    });

});
