/* @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

var registry = publicWidget.registry;

registry.AddReview = publicWidget.Widget.extend({
    selector: '.property-detail-section',
    events: {
        "click #saveReview": "_onSaveReview",
        "click .star-rating .star": "_onStarClick",
    },

    init() {
        this._super.apply(this, arguments);
        this.notification = this.bindService("notification");
    },

    _onStarClick: function (ev) {
        ev.preventDefault();
        let rating = parseInt($(ev.currentTarget).data("value"), 10);
        // Set value in the hidden input
        this.$("#review_rating").val(rating);
        // Highlight the stars accordingly
        this.$(".star-rating .star").each(function () {
            let currentValue = parseInt($(this).data("value"), 10);
            if (currentValue <= rating) {
                $(this).removeClass("text-muted").addClass("text-warning");
            } else {
                $(this).removeClass("text-warning").addClass("text-muted");
            }
        });
    },

    _onSaveReview: function (ev) {
        ev.preventDefault();
        // Retrieve the comment from the textarea
        let $textarea = this.$("#review_comment_text");
        // let $propUser = this.$("#current_prop_user");
        let comment = parseInt($textarea.val().trim(), 10) || $textarea.val().trim();
        if (!comment) {
            this.notification.add("Please enter a comment", { type: "warning" });
            return;
        }

        // Retrieve property id and user id from the button's data attributes
        let $button = this.$("#saveReview");
        let propertyId = $button.data("curr_prop_id");
        let rating = parseInt(this.$("#review_rating").val(), 10) || 0;
        let propertyUserId = $button.data("curr_prop_user");
        if (!propertyUserId) {
            this.notification.add("User must need to be logged in as property user", { type: "warning" });
        }
        rpc("/property/submit_review", {
            property_id: propertyId,
            property_user_id: propertyUserId,
            comment: comment,
            rating : rating
        }).then((result) => {
            if (result.success){
                location.reload();
            }
            
        }).catch((error) => {
            console.error("Error saving review:", error);
        });
    },
});
