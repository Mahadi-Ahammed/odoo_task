/* @odoo-module */
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

var registry = publicWidget.registry;

registry.PropertyUserProfile = publicWidget.Widget.extend({
    selector: '.profile-section',
    events: {
        "click #saveProfile": "_onSaveProfile",
    },

    init() {
        this._super.apply(this, arguments);
        this.notification = this.bindService("notification");
    },

    _onSaveProfile: function (ev) {
        ev.preventDefault();
        // Collect data from the form
        const $form = this.$("#editProfileForm");
        let formData = {
            user_id: $form.find("input[name='user_id']").val(),
            name: $form.find("input[name='name']").val().trim(),
            email: $form.find("input[name='email']").val().trim(),
            street: $form.find("input[name='street']").val().trim(),
            city: $form.find("input[name='city']").val().trim(),
            zip_code: $form.find("input[name='zip_code']").val().trim(),
            // You can add additional fields for country_id, state_id if needed
        };

        rpc("/bay_vista_user/update_profile", formData)
            .then((result) => {
                if (result.status === "success") {
                    location.reload();
                } else {
                    console.error("Error updating profile:", result.error);
                }
            })
            .catch((error) => {
                console.error("Error updating profile:", error);
            });
    },
});
