odoo.define('product_owner.receipt-lines', function (require) {
"use strict";
  var { Orderline } = require('point_of_sale.models');
  const Registries = require('point_of_sale.Registries');

const OwnerInOrderline = (Orderline) => class OwnerInOrderline extends Orderline {
    export_for_printing() {
        var line = super.export_for_printing(...arguments);
            var product_owner=this.get_product().owner_id
            line.product_owner=product_owner
        return line;
    }

}
Registries.Model.extend(Orderline, OwnerInOrderline);

});