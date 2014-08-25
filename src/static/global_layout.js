$(function() {

    function get_city_stats() {
        var city = $("#city").val();
        $.getJSON("/city_stats.json?city=" + city, function(data) {
            if(data["result"] != "ok")
                alert("server error occured");
            else {
                var target = $('#periods');
                target.empty();
                $.each(data["list"], function (key, val) {
                        
                    var start = new Date(Date.parse(val[0]));
                    var end = new Date(Date.parse(val[1]));
                    
                    target.append('<div class="tile' + ' tile-' + key + '">'
                        + '<div class="weather-text">'
                        + '     <span class="weather-title">' + key + '</span>'
                        + '     <span>Start: ' + $.format.date(start, 'dd/MM/yyyy') + '</span>'
                        + '     <span>End: ' + $.format.date(end, 'dd/MM/yyyy') + '</span>'
                        + '     <span>' + val[2] + ' days streak</span>'
                    
                        + '</div>');
                });
            }
        });
    }

    $('#city').change(function() {
        get_city_stats();
    });

    get_city_stats();
});

