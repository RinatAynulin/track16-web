$(document).ready(function () {
    $('.edit-post-link').click(function () {
        $("#modal-edit-post").modal();
        $(".modal-body p").load($(this).attr("href"));
        return false; // without default callback
    });

    $('.edit-comment-link').click(function () {
        $("#modal-edit-comment").modal();
        $(".modal-comment-body p").load($(this).attr("href"));
        return false; // without default callback
    });

    $(document).on('submit', '.form-ajax', function () {
        var form = $(this);
        $.post(form.attr('action'), form.serialize(), function (data) {
            if (data == 'success') {
                location.reload();
            }
            else {
                form.html(data);
            }
        });
        return false;
    });
});