$(function() {

    function get_city_stats() {
        var city = $("#city").val();
        $.getJSON('/city_stats.json', function(data) {
            var target = $('#stats ul');
            target.empty();
            $.each(data, function (key, val) {
                target.append('<li>' + val + '</li>');
            });
        });
    }

    $('#city').change(function() {
        get_city_stats();
    });

    get_city_stats();
});

