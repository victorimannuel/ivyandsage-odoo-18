import { _t } from '@web/core/l10n/translation';
import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from '@web/core/network/rpc';

publicWidget.registry.WebsiteSaleCheckout.include({
    events: Object.assign({}, publicWidget.registry.WebsiteSaleCheckout.prototype.events, {
        'change [name="scheduled_delivery_date"]': '_setDeliveryDate',
    }),
    
    async _setDeliveryDate(ev) {
        console.log(ev);
        let date = ev.target.value;
        return await rpc('/website_sale/set_delivery_date', {'date': date});
    },
});