odoo.define('discount_tag.receipt-lines', function (require) {
"use strict";
  var { Orderline } = require('point_of_sale.models');
  const Registries = require('point_of_sale.Registries');

const  TagInOrderline = (Orderline) => class TagInOrderline extends Orderline {
    export_for_printing() {
        var line = super.export_for_printing(...arguments);
            var discount_tag=this.get_product().discount
            line.discount_tag=discount_tag
        return line;
    }

}
Registries.Model.extend(Orderline, TagInOrderline);

});