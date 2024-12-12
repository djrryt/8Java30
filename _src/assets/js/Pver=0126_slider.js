$(function () {

    $('.loop-slider').slick({
        autoplay: true,
        autoplaySpeed: 0,
        speed: 15000,
        arrows: false,
        slidesToShow: 4,
        cssEase: "linear",
        pauseOnHover: false,    //追加（ホバーしても止まらないように
        pauseOnFocus: false,    //追加（フォーカスしても止まらないように
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 1,
                    autoplaySpeed: 3000,
                    speed: 1500,
                    fade: true,
                },
            },
        ],
    });

    $('.loop-slider-index').slick({
        autoplay: true,
        autoplaySpeed: 0,
        speed: 15000,
        arrows: false,
        slidesToShow: 3,
        cssEase: "linear",
        pauseOnHover: false,    //追加（ホバーしても止まらないように
        pauseOnFocus: false,    //追加（フォーカスしても止まらないように
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                },
            },
        ]
    });

    $('.fade-slider,.first-view .slider').slick({
        autoplay: true,
        autoplaySpeed: 3000,
        speed: 1500,
        arrows: false,
        slidesToShow: 1,
        cssEase: "linear",
        pauseOnHover: false,    //追加（ホバーしても止まらないように
        pauseOnFocus: false,    //追加（フォーカスしても止まらないように
        fade: true,
    });

}); 