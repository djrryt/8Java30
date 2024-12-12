$(function () {

    // inview
    $(".inview").on("inview", function (event, isInView) {
        if (isInView) {
            $(this).stop().addClass("is-show");
            $('html').css("scroll-behavior", "smooth");
        }
        if (isInView) {
            $(this).stop().addClass("animation");
        }
    });

    // ハンバーガー
    $('.menu-btn').on('click', function () {
        $('.btn__menu').toggleClass('active');
        $('.menu-mobile').toggleClass('active');
        $('main').toggleClass('menu-active');
    });

    $('main').on('click', function () {
        $('.btn__menu').removeClass('active');
        $('.menu-mobile').removeClass('active');
        $('main').removeClass('menu-active');
    });

    //事業者紹介

    $('.hover-link').hover(
        function () {
            $('.hover-link-content').addClass('active');
        },
        function () {
            $('.hover-link-content').removeClass('active');
        }
    );

    //

    $('#child-work1').hover(function () {
        // すべての要素に対してremoveClassを実行
        $('[id^=img-work],[id^=child-work]').removeClass('active');
        // img-work2にだけactiveクラスを追加
        $('#img-work1,#child-work1').addClass('active');
    });

    $('#child-work2').hover(function () {
        // すべての要素に対してremoveClassを実行
        $('[id^=img-work],[id^=child-work]').removeClass('active');
        // img-work2にだけactiveクラスを追加
        $('#img-work2,#child-work2').addClass('active');
    });

    $('#child-work3').hover(function () {
        // すべての要素に対してremoveClassを実行
        $('[id^=img-work],[id^=child-work]').removeClass('active');
        // img-work2にだけactiveクラスを追加
        $('#img-work3,#child-work3').addClass('active');
    });

    $('#child-work4').hover(function () {
        // すべての要素に対してremoveClassを実行
        $('[id^=img-work],[id^=child-work]').removeClass('active');
        // img-work2にだけactiveクラスを追加
        $('#img-work4,#child-work4').addClass('active');
    });

    $('#child-work5').hover(function () {
        // すべての要素に対してremoveClassを実行
        $('[id^=img-work],[id^=child-work]').removeClass('active');
        // img-work2にだけactiveクラスを追加
        $('#img-work5,#child-work5').addClass('active');
    });

    $('#child-work6').hover(function () {
        // すべての要素に対してremoveClassを実行
        $('[id^=img-work],[id^=child-work]').removeClass('active');
        // img-work2にだけactiveクラスを追加
        $('#img-work6,#child-work6').addClass('active');
    });


    $('#person-1').hover(function () {
        $('[id^=person-],[id^=content-],[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('#person-1,#content-1,.schdule-1,.schdule-img-1').addClass('active');
    });

    $('#person-2').hover(function () {
        $('[id^=person-],[id^=content-],[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('#person-2,#content-2,.schdule-1,.schdule-img-1').addClass('active');
    });

    $('#person-3').hover(function () {
        $('[id^=person-],[id^=content-],[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('#person-3,#content-3,.schdule-1,.schdule-img-1').addClass('active');
    });

    $('.schdule-1').hover(function () {
        $('[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('.schdule-1,.schdule-img-1').addClass('active');
    });

    $('.schdule-2').hover(function () {
        $('[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('.schdule-2,.schdule-img-2').addClass('active');
    });

    $('.schdule-3').hover(function () {
        $('[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('.schdule-3,.schdule-img-3').addClass('active');
    });

    $('.schdule-4').hover(function () {
        $('[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('.schdule-4,.schdule-img-4').addClass('active');
    });

    $('.schdule-5').hover(function () {
        $('[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('.schdule-5,.schdule-img-5').addClass('active');
    });

    $('.schdule-6').hover(function () {
        $('[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('.schdule-6,.schdule-img-6').addClass('active');
    });

    $('.schdule-7').hover(function () {
        $('[class^=schdule-],[class^=schdule-img-]').removeClass('active');
        $('.schdule-7,.schdule-img-7').addClass('active');
    });


    //ナビアニメーション
    var lastScrollPosition = 0;
    // スクロールイベントを監視
    window.addEventListener('scroll', function () {
        // 現在のスクロール位置を取得
        var currentScrollPosition = window.scrollY;

        // スクロール方向の判定
        if (currentScrollPosition > lastScrollPosition) {
            // 下向きスクロール
            document.querySelector('.desk-nav').classList.add('hidden');
        } else {
            // 上向きスクロール
            document.querySelector('.desk-nav').classList.remove('hidden');
            ;
        }
        // 現在のスクロール位置を前回の位置として保存
        lastScrollPosition = currentScrollPosition;
    });

});