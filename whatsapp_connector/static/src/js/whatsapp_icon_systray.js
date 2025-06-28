import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
export class whatsappIconSystray extends Component {
    static template = "whatsapp_icon_systray";
    setup() {
        this.action = useService("action");
    }

    openWhatsapp() {
        this.action.doAction("whatsapp_connector.whatsapp_composer_action");
    }
}

registry.category("systray").add(
    "whatsappIconSystray",
    { Component: whatsappIconSystray }
    // {
    //     sequence: 23,
    // }
);
