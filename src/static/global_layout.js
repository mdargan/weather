$(function() {

    function get_cookie(cookie_name) {
        var cookie = document.cookie;
        
        if(cookie.length != 0) {
            var cookie_value = cookie.match(
                '(^|;)[\s]*' + cookie_name + '=([^;]*)' );
            return decodeURIComponent (cookie_value[2]);
        }
        return '' ;
    }

    function set_cookie(cookie_name, cookie_value) {
        document.cookie = cookie_name + "=" + encodeURIComponent( cookie_value ) +
            "; max-age=" + 60*60*24 * 365;
    }


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
                    
                    var tile = '<div class="tile' + ' tile-' + key + '">'
                        + '<div class="weather-text">'
                        + '     <span class="weather-title">' + key + '</span>'
                        + '     <span>Start: ' + $.format.date(start, 'dd/MM/yyyy') + '</span>';

                     if(key != "current") {
                        tile += '<span>End: ' + $.format.date(end, 'dd/MM/yyyy') + '</span>'
                             + '<span>' + val[2] + ' days streak</span>';
                     }                        
                     tile += "</div>";
                     target.append(tile);
                });
            }
        });
    }

    $('#city').change(function() {
        set_cookie("city_preset",  $("#city").val());
        get_city_stats();
    });

    var city = get_cookie("city_preset");
    $("#city").val(city.length > 0 ? city : "Moscow");
    get_city_stats();
});

