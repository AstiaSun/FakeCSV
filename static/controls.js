function delete_csv_column(node) {
    node.closest('.schema_column').remove();
}

function show_integer_bounds(node){
    var parent = node.closest(".schema_column");
    var selected_type = $(parent).find("option:selected").val();
    if (selected_type == "7") {
        $(parent).find("#integer_bounds").attr("hidden", false);
    } else {
        $(parent).find("#integer_bounds").attr("hidden", true);
    }
}

function add_csv_column() {
    var column_types = JSON.parse($('#column_types').val());
    options = ' ';
    for (column_type of column_types) {
        options += `<option value="${column_type.value}">
            ${column_type.name} </option>`
    }
    var new_column_html_text = `
    <div class="row g-3 schema_column">
        <div class="col col-3">
            <label class="form-label">Column Name</label>
            <input type="text" class="form-control column_name"
                   placeholder="Name" value required>
            <div class="invalid-feedback">Valid name is required</div>
        </div>
        <div class="col col-3">
            <label class="form-label">Type</label>
            <select class="form-select column_type"
            onchange="show_integer_bounds(this)">
                <option selected>----</option>
                ${options}
            </select>
        </div>
        <div class="col col-3">
            <div id="integer_bounds" hidden>
                <div class="row">
                    <div class="col col-5">
                        <label class="form-label">From</label>
                        <input type="text" class="form-control int_value_from"
                               placeholder="18">
                    </div>
                    <div class="col col-5">
                        <label class="form-label">To</label>
                        <input type="text" class="form-control int_value_to"
                               placeholder="90">
                    </div>
                </div>
            </div>
        </div>
        <div class="col col-3">
            <label class="form-label">Order</label>
            <div class="row">
                <div class="col">
                    <input type="number" class="form-control column_order">
                </div>
                <div class="col">
                    <button onclick="delete_csv_column(this)"
                    class="btn btn-link link-danger text-decoration-none">
                        Delete
                    </button>
                </div>
            </div>
        </div>
    </div>`;
    $('#columns').append(new_column_html_text);
}


function prepare_schema_columns_data() {
    var column_elements = $('#columns > div');
    var prepared_data = column_elements
    .sort(function(a, b) {
        var a_value = parseInt($(a).find('.column_order').val());
        var b_value = parseInt($(b).find('.column_order').val());
        return a_value - b_value;
    })
    .map(function() {
        return {
            column_name: $(this).find('.column_name').val(),
            column_type: parseInt($(this).find('.column_type').val()),
            int_value_from: parseInt($(this).find('.int_value_from').val()),
            int_value_to: parseInt($(this).find('.int_value_to').val())
        }
    }).get();
    $('#prepared_columns').val(JSON.stringify(prepared_data));
}
