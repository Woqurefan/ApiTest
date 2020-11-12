/**
 * rvnm Responsive vertical navigation menu
 *
 * Copyright (C) 2017 4xmen team <a1gard@4xmen.ir>
 *
 * LICENSE: This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 3 of the License, or (at your option) any
 * later version.  This program is distributed in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
 * Public License for more details.  You should have received a copy of the GNU
 * General Public License along with this program.
 * If not, see <http://opensource.org/licenses/gpl-license.php>.
 *
 * @package    rvnm
 * @author     4xmen team  <www.4xmen.ir>
 * @author     A1Gard <a1gard@4xmen.ir>
 * @link       https://github.com/4xmen/rvnm
 */

;
(function ($) {

    $.fn.rvnm = function (options) {


        /**
         * settings ofplgin
         * @type Object
         */
        var settings = $.extend({
            wrapper: '#wrapper', // main page wrapper
            mode: 'default', // mode of menu (default = desktop| minimal = tablet | mobile)
            responsive: true, // repsonsve mode only work in default mode
            theme: '',
            searchable: false,
        }, options);

        /**
         * sizetrigger is function to change nav box size
         * or control reponsive & mode of menu
         * @returns {undefined}
         */
        this.sizetrigger = function () {
            // repsonvive mode controller
            if (settings.responsive && settings.mode === 'default') {
                // if window size between 450 and 768 active minimal
                if ($(window).width() > 450 && $(window).width() < 768) {
                    if (!$(self).hasClass('rvnm-minimal')) {
                        // fix extended  after switch from defualt to minimal
                        $(self).find('.rvnm-collapseable ul').attr('style', '');
                        $(self).find('.rvnm-collapseable').addClass('rvnm-expandable').removeClass('rvnm-collapseable');
                    }
                    $(settings.wrapper).removeClass('rvnm-mobile');
                    $(self).removeClass('rvnm-mobile');
                    $(settings.wrapper).addClass('rvnm-minimal');
                    $(self).addClass('rvnm-minimal');
                }
                // if window size less than 450 active mobile mode
                if ($(window).width() <= 450) {
                    $(settings.wrapper).removeClass('rvnm-minimal');
                    $(self).removeClass('rvnm-minimal');
                    $(settings.wrapper).addClass('rvnm-mobile');
                    $(self).addClass('rvnm-mobile');
                }
                // if window size greater than 768 active desktop mode by
                // remove minimal & mobile calss
                if ($(window).width() >= 768) {
                    $(settings.wrapper).removeClass('rvnm-minimal');
                    $(self).removeClass('rvnm-minimal');
                    $(settings.wrapper).removeClass('rvnm-mobile');
                    $(self).removeClass('rvnm-mobile');
                }
            }
            $(".rvnm-navbar-box").css('height', '');
            if (settings.mode !== 'mobile' && !$(self).hasClass('rvnm-mobile')) {
                if ($(".rvnm-navbar-box").height() < $("body").height() || $(".rvnm-navbar-box").height() < $(window).height() || $(".rvnm-navbar-box").height() < $("html").height()) {
                    $(".rvnm-navbar-box").height(Math.max($('body').height(), $(window).height(), $("html").height()));
                }
            }


        };

        // set plugn selector to self for use in other place of plugin
        var self = this;

        this.each(function () {
            // add rvnm-navbar-box to menu
            $(this).addClass('rvnm-navbar-box');

            if (settings.searchable) {
                $(this).find('> ul').prepend('<li class="search"> <i class="fa fa-search"></i> <input class="rvnm-search" type="search" placeholder="Search..." />  </li>');
            }

            // add theme if extis
            if (settings.theme !== '') {
                $(this).addClass(settings.theme);
            }

            // add expandable class to li's has ul child
            $(this).find('li:has(> ul)').addClass('rvnm-expandable');
            // rvnm-wrapper class to main content element
            $(settings.wrapper).addClass('rvnm-wrapper');
            // check if minimal mode active change mode
            if ($(this).hasClass('rvnm-minimal') || settings.mode === 'minimal') {
                $(settings.wrapper).addClass('rvnm-minimal');
                $(this).addClass('rvnm-minimal');
                settings.mode = 'minimal';
            }
            // check if mobile mode active change mode
            if ($(this).hasClass('rvnm-minimal') || settings.mode === 'mobile') {
                $(settings.wrapper).addClass('rvnm-mobile');
                $(this).addClass('rvnm-mobile');
                settings.mode = 'mobile';
            }

            // resize navbar box
            self.sizetrigger();

            // add triger windows resize
            $(window).bind('resize.rvnm', function () {
                self.sizetrigger();
            });


            /**
             * ripple effect for links
             */
            $(document).on('click', '.rvnm-navbar-box ul li a', function (e) {
                // Remove any old one
                $(".rvnm-ripple").remove();

                // Setup
                var posX = $(this).offset().left,
                    posY = $(this).offset().top,
                    buttonWidth = $(this).width(),
                    buttonHeight = $(this).height();

                // Add the element
                $(this).prepend("<span class='rvnm-ripple'></span>");


                // Make it round!
                if (buttonWidth >= buttonHeight) {
                    buttonHeight = buttonWidth;
                } else {
                    buttonWidth = buttonHeight;
                }

                // Get the center of the element
                var x = e.pageX - posX - buttonWidth / 2;
                var y = e.pageY - posY - buttonHeight / 2;


                // Add the ripples CSS and start the animation
                $(".rvnm-ripple").css({
                    width: buttonWidth,
                    height: buttonHeight,
                    top: y + 'px',
                    left: x + 'px'
                }).addClass("rvnm-rippleEffect");

                setTimeout(function () {
                    $(".rvnm-ripple").remove();
                }, 600);

            });

            // add click event to expandable link 
            $(document).on('click', '.rvnm-expandable > a', function (e) {
                // check click only this element
                if (e.target !== e.currentTarget)
                    return false;

                // check is first level of li child and minimal mode siable
                if ($(this).parent().hasClass('rvnm-minimal-expand')) {
                    return false;
                }

                // check is first level of li child 
                // try to close other expanded items
                if ($(this).parent().closest('.rvnm-collapseable').length === 0) {
                    // slide up first level ul of this
                    $(".rvnm-collapseable > a").parent().find('> ul').slideUp(300);
                    // add expandable class to parent of link and remove collapseable
                    $(".rvnm-collapseable > a").parent().addClass('rvnm-expandable').removeClass('rvnm-collapseable');
                }


                // add collapseable class to parent of link and remove expandable
                $(this).parent().addClass('rvnm-collapseable').removeClass('rvnm-expandable');
                // slide down first level ul 
                $(this).parent().find('> ul').slideDown(300, function () {
                    // then use size triger
                    self.sizetrigger();
                });
                // if href is # link should not be work
                if ($(this).attr('href') === '#') {
                    return false;
                }
            });

            $(document).on('keyup mouseup change', '.rvnm-search', function (e) {
                var word = $(this).val();
                if (word.length == 0) {
                    $(this).closest('ul').find('> li').show();
                } else {
                    $(this).closest('ul').find('> li').each(function () {
                        if (!$(this).hasClass('search')) {
                            $(this).show();
                            var txt = $(this).text();
                            if (txt.indexOf(word) == -1) {
                                $(this).hide();
                            }
                        }
                    });
                    self.sizetrigger();
                }
            });


            // add click event to collapseable link 
            $(document).on('click', '.rvnm-collapseable > a', function (e) {
                // check click only this element
                if (e.target !== e.currentTarget)
                    return false;
                // add expandable class to parent of link and remove collapseable
                $(this).parent().addClass('rvnm-expandable').removeClass('rvnm-collapseable');
                // slide up first level ul of this
                $(this).parent().find('> ul').slideUp(300, function () {
                    self.sizetrigger();
                });

                // if href is # link should not be work
                if ($(this).attr('href') === '#') {
                    return false;
                }
            });


            // click an nav box when has rvnm-mobile class
            $(document).on('click', '.rvnm-mobile', function (e) {
                if (e.target !== e.currentTarget)
                    return false;
                // try to expand menu
                $(this).toggleClass('rvnm-mobile-expand');
            });

            // on mouseenter when menu is minimal 
            $(document).on('mouseenter', '.rvnm-navbar-box.rvnm-minimal  li', function (e) {
                // if menu is first level li 
                if ($(this).closest('.rvnm-minimal-expand').length === 0) {
                    // show menu
                    $(this).addClass('rvnm-minimal-expand');
                }
            });
            // on mouseleave when menu is minimal 
            $(document).on('mouseleave', '.rvnm-navbar-box.rvnm-minimal  li.rvnm-minimal-expand', function (e) {
                $(".rvnm-minimal-expand .rvnm-collapseable ul").slideUp();
                $(".rvnm-minimal-expand .rvnm-collapseable").addClass('rvnm-expandable').removeClass('rvnm-collapseable');
                $(this).removeClass('rvnm-minimal-expand');
            });

            $(window).load(function () {
                setTimeout(function () {
                    self.sizetrigger();
                }, 100);
            });

        });

        return {
            settings: settings,
            setMode: function (mode) {
                $(settings.wrapper).removeClass('rvnm-mobile');
                $(self).removeClass('rvnm-mobile');
                $(settings.wrapper).removeClass('rvnm-minimal');
                $(self).removeClass('rvnm-minimal');
                settings.responsive = false;
                settings.mode = mode;

                if (mode === 'default') {
                    return true;
                }
                if (mode === 'minimal') {
                    $(settings.wrapper).addClass('rvnm-minimal');
                    $(self).addClass('rvnm-minimal');
                    return true;
                }
                if (mode === 'mobile') {
                    $(settings.wrapper).addClass('rvnm-mobile');
                    $(self).addClass('rvnm-mobile');
                    return true;
                }
            },
            setTheme: function (theme) {
                $(self).removeClass('dark');
                $(self).removeClass('dark-lesb');
                $(self).removeClass('dark-doder');
                $(self).removeClass('dark-beryl');
                $(self).removeClass('dark-ruby');
                $(self).addClass(theme);
                settings.theme = theme;
            },
            $this: this
        };


    };

}(jQuery));