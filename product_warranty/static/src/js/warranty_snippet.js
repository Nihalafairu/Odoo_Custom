odoo.define('product_warranty.warranty_snippet', function(require){
console.log("first")
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;
    var Dynamic = PublicWidget.Widget.extend({

        selector: '.dynamic_snippet_warranty',
        events: {
        'click #add_to_cart_warranty': '_addToCart',
        },
        start: function (){
            var self = this;
            rpc.query({
                route: '/warranty/snippet',
                params: {},

        }).then(function (result){
        var chunks = _.chunk(result, 4)
        console.log(chunks)
        chunks[0].is_active = true
        this.$('#courosel').html(
        qweb.render('website_warranty_snippet', {
        chunks
        })
        )

        })
        },
        _addToCart: function(e){
         var product_id = e.target.getAttribute('data-id')
            rpc.query({
            route:"/shop/cart/update_json",
            params:{
            force_create : true,
            product_id: parseInt(product_id),
            add_qty: 1,
            }

        }).then(function(data){
        })

        }
    })
    PublicWidget.registry.dynamic_snippet_warranty = Dynamic;
    return Dynamic;
})