(function ($) {
            $('#id_password1').complexify({}, function (valid, complexity) {
                var progressBar = $('#complexity-bar');

                progressBar.toggleClass('progress-bar-success', valid);
                progressBar.toggleClass('progress-bar-danger', !valid);
                progressBar.css({'width': complexity + '%'});

                $('#complexity').text(Math.round(complexity) + '%');
            });

        })(jQuery);