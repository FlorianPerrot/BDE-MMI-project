var scroll_speed = 500, // en ms
    diapo_speed = 1000,
    diapo_auto = 5000,
    home_appear_first_time = false;



jQuery(document).ready(function($){
    var main = $("#main"),
        nav = $("#navigation");
        nav_h = nav.height();
    var main_offset_top = parseInt(main.offset().top);

    if($(document).width() <= 1024){
        $("nav").addClass("nav-bar-colored");
    }

    window.mySwipe = new Swipe(document.querySelector("#diapo"), {
        startSlide: 0,
        speed: diapo_speed,
        auto: diapo_auto,
        continuous: true
    });

    $("#ctrl-next").click(function(e){
        window.mySwipe.next();
    });
    $("#ctrl-prec").click(function(e){
        window.mySwipe.prev();
    });

    $(window).resize(function(){
        main_offset_top = parseInt(main.offset().top);
    });

	$(window).scroll(function(e){
        main.offset({top: main_offset_top});
        if(main.offset().top > nav.offset().top + 100 && $(document).width() > 1024){
            $("nav").removeClass("nav-bar-colored");
        }else{
            $("nav").addClass("nav-bar-colored");
        }
        if($("#wrap-diapo").offset().top > nav.offset().top && $(document).width() > 1024){
            $("footer").css("display", "none");
        }else{
            $("footer").css("display", "block");
        }
    });

    $("nav a").click(function(e){
        e.preventDefault();
        var target = $(this).attr("href");
        if(target != "#contact"){
            $('html, body').animate( { scrollTop: $(target).offset().top }, scroll_speed );
        }else{
            if($(document).width() <= 1024){
                $('html, body').animate( { scrollTop: $("footer").offset().top }, scroll_speed );
            }else{
                $('html, body').animate( { scrollTop: $(document).height() }, scroll_speed );
            }
        }
		return false;
    });

    $("#go_articles").click(function(e){
        e.preventDefault();
        $('html, body').animate( { scrollTop: $("#wrap-home").offset().top }, scroll_speed );
        return false;
    })

});
