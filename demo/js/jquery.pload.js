(function ($) {
    $.fn.pload = function(pload_obj){
        $(this).on('click', function (e) {
            container = pload_obj.container || "body";
            start = pload_obj.start || function(){return};
            onSuccess = pload_obj.onSuccess || function(){return};
            e.preventDefault();
            start();
            url = pload_obj.url || $(this).attr('href');
            $('body').load(url + pload_obj.container, function () {
                window.history.pushState(null, '', url);
                onSuccess();
            })
        });
    }
})(jQuery)