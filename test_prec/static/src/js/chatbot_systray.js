import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { user } from "@web/core/user";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";


export class ChatbotSystray extends Component {
    static template = "test_prec.ChatbotSystray";
    static components = { ChatbotSystray };
    static props = [];

    setup() {
        this.store = useService("mail.store");
        this.userId = user.userId;
        this.orm = useService("orm");
        onMounted(async () => {
            var self = this;
            this.chatbotChannel = await this.orm.call("chat.bot", "search_odoobot_channel", []);
            if (this.chatbotChannel){
                this.channels = await this.store.channels.fetch();
                if (this.chatbotChannel){
                    this.thread = this.store.Thread.get({
                        id:  this.chatbotChannel,
                        model: "discuss.channel",
                    });
        }
            }
        });
    }
    openChatbot(){
        // this.channels = this.store.channels.fetch();
        // if (this.chatbotChannel){
        //     this.thread = this.store.Thread.get({
        //         id:  this.chatbotChannel,
        //         model: "discuss.channel",
        //     });
        // }
        if (this.thread){
            this.thread.open();
            this.foldStateCount = this.thread.foldStateCount
        }
        // const channel_id = rpc(
        //     "/discuss/channel/fold",
        //     {
        //         channel_id: this.chatbotChannel,
        //         state: "open",
        //         state_count: this.foldStateCount,
        //     },
        //     { shadow: true }
        // )

    }
}
registry.category("systray").add("chatbot_systray", {
    Component: ChatbotSystray,
    props: {},
    template: "test_prec.ChatbotSystray",
    isDisplayed: () => true,
    sequence: 10,
});