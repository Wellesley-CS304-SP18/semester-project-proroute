/*
Copyright (c) 2017 DoctorDirectory
------------------------------------------------------------------
[Master Javascript]

Project:	DoctorDirectory

-------------------------------------------------------------------*/
var b_url = $('#b_url').val();
(function ($) {
	"use strict";
	var DoctorDirectory = {
		initialised: false,
		version: 1.0,
		mobile: false,
		init: function () {

			if(!this.initialised) {
				this.initialised = true;
			} else {
				return;
			}

			/*-------------- DoctorDirectory Functions Calling ---------------------------------------------------
			------------------------------------------------------------------------------------------------*/
			this.RTL();
			this.PopUps();
			this.SidebarOpen();
			
		},
		
		/*-------------- DoctorDirectory Functions definition ---------------------------------------------------
		---------------------------------------------------------------------------------------------------*/
		RTL: function () {
			// On Right-to-left(RTL) add class 
			var rtl_attr = $("html").attr('dir');
			if(rtl_attr){
				$('html').find('body').addClass("rtl");	
			}		
        },
        PopUps: function(){
            $('.jp_popup_link').on('click', function(){
                $('body').addClass('popup_open');
            });
            $('.jp_popup_close').on('click', function(){
                $('body').removeClass('popup_open');
            });
        },
        SidebarOpen: function(){
			$('.jp_nav_toggle').on('click', function(){
				$('body').removeClass('jp_cat_sidebar_open');
				$('body').toggleClass('jp_sidebar_open');
			});
			$('.jp_category_toggle').on('click', function(){
				$('body').removeClass('jp_sidebar_open');
				$('body').toggleClass('jp_cat_sidebar_open');
			});
			$('.jp_sidebar_close').on('click', function(){
				$('body').removeClass('jp_sidebar_open');
				$('body').removeClass('jp_cat_sidebar_open');
			});
            
        },
		BackToTop: function(){
			//Goto Top
			$(window).scroll(function() {
				if ($(this).scrollTop() > 100) {
					$("#jp_backToTop").addClass('btt_show')
				} else {
					$("#jp_backToTop").removeClass('btt_show')
				}
			});
			$("#jp_backToTop").on("click", function() {
				$("html, body").animate({
					scrollTop: 0
				}, 600);
				return false
			});
		}
		
		
	};

	// Load Event
	$(window).on('load', function() {
		$(".jp_loading_wrapper").delay(350).fadeOut("slow");
		
		var body_h = window.innerHeight;
		$('body').css('height',body_h);
		
		// add class on body
		setTimeout(function(){
			$('body').addClass('jp_site_loaded');
		},1000);
	});

	// Resize Event
	$(window).on('resize', function () {
		var body_h = window.innerHeight;
		$('body').css('height',body_h);
	});
	
	$(window).on('scroll', function () {
		
	});
	
	
	// ready function
	$(document).ready(function() {
		DoctorDirectory.init();
		DoctorDirectory.BackToTop();
	});
	
	
})(jQuery);
