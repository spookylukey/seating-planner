var connectionsMatrix;


function getRawConnectionsData () {
    var data = connectionsMatrix.getData();
    var connections = [];
    for (i in data) {
        var row = data[i];
        for (j in row) {
            var d = row[j];
            connections.push(d);
            if (j < row.length - 1) {
                connections.push(",")
            }
        }
        connections.push("\n");
    }
    return connections.join("");
}

function updateMatrixFromRaw () {
    var raw = $("#connections-raw").val();
    var rows = raw.trim().split(/\n/);
    var m = [];
    for (i in rows) {
        l = [];
        parts = rows[i].split(/,/);
        for (j in parts) {
            l.push(parts[j])
        }
        m.push(l);
    }
    $("#connections-matrix-controls").show();
    $("#connections-raw-controls").hide();
    connectionsMatrix.loadData(m);
    return true;
}

$(document).ready(function () {

    var $tbl = $("#connections");

    function mirrorChange(x, y, val) {
        connectionsMatrix.setDataAtCell(y, x, val, "mirrorChange");
    }

    function afterChange (changes, source) {
        if (source == "edit" || source == "autofill") {
            for (i in changes) {
                var change = changes[i];
                mirrorChange(change[0], change[1], change[3]);
            }
        }
    }

    $tbl.handsontable({
        data: [[""]],
        rowHeaders: false,
        colHeaders: false,
        fixedRowsTop: 1,
        fixedColumnsLeft: 1,
        cells: function (row, col, prop) {
            var cellProperties = {};
            if (row == 0 || col == 0 || row == col) {
                cellProperties.readOnly = true;
            }
            return cellProperties;
        },
        afterChange: afterChange,
        contextMenu: false
    });

    connectionsMatrix = $tbl.data('handsontable');

    function addNamesToConnections (names) {
        var existingData = connectionsMatrix.getData();
        var newNames = names.slice();
        for (i in newNames) {
            if (newNames[i].match(/,/)) {
                alert("Names must not contain the comma character");
                return;
            }
        }
        for (i in newNames) {
            var newName = newNames[i];

            // Add a new row
            var templateRow = existingData[0].slice();
            for (j in templateRow) {
                if (j == 0) {
                    templateRow[j] = newName;
                } else {
                    templateRow[j] = "";
                }
            }
            existingData.push(templateRow);

            // Add a new column. Have to add item to each row.
            for (j in existingData) {
                row = existingData[j];
                if (j == 0) {
                    row.push(newName);
                } else {
                    row.push("");
                }
            }
            var idx = existingData.length - 1;
            existingData[idx][idx] = "0";
        }
        connectionsMatrix.loadData(existingData);
    };

    $("#add-names").click(function (ev) {
        var names = $("#names").val().trim().split(/\n/);
        addNamesToConnections(names);
    });

    $("#show-raw-connections").click(function () {
        $("#connections-matrix-controls").hide();
        $("#connections-raw").val(getRawConnectionsData());
        $("#connections-raw-controls").show();
    });

    $("#hide-raw-connections").click(function () {
        $("#connections-matrix-controls").show();
        $("#connections-raw-controls").hide();
    });

    $("#update-matrix").click(function () {
        updateMatrixFromRaw();
    });

});

