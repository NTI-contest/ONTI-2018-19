(function($) {
    var wow = new WOW({
    boxClass:     'wow',      
    animateClass: 'animated', 
    offset:       0,          
    mobile:       true,      
    live:         true,       
    callback:     function(box) {},
    scrollContainer: null,    
    resetAnimation: true,
   }
  );
  wow.init();})(jQuery);  