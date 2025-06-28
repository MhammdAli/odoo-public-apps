import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
export class MailIconSystray extends Component {
    static template = "mail_icon_systray";
    setup() {
        this.action = useService("action");
    }

    openMailComposer() {
        this.action.doAction("mail.action_email_compose_message_wizard");
    }
}

registry.category("systray").add(
    "mailIconSystray",
    { Component: MailIconSystray }
    // {
    //     sequence: 24,
    // }
);
