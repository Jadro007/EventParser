/*! Wolf Share Wordpress Plugin v1.0.8 */ 
/*!
 * Wolf Share 1.0.8 
 */
/* jshint -W062 */
/* global WolfShareJSParams */
var WolfShare=function(a){"use strict";return{/**
		 * Init UI
		 */
init:function(){this.shareLinkPopup()},/**
		 * Share Links Popup
		 */
shareLinkPopup:function(){var b=this;a(".wolf-share-link").on("click",function(){var c,d=a(this),e=d.attr("href"),f=d.data("height")||250,g=d.data("width")||500,h=d.parent().parent().data("post-id");if(h&&b.incrementShareCount(h),!0===a(this).data("popup")&&!b.isMobile&&!d.hasClass("wolf-share-link-email"))return c=window.open(e,"null","height="+f+",width="+g+", top=150, left=150"),window.focus&&c.focus(),!1})},/**
		 * Increment share met count
		 */
incrementShareCount:function(b){var c={action:"wolf_share_ajax_increment_shares_count",postId:b};a.post(WolfShareJSParams.ajaxUrl,c,function(){})}}}(jQuery);!function(a){"use strict";a(document).ready(function(){WolfShare.init()})}(jQuery);