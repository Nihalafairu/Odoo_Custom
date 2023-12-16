odoo.define('combo_product.receipt-lines', function (require) {
"use strict";
  var { Orderline } = require('point_of_sale.models');
  const Registries = require('point_of_sale.Registries');

const  ComboInOrderline = (Orderline) => class ComboInOrderline extends Orderline {
    export_for_printing() {
        var line = super.export_for_printing(...arguments);
            var combo=this.product.combo_pro
            if(combo != undefined){
            line.combo_products = combo
            }

            var optional = this.product.optional
            if (optional != undefined){
            line.optional = optional
            }
        return line;
    }

}
Registries.Model.extend(Orderline, ComboInOrderline);

});