import { ChatWindow } from "@mail/core/common/chat_window";
import { Component, toRaw, useChildSubEnv, useRef, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(ChatWindow.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
    },
    async close(options) {
        const chat_window = toRaw(this.props.chatWindow);
        const thread = this.thread;
        // this.orm.call("discuss.channel", "remove_message", [thread.id]);
        const messages = thread.messages;
        // thread.messages.delete(messages);
        messages.forEach(message => {
            message.remove();
        });
        super.close(...arguments);
    }
});