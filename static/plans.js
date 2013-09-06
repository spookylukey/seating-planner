$(document).ready(function () {

    function addRow($tbl, item1, item2) {
        $row = $("<tr><td></td><td><td></tr>")
            .find("td:first-child").text(item1).end()
            .find("td:nth-child(2)").text(item2).end();
        $tbl.find("tbody").append($row);
    }

    function finishedLoading () {
        $("#loading").hide();
    }

    function showSolution (solutionData) {
        finishedLoading();

        if (solutionData.solution != undefined) {
            var data = solutionData.solution;
            var $tbl = $("<table class='plan'><thead><tr><th colspan='2'>Plan</th></tr></thead><tbody></tbody><tfoot><tr><td colspan='2'><a class='remove-plan' href='#'>Remove</a> <a class='save-plan' href='#'>Download</a></td></tr></tfoot></table>");
            for (i in data) {
                var row = data[i];
                for (j in row) {
                    var person = row[j];
                    addRow($tbl, person.name, person.friends);
                }
                if (i < data.length - 1) {
                    addRow($tbl, "-", "");
                }
            }
            $("#plans").append($("<td></td>").append($tbl));
        } else if (solutionData.error != undefined) {
            alert(solutionData.error);
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

        var tableCount = $('#table-count').val();
        if (! tableCount.match(/^\d+$/)) {
            alert("Please enter an integer for number of tables");
            return;
        }
        tableCount = parseInt(tableCount, 10);

        if (tableCount * tableSize < nameCount) {
            alert("You just don't have enough tables. This is never going to work...");
            return;
        }

        var annealingTime = $('#annealing-time').val();
        if (! annealingTime.match(/^\d+$/)) {
            alert("Please enter an integer for annealing time.");
            return;
        }
        annealingTime = parseInt(annealingTime, 10);

        var explorationSteps = $('#exploration-steps').val();
        if (! explorationSteps.match(/^\d+$/)) {
            alert("Please enter an integer for exploration steps.");
            return;
        }
        explorationSteps = parseInt(explorationSteps, 10);


        $("#loading").show();
        $.ajax({
            url: $SCRIPT_ROOT + "/find-solution/",
            dataType: 'json',
            type: 'POST',
            data: {
                connections: getRawConnectionsData(),
                annealingTime: annealingTime,
                explorationSteps: explorationSteps,
                tableCount: tableCount,
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

    $("#plans").on("click", ".save-plan", function (ev) {
        ev.preventDefault();
        $tbl = $(ev.target).closest("table").clone();
        $tbl.find("tfoot").remove();
        downloadFile("<table>" + $tbl.html() + "</table>", "plan.html");
    });

});
