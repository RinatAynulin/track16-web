$(document).ready(function () {
    function update_likes() {
        ids = Array()

        $('.votes-count').each(function () {
            ids.push($(this).data('post-id'));
        })

        $.getJSON('/posts/likes', {ids: ids.join(',')}, function (data) {
            for (var i in data) {
                $('.votes-count[data-post-id='+i+']').html(data[i])
            }
        })
    }
    update_likes();
    window.setInterval(update_likes, 5000);

    $('.arrow-up').click(function () {
        
    })
});