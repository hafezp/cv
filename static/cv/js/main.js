//Use Strict Mode
(function($) {
	"use strict";

//Begin - Window Load
$(window).load(function(){


	//==============___Page Loader___================
	
	$('#page-loader').delay(300).fadeOut(400, function(){

	});

	$('#loader-name').addClass('loader-left');
	$('#loader-job').addClass('loader-right');
	$('#loader-animation').addClass('loader-hide');

});

//Begin - Document Ready
$(document).ready(function(){

//==============___Page Loader___================
	$('#loading-wraper').fadeIn(300);

//==============___Testimonials - owl Carousel___================
 $("#testimonial-carousel").owlCarousel({
		navigation : false, // Show next and prev buttons
		slideSpeed : 300,
		paginationSpeed : 400,      
		responsiveRefreshRate : 200,
		responsiveBaseWidth: window,
		pagination: true,
		singleItem: true,    
		navigationText: ["<span class='fa fa-chevron-left'></span>","<span class='fa fa-chevron-right'></span>"],     
	});


//==============_Map_================
$('.map').on('click', function(){
	$('.map-overlay').hide();
});

$('.map').on('mouseleave', function(){
	$('.map-overlay').show();
});

//==============_Lightbox_================
//Nivo Lightbox
	$('a.nivobox').nivoLightbox({ effect: 'fade' });


//==============___Scrollbars___================
$('.section-vcardbody').perfectScrollbar({
	wheelSpeed: 0.9
});

//==============___Menu & Pages Animation___================

var linkHome = 0;
var linkPage = '';

function pageOn(){
		$('#main-menu').addClass('main-menu-pgactive');
		$('#section-home').addClass('section-vcardbody-pgactive');    
		$('.profileActive').removeClass('profileActive');    
		$('#profile2').addClass('profileActive');
		
		linkHome = 1;
}

function pageOff(){
		$('.section-page-active').removeClass('section-page-active');
		$('#main-menu').removeClass('main-menu-pgactive');
		$('#section-home').removeClass('section-vcardbody-pgactive');
		$('.profileActive').removeClass('profileActive');
		$('#profile1').addClass('profileActive');
		linkHome = 0;
}


$(".link-page").on('click', function(event){
	event.preventDefault();
	$('.menuActive').removeClass('menuActive');  
	$(this).addClass('menuActive');
	linkPage = $(this).attr('href');
	$('.section-page-active').removeClass('section-page-active');
	$(linkPage).addClass('section-page-active');
	pageOn();
});


$(".link-home").on('click', function(event){
	event.preventDefault();

	if (linkHome == 0) {
		//pageOn();
	}
	else if (linkHome == 1) {
		$('.menuActive').removeClass('menuActive');
		$(this).addClass('menuActive');
		pageOff();
	}  
});




//==============___Blog - Ajax___================
function loadPost(){

	$.ajax({
			url: 'single/1', 
			type: 'GET',
			success: function(html) {

				var $lis = $(html).find('#blogPost'); // Loads the content inside #blogPost div

				$("#postHere").html($lis);
		}
	});
}

$(".loadPost").on('click', function(event){
	event.preventDefault();
	//$("#postHere").html('loading...');
	$('.section-page-active').removeClass('section-page-active');
	$('#page-blog-single').addClass('section-page-active');
	pageOn();
	loadPost();
});



//================================hafez=====================================


$("#contactForm").submit(function(e){
	// prevent from normal form behaviour

	e.preventDefault();
	// serialize the form data

	var serializedData = $(this).serialize();

	$.ajax({
			type : 'POST',
			url : "",
			data : serializedData,

			success : function(response){
				//reset the form after successful submit
				alert("???????? ???? ???????????? ?????????? ????");
				$("#contactForm")[0].reset();
			},

			error : function(response){
				// console.log(response)
				alert("??????");
				}
		});
 });


//================================hafez=====================================


//==============___Contact Form Validator and Ajax Sender___================
	// $("#contactForm").validate({
	//   submitHandler: function(form) {
	//     $.ajax({
	//       type: "POST",
	//       url: "{% url 'cv:contact' %}",
	//       data: {
	//         "name": $("#contactForm #name").val(),
	//         "email": $("#contactForm #email").val(),
	//         "text": $("#contactForm #text").val(),
	//       },
	//       dataType: "json",
	//       success: function (data) {
	//         if (data.response == "success") {
	//           $("#contactSuccess").fadeIn(300);
	//           $("#contactError").addClass("hidden");

	//           $("#contactForm #name, #contactForm #email, #contactForm #text")
	//             .val("")
	//             .blur()
	//             .closest(".control-group")
	//             .removeClass("success")
	//             .removeClass("error");              
						
	//         } else {
	//           $("#contactError").fadeIn(300);
	//           $("#contactSuccess").addClass("hidden");
	//         }
	//       }

	//     });
	//   }
	// });


//Modal for Contact Form
$('.modal-wrap').click(function(){
	$('.modal-wrap').fadeOut(300);
});   

//End - Document Ready
});

//End - Use Strict mode
})(jQuery);