odoo.define('product_warranty.warranty_website', function(require){
'use strict';

var PublicWidget = require('web.public.widget');
var ajax = require('web.ajax');

PublicWidget.registry.WarrantyRequest = PublicWidget.Widget.extend({
    selector: '.container',
    events: {
        'change #invoice_ids': '_onInvoiceChange',
        'change #product_ids': '_onProductChange',
    },

    _onInvoiceChange: function(){
        var invoice_id=$('#invoice_ids').val()
        ajax.jsonRpc('/warranty/product','call',{
            'invoice_id': invoice_id,

        })
        .then(function(data){
        var product_ids = $('#product_ids')
        var partner_id = $('#partner_id')

        product_ids.empty()
        $('#partner_id').val(data['partner_name'])
        $('#purchase_date').val(data['invoice_date'])

        for (let i in data['product_name']){
        product_ids.append(`<option selected="selected" hidden="hidden" value="default">choose product</option><option value = "${data['product_ids'][i]}">`+data['product_name'][i]+`</option>`)
        }
        })
    },
    _onProductChange: function(){
        var product_id = $('#product_ids').val()
        var invoice_date = $('#purchase_date').val()

        ajax.jsonRpc('/change/product','call',{
        'product_id':product_id,
        'invoice_date':invoice_date
        })
        .then(function(data){
        var lot_serial = $('#lot_serial')
        var expire_date = $('#expire_date')
        lot_serial.empty()
        for (let i in data['lot_serial']){
        lot_serial.append(`<option value = "${data['lot_id'][i]}">`+data['lot_serial'][i]+`</option>`)
        }
        $('#expire_date').val(data['expire_date'])

        })

    }

    })
})