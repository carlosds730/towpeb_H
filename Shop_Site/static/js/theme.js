/* Simple jQuery Equal Heights @version 1.5.1. Copyright (c) 2013 Matt Banks. Dual licensed under the MIT and GPL licenses. */
!function (a) {
    a.fn.equalHeights = function () {
        var b = 0, c = a(this);
        return c.each(function () {
            var c = a(this).innerHeight();
            c > b && (b = c)
        }), c.css("height", b)
    }, a("[data-equal]").each(function () {
        var b = a(this), c = b.data("equal");
        b.find(c).equalHeights()
    })
}(jQuery);

/* Run function after window resize */
var afterResize = (function () {
    var t = {};
    return function (callback, ms, uniqueId) {
        if (!uniqueId) {
            uniqueId = "Don't call this twice without a uniqueId";
        }
        if (t[uniqueId]) {
            clearTimeout(t[uniqueId]);
        }
        t[uniqueId] = setTimeout(callback, ms);
    };
})();

window.theme = window.theme || {};

theme.cacheSelectors = function () {
    theme.cache = {
        // General
        $w: $(window),
        $body: $('body'),

        // Mobile Nav
        $mobileNavTrigger: $('#MobileNavTrigger'),
        $mobileNav: $('#MobileNav'),
        $mobileSublistTrigger: $('.mobile-nav__sublist-trigger'),

        // Equal height elements
        $productGridImages: $('.grid-link__image--product'),
        $featuredGridImages: $('.grid-link__image--collection'),

        // Product page
        $productImage: $('#ProductPhotoImg'),
        $productImageGallery: $('.gallery__item'),

        // Cart Page
        cartNoteAdd: '.cart__note-add',
        cartNote: '.cart__note'
    }
};

theme.init = function () {
    theme.cacheSelectors();
    theme.mobileNav();
    theme.equalHeights();
    theme.cartPage();


    theme.productImageGallery();

};

theme.mobileNav = function () {
    theme.cache.$mobileNavTrigger.on('click', function () {
        theme.cache.$mobileNav.slideToggle(220);
    });

    theme.cache.$mobileSublistTrigger.on('click', function (evt) {
        var $el = $(this);

        // Enable commented out if statement to allow direct clicking on trigger link
        // if (!$el.hasClass('is-active')) {
        evt.preventDefault();
        $el.toggleClass('is-active').next('.mobile-nav__sublist').slideToggle(200);
        // }
    });
};

theme.equalHeights = function () {
    theme.cache.$w.on('load', resizeElements());

    theme.cache.$w.on('resize',
        afterResize(function () {
            resizeElements();
        }, 250, 'equal-heights')
    );

    function resizeElements() {
        theme.cache.$productGridImages.css('height', 'auto').equalHeights();
        theme.cache.$featuredGridImages.css('height', 'auto').equalHeights();
    }
};

theme.productImageGallery = function () {

    if (!theme.cache.$productImageGallery.length) {
        return;
    }
    ;

    theme.cache.$productImageGallery.magnificPopup({
        type: 'image',
        mainClass: 'mfp-fade',
        closeOnBgClick: true,
        closeBtnInside: false,
        closeOnContentClick: true,
        tClose: 'Close (Esc)',
        removalDelay: 500,
        gallery: {
            enabled: true,
            navigateByImgClick: false,
            arrowMarkup: '<button title="%title%" type="button" class="mfp-arrow mfp-arrow-%dir%"><span class="mfp-chevron mfp-chevron-%dir%"></span></button>',
            tPrev: 'Previous (Left arrow key)',
            tNext: 'Next (Right arrow key)'
        }
    });

    theme.cache.$productImage.bind('click', function () {
        var imageId = $(this).attr('data-image-id');
        theme.cache.$productImageGallery.filter('[data-image-id="' + imageId + '"]').trigger('click');
    });
};

theme.cartPage = function () {


    theme.cache.$body.on('click', theme.cache.cartNoteAdd, function () {
        $(this).addClass('is-hidden');
        $(theme.cache.cartNote).addClass('is-active');
        ajaxifyShopify.sizeDrawer();
    });
};

// Initialize theme's JS on docready
$(theme.init)
