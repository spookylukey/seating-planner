$(document).ready(function () {

    var $tbl = $("#connections");

    function mirrorChange(x, y, val) {
        ht.setDataAtCell(y, x, val, "mirrorChange");
    }

    function afterChange (changes, source) {
        if (source == "edit" || source == "autofill") {
            for (i in changes) {
                var change = changes[i];
                mirrorChange(change[0], change[1], change[3]);
            }
        }
        console.log(changes);
        console.log(source);
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

    var ht = $tbl.data('handsontable');

    function addNamesToConnections (names) {
        var existingData = ht.getData();
        var newNames = names.slice();
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
        ht.loadData(existingData);
    };

    $("#update-connections").click(function (ev) {
        var names = $("#names").val().trim().split(/\n/);
        addNamesToConnections(names);
    });

});

