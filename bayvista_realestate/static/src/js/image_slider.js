/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
var registry = publicWidget.registry;

registry.ImageSlider = publicWidget.Widget.extend({
    selector: '.property-images-container',

    start: function () {
        this._super.apply(this, arguments);
        // Collect all slides
        this.$slides = this.$el.find('.property-image');
        this.currentIndex = 0;
        // Instead of immediate show/hide, fade in the first image.
        this.$slides.hide();
        this.$slides.eq(this.currentIndex).fadeIn(500);  // Transition duration = 500ms
        this._bindEvents();
    },

    _bindEvents: function () {
        var self = this;
        // Bind previous arrow click
        this.$el.parent().find('.slider-prev').on('click', function (e) {
            e.preventDefault();
            self.prevSlide();
        });
        // Bind next arrow click
        this.$el.parent().find('.slider-next').on('click', function (e) {
            e.preventDefault();
            self.nextSlide();
        });
    },

    showSlide: function (index) {
        // Fade out current slide and fade in the new slide
        this.$slides.filter(':visible').fadeOut(500, () => {
            this.$slides.eq(index).fadeIn(500);
        });
    },

    prevSlide: function () {
        this.currentIndex = (this.currentIndex === 0) ? this.$slides.length - 1 : this.currentIndex - 1;
        this.showSlide(this.currentIndex);
    },

    nextSlide: function () {
        this.currentIndex = (this.currentIndex === this.$slides.length - 1) ? 0 : this.currentIndex + 1;
        this.showSlide(this.currentIndex);
    },
});
