/**
 * jQuery lightBox plugin
 * This jQuery plugin was inspired and based on Lightbox 2 by Lokesh Dhakar (http://www.huddletogether.com/projects/lightbox2/)
 * and adapted to me for use like a plugin from jQuery.
 * @name jquery-lightbox-0.5d.js
 * @author Leandro Vieira Pinho - http://leandrovieira.com
 * @version 0.5d
 * @date April 11, 2008
 * @category jQuery plugin
 * @copyright (c) 2008 Leandro Vieira Pinho (leandrovieira.com)
 * @license CC Attribution-No Derivative Works 2.5 Brazil - http://creativecommons.org/licenses/by-nd/2.5/br/deed.en_US
 * @example Visit http://leandrovieira.com/projects/jquery/lightbox/ for more informations about this jQuery plugin
 *
 * modified by Pierangelo Baggio, May 18, 2008
 * every line modified have been marked with "PBAGGIO" label
 * removed lines, have been removed ;)
 * main modifications:
 * - moved plug-in variables from "settings" object to "my" object
 * - added "autoDetectGroups" setting (and code), to allow image grouping in rel
 *         attribute:   <a href... rel="[group 1]"> or <a href... rel="lightbox[group 1]"> or <a href... rel="myrel[group 1]"> and so on....
 * - added "imageResizable" setting (and code), that allow images to remain in window viewport, without needs of scrolling
 * - replaced "txtImage" and "txtOf" settings with a more flexible "captionFunction" which may accept a function to render the caption text
 * - added "imageBaseDir" setting (and code), that allow the user to (optionally) specify the directory where are located the images
 *         needed by this script (so, images, don't need the full path anymore), that let's user just to specify this one,
 *         leaving other "image..." settings to their default value
 * - added a *space* in inline style, replacing    style=""    with     style=" ", that's because, sometimes, the original definition
 *         (without the space), occasionally - and almost randomly - generate an error on mozilla firefox "firebug" plug-in.
 *         Is the inline specification of empty-style really necessary?
 * - added the function "_set_dimensions" for some repeated operation
 * - added the code to manage various form elements, like "select", "input", and so on... to hide and show again, to prevent some IE problems...
 *         now the code remember which elements have been hidden, and then re-show only them (not tested yet ;-)
 */

// Offering a Custom Alias suport - More info: http://docs.jquery.com/Plugins/Authoring#Custom_Alias
(function($) {
	/**
	 * $ is an alias to jQuery object
	 *
	 */
	$.fn.lightBox = function(settings) {
		// Settings to configure the jQuery lightBox plugin how you like
		settings = jQuery.extend({
			// Configuration related to overlay
			 overlayBgColor: 			'#000'	// (string) Background color to overlay; inform a hexadecimal value like: #RRGGBB. Where RR, GG, and BB are the hexadecimal values for the red, green, and blue values of the color.
			,overlayOpacity:			0.8		// (integer) Opacity value to overlay; inform: 0.X. Where X are number from 0 to 9
			// Configuration related to navigation
			,fixedNavigation:			false		// (boolean) Boolean that informs if the navigation (next and prev button) will be fixed or not in the interface.
			// Configuration related to images
			,imageBaseDir:				'imgages/lightbox' // <--- PBAGGIO // trailing "/" can be savetly either omitted or specified...
			,imageLoading:				'lightbox-ico-loading.gif'		// (string) Path and the name of the loading icon
			,imageBtnPrev:				'lightbox-btn-prev.gif'			// (string) Path and the name of the prev button image
			,imageBtnNext:				'lightbox-btn-next.gif'			// (string) Path and the name of the next button image
			,imageBtnClose:				'lightbox-btn-close.gif'		// (string) Path and the name of the close btn
			,imageBlank:				'lightbox-blank.gif'			// (string) Path and the name of a blank image (one pixel)
			// Configuration related to container image box
			,containerBorderSize:	10			// (integer) If you adjust the padding in the CSS for the container, #lightbox-container-image-box you will need to update this value
			,containerResizeSpeed:	300		// (integer) Specify the resize duration of container image. These number are miliseconds. 400 is default.
			// Configuration related to texts in caption. For example: Image 2 of 8. You can alter either "Image" and "of" texts.
			,captionFunction:			_default_caption // <--- PBAGGIO
			// Configuration related to keyboard navigation
			,keyToClose:				'c'		// (string) (c = close) Letter to close the jQuery lightBox interface. Beyond this letter the letter X and the SCAPE key is used to.
			,keyToPrev:					'p'		// (string) (p = previous) Letter to show the previous image
			,keyToNext:					'n'		// (string) (n = next) Letter to show the next image.
			// <--- PBAGGIO (new settings) // new settings
			,imageResizable:			true // <--- PBAGGIO
			,fix_MSIE_Width:			21 // <--- PBAGGIO
			,marginTop:					20 // <--- PBAGGIO
			,reduceMaxHeight:			120 // <--- PBAGGIO
			,autoDetectGroups:			true // <--- PBAGGIO
			,langPicture:				'Picture' // <--- radeksir
			,langOf:					'from' // <--- radeksir
		},settings);
		if (settings.imageBaseDir) settings.imageBaseDir = settings.imageBaseDir.replace(/[/\\]+$/, '') + '/'; // <--- PBAGGIO

		var my = { // <--- PBAGGIO // this object collect the various variables needed (it's better to use "settings" only for real settings ;-)
			 jQueryMatchedObjs: 		this // This, in this context, refer to jQuery matched object(s)
			,jQueryGroupedObjs: 		false // <--- PBAGGIO // filter jQueryMatchedObjs by current object
			,imageArray:				[]
			,activeImage:				0
			,jLightBoxHidedInputs:	false // <--- PBAGGIO
			,groupName:					'' // <--- PBAGGIO
		};
		/**
		 * Initializing the plugin calling the start function
		 *
		 * @return boolean false
		 */
		function _initialize() {
			_start(this); // This, in this context, refer to object (link) which the user have clicked
			return false; // Avoid the browser following the link
		}
		/**
		 * Start the jQuery lightBox plugin
		 *
		 * @param object objClicked The object (link) whick the user have clicked
		 */
		function _start(objClicked) {
			my.groupName = ''; // <--- PBAGGIO
			my.jQueryGroupedObjs = false; // <--- PBAGGIO
			if (settings.autoDetectGroups) { // <--- PBAGGIO
				var rel = $(objClicked).attr('rel'); // <--- PBAGGIO
				if (rel) { // <--- PBAGGIO
					rel = rel.match(/\[(.*)\]$/); // <--- PBAGGIO
					if (rel) { // <--- PBAGGIO
						my.groupName = rel[1]; // <--- PBAGGIO
						my.jQueryGroupedObjs = my.jQueryMatchedObjs.filter('[rel$=\'['+rel[1]+']\']'); // <--- PBAGGIO
					} // <--- PBAGGIO
				} // <--- PBAGGIO
			} // <--- PBAGGIO
			if (!my.jQueryGroupedObjs) my.jQueryGroupedObjs = my.jQueryMatchedObjs; // <--- PBAGGIO
			// Hide some elements to avoid conflict with overlay in IE. These elements appear above the overlay.
			my.jLightBoxHidedInputs = $(':input').filter(':not(:hidden)').hide(); // <--- PBAGGIO
			// Call the function to create the markup structure; style some elements; assign events in some elements.
			_set_interface();
			// Unset total images in my.imageArray // <--- PBAGGIO
			my.imageArray.length = 0; // <--- PBAGGIO
			// Unset image active information
			my.activeImage = 0; // <--- PBAGGIO
			// We have an image set? Or just an image? Let´s see it.
			if ( my.jQueryGroupedObjs.length == 1 ) { // <--- PBAGGIO
				my.imageArray.push(new Array(objClicked.getAttribute('href'),objClicked.getAttribute('title'))); // <--- PBAGGIO
			} else {
				// Add an Array (as many as we have), with href and title atributes, inside the Array that storage the images references
				for ( var i = 0; i < my.jQueryGroupedObjs.length; i++ ) { // <--- PBAGGIO
					my.imageArray.push(new Array(my.jQueryGroupedObjs[i].getAttribute('href'),my.jQueryGroupedObjs[i].getAttribute('title'))); // <--- PBAGGIO
				}
			}
			while ( my.imageArray[my.activeImage][0] != objClicked.getAttribute('href') ) { // <--- PBAGGIO
				my.activeImage++; // <--- PBAGGIO
			}
			// Call the function that prepares image exibition
			_set_image_to_view();
		}
		/** // <--- PBAGGIO
		 * Create the default caption text // <--- PBAGGIO
		 * // <--- PBAGGIO
		 * @param integer current The number of current image // <--- PBAGGIO
		 * @param integer length The total number of images // <--- PBAGGIO
		 * @param boolean showGroup Must show group name? // <--- PBAGGIO
		 * @param string groupName The group name of current image. If image is ungrouped then groupName='' // <--- PBAGGIO
		 */ // <--- PBAGGIO
		function _default_caption(current,length,showGroup,groupName) { // <--- PBAGGIO
			var $ret = settings.langPicture + ' <strong>' + current + '</strong> ' + settings.langOf + ' <strong>' + length + '</strong>'; // <--- PBAGGIO
			if (showGroup && groupName) $ret += ''; // <--- PBAGGIO
			return $ret; // <--- PBAGGIO
		} // <--- PBAGGIO
		/**
		 * Create the jQuery lightBox plugin interface
		 *
		 */
		function _set_interface() { // <--- PBAGGIO (many lines removed by)
			// Apply the HTML markup into body tag
			$('body').append( // <--- PBAGGIO
				 '<div style="display:none" id="jquery-overlay"></div>' // <--- PBAGGIO
				+'<div style="display:none" id="jquery-lightbox">' // <--- PBAGGIO
					+'<div id="lightbox-container-image-box"><div id="lightbox-container-image">' // <--- PBAGGIO
						+'<img id="lightbox-image">' // <--- PBAGGIO
						+'<div style=" " id="lightbox-nav">' // <--- PBAGGIO
							+'<a href="#" id="lightbox-nav-btnPrev"></a>' // <--- PBAGGIO
							+'<a href="#" id="lightbox-nav-btnNext"></a>' // <--- PBAGGIO
						+'</div>' // <--- PBAGGIO
						+'<div id="lightbox-loading">' // <--- PBAGGIO
							+'<a href="#" id="lightbox-loading-link">' // <--- PBAGGIO
								+'<img src="' + settings.imageBaseDir + settings.imageLoading + '">' // <--- PBAGGIO
							+'</a>' // <--- PBAGGIO
						+'</div>' // <--- PBAGGIO
					+'</div></div>' // <--- PBAGGIO
					+'<div id="lightbox-container-image-data-box"><div id="lightbox-container-image-data">' // <--- PBAGGIO
						+'<div id="lightbox-image-details">' // <--- PBAGGIO
							+'<span id="lightbox-image-details-caption"></span>' // <--- PBAGGIO
							+'<span id="lightbox-image-details-currentNumber"></span>' // <--- PBAGGIO
						+'</div>' // <--- PBAGGIO
						+'<div id="lightbox-secNav">' // <--- PBAGGIO
							+'<a href="#" id="lightbox-secNav-btnClose">' // <--- PBAGGIO
								+'<img src="' + settings.imageBaseDir + settings.imageBtnClose + '">' // <--- PBAGGIO
							+'</a>' // <--- PBAGGIO
						+'</div>' // <--- PBAGGIO
					+'</div></div>' // <--- PBAGGIO
				+'</div>' // <--- PBAGGIO
			); // <--- PBAGGIO
			_set_dimensions(); // <--- PBAGGIO
			// Style overlay and show it
			$('#jquery-overlay').css({
				backgroundColor:	settings.overlayBgColor,
				opacity:				settings.overlayOpacity
			}).fadeIn();
			$('#jquery-lightbox').show();
			// Assigning click events in elements to close overlay
			$('#jquery-overlay,#jquery-lightbox').click(function() {
				_finish();
			});
			// Assign the _finish function to lightbox-loading-link and lightbox-secNav-btnClose objects
			$('#lightbox-loading-link,#lightbox-secNav-btnClose').click(function() {
				_finish();
				return false;
			});
			// If window was resized, calculate the new overlay dimensions
			$(window).resize(_set_dimensions); // <--- PBAGGIO
		}

		/**
		 * Set overlay and lightbox dimensions, for initial use and when window is resized
		 *
		 */
		function _set_dimensions() { // <--- PBAGGIO (added by) // pay attention: "this", here, *may* means "window"... never use "this"!!
			// Get page sizes
			var arrPageSizes = ___getPageSize();
			// Style overlay and show it
			$('#jquery-overlay').css({
				width:		arrPageSizes[0],
				height:		arrPageSizes[1]
			});
			// Get page scroll
			var arrPageScroll = ___getPageScroll();
			// Calculate top and left offset for the jquery-lightbox div object and show it
			$('#jquery-lightbox').css({
				top:	arrPageScroll[1] + settings.marginTop, // <--- PBAGGIO
				left:	arrPageScroll[0]
			});
		}

		/**
		 * Prepares image exibition; doing an image´s preloader to calculate it´s size
		 *
		 */
		function _set_image_to_view() { // show the loading
			// Show the loading
			$('#lightbox-loading').show();
			if ( settings.fixedNavigation ) {
				$('#lightbox-image,#lightbox-container-image-data-box,#lightbox-image-details-currentNumber').hide();
			} else {
				// Hide some elements
				$('#lightbox-image,#lightbox-nav,#lightbox-nav-btnPrev,#lightbox-nav-btnNext,#lightbox-container-image-data-box,#lightbox-image-details-currentNumber').hide();
			}
			// Image preload process
			var objImagePreloader = new Image();
			objImagePreloader.onload = function() {
				var w = objImagePreloader.width; // <--- PBAGGIO
				var h = objImagePreloader.height; // <--- PBAGGIO
				if (settings.imageResizable) { // <--- PBAGGIO
					var max_w = $(window).width() - 30; // <--- PBAGGIO
					var max_h = $(window).height() - settings.reduceMaxHeight; // <--- PBAGGIO
					if (w >= max_w) { h = (h / w) * max_w; w = max_w; } // <--- PBAGGIO
					if (h >= max_h) { w = (w / h) * max_h; h = max_h; } // <--- PBAGGIO
					h = parseInt(h); w = parseInt(w); // <--- PBAGGIO
				} // <--- PBAGGIO
				$('#lightbox-image').attr({
					'src': my.imageArray[my.activeImage][0] // <--- PBAGGIO
					,width: w // <--- PBAGGIO
					,height: h // <--- PBAGGIO
				});
				// Perfomance an effect in the image container resizing it
				_resize_container_image_box(w,h); // <--- PBAGGIO
				//	clear onLoad, IE behaves irratically with animated gifs otherwise
				objImagePreloader.onload=function(){};
			};
			objImagePreloader.src = my.imageArray[my.activeImage][0]; // <--- PBAGGIO
		};
		/**
		 * Performe an effect in the image container resizing it
		 *
		 * @param integer intImageWidth The image´s width that will be showed
		 * @param integer intImageHeight The image´s height that will be showed
		 */
		function _resize_container_image_box(intImageWidth,intImageHeight) {
			// Get current width and height
			var intCurrentWidth = $('#lightbox-container-image-box').width();
			var intCurrentHeight = $('#lightbox-container-image-box').height();
			// Get the width and height of the selected image plus the padding
			var intWidth = (intImageWidth + (settings.containerBorderSize * 2)); // Plus the image´s width and the left and right padding value
			var intHeight = (intImageHeight + (settings.containerBorderSize * 2)); // Plus the image´s height and the left and right padding value
			// Diferences
			var intDiffW = intCurrentWidth - intWidth;
			var intDiffH = intCurrentHeight - intHeight;
			// Perfomance the effect
			$('#lightbox-container-image-box')
				.animate({ width: intWidth, height: intHeight },settings.containerResizeSpeed,function() { _show_image(); });
			if ( ( intDiffW == 0 ) && ( intDiffH == 0 ) ) {

					___pause(100);

			}
			$('#lightbox-container-image-data-box').css({ width: intImageWidth });
			$('#lightbox-nav-btnPrev,#lightbox-nav-btnNext').css({ height: intImageHeight + (settings.containerBorderSize * 2) });
		};
		/**
		 * Show the prepared image
		 *
		 */
		function _show_image() {
			$('#lightbox-loading').hide();
			$('#lightbox-image').fadeIn(function() {
				_show_image_data();
				_set_navigation();
			});
			_preload_neighbor_images();
		};
		/**
		 * Show the image information
		 *
		 */
		function _show_image_data() {
			$('#lightbox-container-image-data-box').slideDown('fast');
			$('#lightbox-image-details-caption').hide();
			if ( my.imageArray[my.activeImage][1] ) { // <--- PBAGGIO
				$('#lightbox-image-details-caption').html(my.imageArray[my.activeImage][1]).show(); // <--- PBAGGIO
			}
			// If we have a image set, display 'Image X of X'
			if ( my.imageArray.length > 1 ) { // <--- PBAGGIO
				var txt = settings.captionFunction(my.activeImage + 1,my.imageArray.length,settings.autoDetectGroups,my.groupName); // <--- PBAGGIO
				$('#lightbox-image-details-currentNumber').html(txt).show(); // <--- PBAGGIO
			}
		}
		/**
		 * Display the button navigations
		 *
		 */
		function _set_navigation() {
			$('#lightbox-nav').show();

			// Instead to define this configuration in CSS file, we define here. And it´s need to IE. Just.
			$('#lightbox-nav-btnPrev,#lightbox-nav-btnNext').css({ 'background' : 'transparent url(' + settings.imageBaseDir+settings.imageBlank + ') no-repeat' }); // <--- PBAGGIO

			// Show the prev button, if not the first image in set
			if ( my.activeImage != 0 ) { // <--- PBAGGIO
				if ( settings.fixedNavigation ) {
					$('#lightbox-nav-btnPrev').css({ 'background' : 'url(' + settings.imageBaseDir+settings.imageBtnPrev + ') left 15% no-repeat' }) // <--- PBAGGIO
						.unbind()
						.bind('click',function() {
							my.activeImage = my.activeImage - 1; // <--- PBAGGIO
							_set_image_to_view();
							return false;
						});
				} else {
					// Show the images button for Next buttons
					$('#lightbox-nav-btnPrev').unbind().hover(function() {
						$(this).css({ 'background' : 'url(' + settings.imageBaseDir+settings.imageBtnPrev + ') left 15% no-repeat' }); // <--- PBAGGIO
					},function() {
						$(this).css({ 'background' : 'transparent url(' + settings.imageBaseDir+settings.imageBlank + ') no-repeat' }); // <--- PBAGGIO
					}).show().bind('click',function() {
						my.activeImage = my.activeImage - 1; // <--- PBAGGIO
						_set_image_to_view();
						return false;
					});
				}
			}

			// Show the next button, if not the last image in set
			if ( my.activeImage != ( my.imageArray.length -1 ) ) { // <--- PBAGGIO
				if ( settings.fixedNavigation ) {
					$('#lightbox-nav-btnNext').css({ 'background' : 'url(' + settings.imageBaseDir+settings.imageBtnNext + ') right 15% no-repeat' }) // <--- PBAGGIO
						.unbind()
						.bind('click',function() {
							my.activeImage = my.activeImage + 1; // <--- PBAGGIO
							_set_image_to_view();
							return false;
						});
				} else {
					// Show the images button for Next buttons
					$('#lightbox-nav-btnNext').unbind().hover(function() {
						$(this).css({ 'background' : 'url(' + settings.imageBaseDir+settings.imageBtnNext + ') right 15% no-repeat' }); // <--- PBAGGIO
					},function() {
						$(this).css({ 'background' : 'transparent url(' + settings.imageBaseDir+settings.imageBlank + ') no-repeat' }); // <--- PBAGGIO
					}).show().bind('click',function() {
						my.activeImage = my.activeImage + 1; // <--- PBAGGIO
						_set_image_to_view();
						return false;
					});
				}
			}
			// Enable keyboard navigation
			_enable_keyboard_navigation();
		}
		/**
		 * Enable a support to keyboard navigation
		 *
		 */
		function _enable_keyboard_navigation() {
			$(document).keydown(function(objEvent) {
				_keyboard_action(objEvent);
			});
		}
		/**
		 * Disable the support to keyboard navigation
		 *
		 */
		function _disable_keyboard_navigation() {
			$(document).unbind();
		}
		/**
		 * Perform the keyboard actions
		 *
		 */
		function _keyboard_action(objEvent) {
			// To ie
			if ( objEvent == null ) {
				keycode = event.keyCode;
				escapeKey = 27;
			// To Mozilla
			} else {
				keycode = objEvent.keyCode;
				escapeKey = objEvent.DOM_VK_ESCAPE;
			}
			// Get the key in lower case form
			key = String.fromCharCode(keycode).toLowerCase();
			// Verify the keys to close the ligthBox
			if ( ( key == settings.keyToClose ) || ( key == 'x' ) || ( keycode == escapeKey ) ) {
				_finish();
			}
			// Verify the key to show the previous image
			if ( ( key == settings.keyToPrev ) || ( keycode == 37 ) ) {
				// If we´re not showing the first image, call the previous
				if ( my.activeImage != 0 ) { // <--- PBAGGIO
					my.activeImage = my.activeImage - 1; // <--- PBAGGIO
					_set_image_to_view();
					_disable_keyboard_navigation();
				}
			}
			// Verify the key to show the next image
			if ( ( key == settings.keyToNext ) || ( keycode == 39 ) ) {
				// If we´re not showing the last image, call the next
				if ( my.activeImage != ( my.imageArray.length - 1 ) ) { // <--- PBAGGIO
					my.activeImage = my.activeImage + 1; // <--- PBAGGIO
					_set_image_to_view();
					_disable_keyboard_navigation();
				}
			}
		}
		/**
		 * Preload prev and next images being showed
		 *
		 */
		function _preload_neighbor_images() {
			if ( (my.imageArray.length -1) > my.activeImage ) { // <--- PBAGGIO
				objNext = new Image();
				objNext.src = my.imageArray[my.activeImage + 1][0]; // <--- PBAGGIO
			}
			if ( my.activeImage > 0 ) { // <--- PBAGGIO
				objPrev = new Image();
				objPrev.src = my.imageArray[my.activeImage -1][0]; // <--- PBAGGIO
			}
		}
		/**
		 * Remove jQuery lightBox plugin HTML markup
		 *
		 */
		function _finish() {
			$('#jquery-lightbox').remove();
			$('#jquery-overlay').fadeOut(function() { $('#jquery-overlay').remove(); });
			// Show some elements to avoid conflict with overlay in IE. These elements appear above the overlay.
			if (my.jLightBoxHidedInputs) { // <--- PBAGGIO
				my.jLightBoxHidedInputs.show(); // <--- PBAGGIO
				my.jLightBoxHidedInputs = false; // <--- PBAGGIO
			}
		}
		/**
		 / THIRD FUNCTION
		 * getPageSize() by quirksmode.com
		 *
		 * @return Array Return an array with page width, height and window width, height
		 */
		function ___getPageSize() {
			var xScroll, yScroll;
			if (window.innerHeight && window.scrollMaxY) {
				xScroll = window.innerWidth + window.scrollMaxX;
				yScroll = window.innerHeight + window.scrollMaxY;
			} else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
				xScroll = document.body.scrollWidth;
				yScroll = document.body.scrollHeight;
			} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
				xScroll = document.body.offsetWidth;
				yScroll = document.body.offsetHeight;
			}
			var windowWidth, windowHeight;
			if (self.innerHeight) {	// all except Explorer
				if(document.documentElement.clientWidth){
					windowWidth = document.documentElement.clientWidth;
				} else {
					windowWidth = self.innerWidth;
				}
				windowHeight = self.innerHeight;
			} else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
				windowWidth = document.documentElement.clientWidth;
				windowHeight = document.documentElement.clientHeight;
			} else if (document.body) { // other Explorers
				windowWidth = document.body.clientWidth;
				windowHeight = document.body.clientHeight;
			}
			// for small pages with total height less then height of the viewport
			if(yScroll < windowHeight){
				pageHeight = windowHeight;
			} else {
				pageHeight = yScroll;
			}
			// for small pages with total width less then width of the viewport
			if(xScroll < windowWidth){
				pageWidth = xScroll;
			} else {
				pageWidth = windowWidth;
			}
			arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight);
			return arrayPageSize;
		};
		/**
		 / THIRD FUNCTION
		 * getPageScroll() by quirksmode.com
		 *
		 * @return Array Return an array with x,y page scroll values.
		 */
		function ___getPageScroll() {
			var xScroll, yScroll;
			if (self.pageYOffset) {
				yScroll = self.pageYOffset;
				xScroll = self.pageXOffset;
			} else if (document.documentElement && document.documentElement.scrollTop) {	 // Explorer 6 Strict
				yScroll = document.documentElement.scrollTop;
				xScroll = document.documentElement.scrollLeft;
			} else if (document.body) {// all other Explorers
				yScroll = document.body.scrollTop;
				xScroll = document.body.scrollLeft;
			}
			arrayPageScroll = new Array(xScroll,yScroll);
			return arrayPageScroll;
		};
		 /**
		  * Stop the code execution from a escified time in milisecond
		  *
		  */
		 function ___pause(ms) {
			var date = new Date();
			curDate = null;
			do { var curDate = new Date(); }
			while ( curDate - date < ms);
		 };
		// Return the jQuery object for chaining. The unbind method is used to avoid click conflict when the plugin is called more than once
		return this.unbind('click').click(_initialize);
	};
})(jQuery); // Call and execute the function immediately passing the jQuery object
