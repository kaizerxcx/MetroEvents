$(document).ready(function() {
    var table= $('#activity-table').DataTable({
        dom: 'lBfrtip',
        buttons: true,
        buttons: [
            'pdf'
        ]
    });
    $("#searchTxb").keyup(function(){
        table.search($("#searchTxb").val().toString());
        table.draw();
    });
    $("#exportBtn").on("click",function(){
        $(".buttons-pdf").trigger("click");
    });
    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            var min = $('#fromDate').val() == "" ? null : new Date($('#fromDate').val());
            var max = $('#toDate').val() == "" ? null : new Date($('#toDate').val());
            var startDate = new Date(data[0]);
            console.log(startDate);
            if (min == null && max == null) { return true; }
            if (min == null && startDate <= max) { return true; }
            if (max == null && startDate >= min) { return true; }
            if (startDate <= max && startDate >= min) { return true; }
            return false;
        }
    );
    $('#fromDate, #toDate').change(function() {
        table.draw();
    });
    $('#select-type-activities').on("change",function(){
        table
        .columns( 3 )
        .search( this.value );
        table.draw();
    });
    $('#select-status-activities').on("change",function(){
        table
        .columns( 4 )
        .search( this.value );
        table.draw();
    });
} );
$(function () {

    $('.datepicker').datepicker({
        clearBtn: true,
        format: "mm-dd-yyyy"
    });
});