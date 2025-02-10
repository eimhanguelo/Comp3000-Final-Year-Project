$(document).ready( function () {
    $('table.display').DataTable({

        // "pagingType": "full_numbers",
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
        searching: True,
        ordering: True,
        select: true,

    });
});

