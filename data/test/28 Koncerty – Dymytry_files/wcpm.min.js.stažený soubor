/*! Wolf Custom Post Meta Wordpress Plugin v1.0.1 */ 
/*!
 * Custom Post Meta 1.0.2
 */
/* jshint -W062 */
/* global WolfCustomPostMetaJSParams, Cookies */
var WolfCustomPostMeta=function(a){"use strict";return{/**
		 * Init UI
		 */
init:function(){this.views(),this.likes()},/**
		 * Increment views meta count
		 */
views:function(){if(a("body").hasClass("single")){var b=a('[id^="post-"]'),c=this.getPostId(b),d={action:"wolf_custom_post_meta_ajax_increment_views",postId:c};a.post(WolfCustomPostMetaJSParams.ajaxUrl,d,function(){})}},/**
		 * Check liked
		 *
		 * Verify if a post has already been liked using cookies.
		 */
checkLikedPosts:function(){var b,c=this,d=a('[id^="post-"]');d.each(function(){b=c.getPostId(a(this)),Cookies.get(WolfCustomPostMetaJSParams.themeSlug+"-w-likes-"+b)&&a(this).find(".wolf-like-this").addClass("wolf-liked")})},/**
		 * Increment likes meta count
		 */
likes:function(b){var c;this.checkLikedPosts(),a(document).on("click",".wolf-like-this",function(d){if(d.preventDefault(),c=a(this),b=a(this).data("post-id"),!a(this).hasClass("wolf-liked")&&!Cookies.get(WolfCustomPostMetaJSParams.themeSlug+"-w-likes-"+b)){var e={action:"wolf_custom_post_meta_ajax_increment_likes",postId:b};c.addClass("wolf-liked"),a.post(WolfCustomPostMetaJSParams.ajaxUrl,e,function(a){a&&(Cookies.set(WolfCustomPostMetaJSParams.themeSlug+"-w-likes-"+b,!0),c.find(".wolf-likes-count").length&&c.find(".wolf-likes-count").html(a))})}})},/**
		 * Get post ID
		 */
getPostId:function(a){var b;return a.data("post-id")?b=a.data("post-id"):a.attr("id")&&(b=a.attr("id").replace("post-","")),b}}}(jQuery);!function(a){"use strict";a(document).ready(function(){WolfCustomPostMeta.init()})}(jQuery);