$(document).ready(function () {

    function addRow($tbl, text) {
        $row = $("<tr><td></td></tr>").find("td").text(text).end();
        $tbl.find("tbody").append($row);
    }

    function finishedLoading () {
        $("#loading").hide();
    }

    function showSolution (solutionData) {
        finishedLoading();

        if (solutionData.solution != undefined) {
            var data = solutionData.solution;
            var $tbl = $("<table class='plan'><thead><tr><th>Plan</th></tr></thead><tbody></tbody><tfoot><tr><td><a class='remove-plan' href='#'>Remove</a></td></tr></tfoot></table>");
            for (i in data) {
                var row = data[i];
                for (j in row) {
                    addRow($tbl, row[j]);
                }
                if (i < data.length - 1) {
                    addRow($tbl, "-");
                }
            }
            $("#plans").append($("<td></td>").append($tbl));
        }
    }

    $("#find-solution").click(function() {
        if (connectionsMatrix == undefined) {
            return;
        }

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

        $("#loading").show();
        $.ajax({
            url: $SCRIPT_ROOT + "/find-solution/",
            dataType: 'json',
            type: 'POST',
            data: {
                connections: getRawConnectionsData(),
                tableSize: tableSize
            },
            success: showSolution,
            error: finishedLoading
        });

    });

    $("#plans").on("click", ".remove-plan", function (ev) {
        ev.preventDefault();
        $(ev.target).closest("table").remove();
    });

});
