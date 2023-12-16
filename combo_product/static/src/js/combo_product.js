/** @odoo-module **/
import ProductScreen from 'point_of_sale.ProductScreen';
import { useListener } from "@web/core/utils/hooks";
import { PosGlobalState } from 'point_of_sale.models';
import Registries from 'point_of_sale.Registries';
import { Gui } from 'point_of_sale.Gui';


const ComboProduct  = (ProductScreen) => class ComboProduct extends ProductScreen {

    //------------show pop up when product with combo products are clicked --------------
    async _clickProduct(event) {
        var product = event.detail.display_name
        var combo_id = event.detail.combo_ids
        if (event.detail.combo_ids[0] != undefined){
            Gui.showPopup("ComboPos", {
                    title: this.env._t('POS Employee'),
                    cancelText: this.env._t("Cancel"),
                    confirmText:this.env._t("Confirm"),
                    body:product,
                    product_detail :event.detail,
                    combo_id:combo_id,
            });
    }
    else{
        super._clickProduct(...arguments);
    }
    }
//    --------------------------------------------------------------
}

Registries.Component.extend(ProductScreen, ComboProduct);