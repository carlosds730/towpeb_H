var MinimalTheme = {};

jQuery(window).ready(function(){

  
  $('.flexslider').flexslider({
    animation: "slide",
    slideshow: true,
    animationDuration: 700,
    slideshowSpeed: 6000,
    animation: "fade",
    controlsContainer: ".flex-controls",
    controlNav: false,
    keyboardNav: true
  }).hover(function(){ $('.flex-direction-nav').fadeIn();}, function(){$('.flex-direction-nav').fadeOut();});
  
});

jQuery(window).load(function(){

  $("select.loc_on_change").change(function(){
    if($(this).find(":selected").attr("value") == "#") return false;
    window.location = $(this).find(":selected").attr("value");
  });

});

jQuery(document).ready(function($){

  // force wide nav -->
  
  // <-- end force wide nav

  $(".flyout").hide();

  $("#menu-button").on("click", function() {
    $(".flyout").slideToggle( "fast" );
  });

  $(".sub-menu").hide();
  $(".more, .account-links").on("click", function() {
    $(this).nextAll("ul").slideToggle( "fast" );
    $("i", this).toggleClass("fa-plus fa-minus");
    $(this).next(".more").find("i").toggleClass("fa-user fa-minus");
  });

  $("nav.mobile select").change(function(){ window.location = jQuery(this).val(); });

  
    $("a.fancy").fancybox({
      padding: 0,
      margin: [50, 20, 50, 20],
      afterShow: function(){
        $(".fancybox-next span").html('<i class="fa fa-chevron-right"></i>');
        $(".fancybox-prev span").html('<i class="fa fa-chevron-left"></i>');
        $(".fancybox-close").html('<i class="fa fa-times"></i>');
     },
      helpers:  {
        thumbs : {
          width: 30,
          height: 30,
          source: function(current) {
                    return $(current.element).attr('href').replace('_1024x1024.','_icon.');
                  },
          position: 'bottom'
        }
      }
    });

    /* Update fancybox gallery image */
    $('#placeholder').on('click', function(evt) {
      evt.preventDefault();
      var imageId = $(this).data('image-id');
      $('#lightbox a[data-image-id="' + imageId + '"]').trigger('click');
    });
  

  MinimalTheme.switchImage = function(newSizedImageSrc, newImage, mainImageDomEl) {
    var largestImage = newSizedImageSrc.replace('_1024x1024.', '.');
    $(mainImageDomEl)
      .attr('src', newSizedImageSrc)
      .parents('a')
      .attr('href', largestImage);
    
      $(mainImageDomEl).parents('a').data('image-id', newImage.id);
    
  };

  $('#product .thumbs a').click(function(e){
    e.preventDefault();
    var newSizedImageSrc = $(this).attr('href'),
        mainImageDomEl = $('.image.featured img')[0],
        newImageId = $(this).data('image-id');
    MinimalTheme.switchImage(newSizedImageSrc, { id: newImageId }, mainImageDomEl);
  });

  $('input[type="submit"], input.btn, button').click(function(){ // remove ugly outline on input button click
    $(this).blur();
  })

  $('li.dropdown').hover(function(){
    $(this).children('.dropdown').show();
    $(this).children('.dropdown').stop();
    $(this).children('.dropdown').animate({
      opacity: 1.0
    }, 200);
  }, function(){
    $(this).children('.dropdown').stop();
    $(this).children('.dropdown').animate({
      opacity: 0.0
    }, 400, function(){
      $(this).hide();
    });
  });

});
