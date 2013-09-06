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

function updateMatrixFromRaw (raw) {
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
    connectionsMatrix.loadData(m);
    return true;
}

$(document).ready(function () {

    var $tbl = $("#connections");
    var leftGroup = null;
    var topGroup = null;
    var groups = {left: [],
                  top: []};
    var groupSuffices = ["left", "top"];

    function resetGroups () {
        groups.left = [];
        groups.top = [];
    }

    function afterChange (changes, source) {
        if (source == "edit" || source == "autofill") {
            var newChanges = [];
            for (var i in changes) {
                var change = changes[i];
                var r = change[0];
                var c = change[1];
                var val = change[3];

                // Mirror
                newChanges.push([c, r, val]);

                // Groups
                var inTopGroup = groups.top.indexOf(c) != -1;
                var inLeftGroup = groups.left.indexOf(r) != -1;
                if (inTopGroup || inLeftGroup) {
                    // Propagate to group
                    var cols, rows;
                    if (inTopGroup) {
                        cols = groups.top;
                    } else {
                        cols = [c];
                    }
                    if (inLeftGroup) {
                        rows = groups.left;
                    } else {
                        rows = [r];
                    }
                    for (var a in rows) {
                        for (var b in cols) {
                            var r2 = rows[a];
                            var c2 = cols[b];
                            if (!((r == r2 && c == c2) ||
                                  (r2 == c2)))
                            {
                                newChanges.push([r2, c2, val])
                                newChanges.push([c2, r2, val])
                            }
                        }
                    }
                }
            }
            connectionsMatrix.setDataAtCell(newChanges, "mirrorChanges");
        }
    }

    function enableAddToGroupBtn (suffix) {
        $("#add-to-group-" + suffix).removeAttr("disabled");
    }

    function enableRemoveFromGroupBtn (suffix) {
        $("#remove-from-group-" + suffix).removeAttr("disabled");
    }

    function disableAddToGroupBtn (suffix) {
        $("#add-to-group-" + suffix).attr("disabled", "disabled");
    }

    function disableRemoveFromGroupBtn (suffix) {
        $("#remove-from-group-" + suffix).attr("disabled", "disabled");
    }

    function enableGroupExistsBtns (suffix) {
        $("#clear-group-" + suffix).removeAttr("disabled");
        $("#mirror-group-" + suffix).removeAttr("disabled");
    }

    function disableGroupExistsBtns (suffix) {
        $("#clear-group-" + suffix).attr("disabled", "disabled");
        $("#mirror-group-" + suffix).attr("disabled", "disabled");
    }

    function updateGroupExistControls (suffix) {
        var group = groups[suffix];
        if (group.length == 0) {
            disableGroupExistsBtns(suffix);
        } else {
            enableGroupExistsBtns(suffix)
        }
    }

    function afterSelectionEnd (r, c, r2, c2) {
        if (r == 0 && r2 == 0 && c != 0 && c2 != 0) {
            enableAddToGroupBtn("top");
            enableRemoveFromGroupBtn("top");
        } else {
            disableAddToGroupBtn("top");
            disableRemoveFromGroupBtn("top")
        }
        if (c == 0 && c2 == 0 && r != 0 && r2 != 0) {
            enableAddToGroupBtn("left");
            enableRemoveFromGroupBtn("left");
        } else {
            disableAddToGroupBtn("left");
            disableRemoveFromGroupBtn("left");
        }
    }

    function cellRenderer (instance, td, row, col, prop, value, cellProperties) {
        Handsontable.TextCell.renderer.apply(this, arguments);
        if (groups.left.indexOf(row) != -1 ||
            groups.top.indexOf(col) != -1) {
            td.style.background = "#eee";
        } else {
            td.style.background = "#fff";
        }
    }

    $tbl.handsontable({
        data: [[""]],
        rowHeaders: false,
        colHeaders: false,
        height: 600,
        fixedRowsTop: 1,
        fixedColumnsLeft: 1,
        cells: function (row, col, prop) {
            var cellProperties = {};
            if (row == 0 || col == 0 || row == col) {
                cellProperties.readOnly = true;
            }
            cellProperties.renderer = cellRenderer;
            return cellProperties;
        },
        afterChange: afterChange,
        afterSelectionEnd: afterSelectionEnd,
        outsideClickDeselects: false,
        contextMenu: false
    });

    connectionsMatrix = $tbl.data('handsontable');

    function addNamesToConnections (names) {
        var existingData = connectionsMatrix.getData();
        var newNames = names.slice();
        for (var i in newNames) {
            if (newNames[i].match(/,/)) {
                alert("Names must not contain the comma character");
                return false;
            }
            if (nameInConnections(newNames[i])) {
                alert("Name '" + newNames[i] + "' is already in the matrix");
                return false;
            }
        }
        for (var i in newNames) {
            var newName = newNames[i];

            // Add a new row
            var templateRow = existingData[0].slice();
            for (var j in templateRow) {
                if (j == 0) {
                    templateRow[j] = newName;
                } else {
                    templateRow[j] = "";
                }
            }
            existingData.push(templateRow);

            // Add a new column. Have to add item to each row.
            for (var j in existingData) {
                var row = existingData[j];
                if (j == 0) {
                    row.push(newName);
                } else {
                    row.push("");
                }
            }
            var idx = existingData.length - 1;
            existingData[idx][idx] = "0";
        }
        resetGroups();
        connectionsMatrix.loadData(existingData);
        return true;
    };

    function nameInConnections (name) {
        var existingData = connectionsMatrix.getData();
        for (var i in existingData) {
            if (existingData[i][0] == name) {
                return true;
            }
        }
        return false;
    }

    function removeNamesFromConnections (names) {
        var existingData = connectionsMatrix.getData();
        var newNames = names.slice();

        for (var i in newNames) {
            var newName = newNames[i];
            if (!nameInConnections(newName)) {
                alert("Name '" + newName + "' is not in the matrix");
                return false;
            }
        }

        for (var i in newNames) {
            var newName = newNames[i];
            // Remove row
            for (var j in existingData) {
                var row = existingData[j];
                if (row[0] == newName) {
                    existingData.splice(j, 1);
                    break;
                }
            }
            // remove column
            var headerRow = existingData[0];
            var idx = headerRow.indexOf(newName);
            for (var j in existingData) {
                var row = existingData[j];
                row.splice(idx, 1);
            }
        }
        resetGroups();
        connectionsMatrix.loadData(existingData);

        return true;

    }

    function downloadConnections () {
        // Need the download to happen inline, without leaving the page.  We
        // also need the data to come from the actually page.
        // So we embed an iframe with a self-submitting form
        if (connectionsMatrix.getData().length < 2) {
            alert("There is no data entered yet");
            return;
        }
        $("#file-data-raw").val(getRawConnectionsData());
        $('#download-container').append('<iframe height="1", width="1" frameborder="0" src="' + $SCRIPT_ROOT + '/download-form/"></iframe>');
    }

    function uploadConnections () {
        var xhr = new XMLHttpRequest();
        var file = $("#upload-selector").get(0).files[0];
        if (file == undefined) {
            alert("No file has been selected for upload.");
            return;
        }
        xhr.file = file;
        xhr.onreadystatechange = function(e) {
            if (this.readyState == 4) {
                console.log(['xhr upload complete', e]);
                updateMatrixFromRaw(xhr.response);
            }
        };
        xhr.open('post', $SCRIPT_ROOT + "/upload-connections/", true);
        xhr.send(file);
    }


    // --- Wiring ---

    $("#add-names").click(function (ev) {
        var names = $("#names").val().trim().split(/\n/);
        if (addNamesToConnections(names)) {
            $('#names').val('');
        }
    });

    $("#remove-names").click(function (ev) {
        var names = $("#names-to-remove").val().trim().split(/\n/);
        if (removeNamesFromConnections(names)) {
            $("#names-to-remove").val('');
        }
    });

    $("#download-connections").click(function (ev) {
        downloadConnections();
    });

    $("#upload-connections").click(function (ev) {
        ev.preventDefault();
        uploadConnections();
    });

    function makeGroupUnique (group) {
        // Has to edit the array in place, not return a new one.
        var seen = [];
        var i = 0;
        while (i < group.length) {
            item = group[i];
            if (seen.indexOf(item) == -1) {
                seen.push(item);
                i++;
            } else {
                group.splice(i, 1);
            }
        }
    }


    function makeAddToGroup (suffix) {
        var addToGroup = function (ev) {
            group = groups[suffix];
            s = connectionsMatrix.getSelected();
            // s = [startRow, startCol, endRow, endCol]
            if (suffix == "left") {
                for (var i = s[0]; i <= s[2]; i++) {
                    group.push(i);
                }
            } else {
                for (var i = s[1]; i <= s[3]; i++) {
                    group.push(i);
                }
            }
            makeGroupUnique(group);
            updateGroupExistControls(suffix);
            connectionsMatrix.render();
        };
        return addToGroup;
    }

    function makeRemoveFromGroup (suffix) {
        var removeFromGroup = function (ev) {
            group = groups[suffix];
            s = connectionsMatrix.getSelected();
            // s = [startRow, startCol, endRow, endCol]
            if (suffix == "left") {
                for (var i = s[0]; i <= s[2]; i++) {
                    group.splice(group.indexOf(i), 1);
                }
            } else {
                for (var i = s[1]; i <= s[3]; i++) {
                    group.splice(group.indexOf(i), 1);
                }
            }
            updateGroupExistControls(suffix);
            connectionsMatrix.render();
        };
        return removeFromGroup;
    }

    function makeClearGroup (suffix) {
        var clearGroup = function (ev) {
            group = groups[suffix];
            group.splice(0);
            updateGroupExistControls(suffix);
            connectionsMatrix.render();
        }
        return clearGroup;
    }

    function makeMirrorGroup (suffix) {
        var mirrorGroup = function (ev) {
            group = groups[suffix];
            otherSuffix = suffix == "left" ? "top" : "left";
            groups[otherSuffix] = group.slice();
            updateGroupExistControls(suffix);
            updateGroupExistControls(otherSuffix);
            connectionsMatrix.render();
        }
        return mirrorGroup;
    }

    for (var i in groupSuffices) {
        suffix = groupSuffices[i];
        $("#add-to-group-" + suffix).click(makeAddToGroup(suffix));
        $("#remove-from-group-" + suffix).click(makeRemoveFromGroup(suffix));
        $("#clear-group-" + suffix).click(makeClearGroup(suffix));
        $("#mirror-group-" + suffix).click(makeMirrorGroup(suffix));
    }

    disableAddToGroupBtn("left");
    disableRemoveFromGroupBtn("left");
    disableAddToGroupBtn("top");
    disableRemoveFromGroupBtn("top");

    disableGroupExistsBtns("left");
    disableGroupExistsBtns("top");

});

