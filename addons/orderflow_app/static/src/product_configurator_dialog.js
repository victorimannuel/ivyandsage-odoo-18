import { _t } from '@web/core/l10n/translation';
import { patch } from '@web/core/utils/patch';
import { useSubEnv } from '@odoo/owl';
import {
    ProductConfiguratorDialog
} from '@sale/js/product_configurator_dialog/product_configurator_dialog';


patch(ProductConfiguratorDialog.prototype, {
    setup() {
        super.setup(...arguments);
        useSubEnv({
            showQuantityAndPrice: this.props.options?.showQuantityAndPrice ?? false,
        });
    },
});