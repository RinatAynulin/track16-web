function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    function update_likes() {
        ids = Array();

        $('.votes-count').each(function () {
            ids.push($(this).data('post-id'));
        });

        $.getJSON('/posts/likes', {ids: ids.join(',')}, function (data) {
            for (var i in data) {
                $('.votes-count[data-post-id=' + i + ']').html(data[i])
            }
        })
    }

    function get_liked_posts() {
        ids = Array();

        $('.votes-count').each(function () {
            ids.push($(this).data('post-id'));
        });

        $.getJSON('/posts/liked_posts', {ids: ids.join(',')}, function (data) {
            for (var i in data) {
                if (data[i] == 1) {
                    $('.arrow-up[data-post-id=' + i + ']').css('border-bottom', '10px solid blue');
                } else if (data[i] == -1) {
                    $('.arrow-down[data-post-id=' + i+ ']').css('border-top', '10px solid blue');
                }
            }
        });
    }

    update_likes();
    get_liked_posts();
    window.setInterval(update_likes, 5000);

    $('.arrow-up').click(function () {
        var url = $(this).data('url');
        csrftoken = getCookie('csrftoken');
        var element = $(this);
        var params = {};
        params['vote-type'] = 1;
        $.ajax({
            type: "POST",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: url,
            data: params,
            dataType: "json",
            success: function (data) {
                element.css('border-bottom', '')
                    .css('border-bottom', '10px solid blue');
                $('.arrow-down[data-post-id=' + element.data('post-id') + ']').css('border-top', '10px solid black');
                $('.votes-count[data-post-id=' + element.data('post-id') + ']').html(data);
            }
        });
    });

    $('.arrow-down').click(function () {
        var url = $(this).data('url');
        csrftoken = getCookie('csrftoken');
        var element = $(this);
        var params = {};
        params['vote-type'] = -1;
        $.ajax({
            type: "POST",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url: url,
            data: params,
            dataType: "json",
            success: function (data) {
                element.css('border-top', '')
                    .css('border-top', '10px solid blue');
                $('.arrow-up[data-post-id=' + element.data('post-id') + ']').css('border-bottom', '10px solid black');
                $('.votes-count[data-post-id=' + element.data('post-id') + ']').html(data);
            }
        });
    })
});