odoo.define('pos_limit.PaymentScreen', function(require) {
"use strict";
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const session = require('web.session');

const posPaymentScreen = (PaymentScreen) => class posPaymentScreen extends PaymentScreen {
    async validateOrder() {
        const payment_method = this.env.pos.selectedOrder.selected_paymentline.name
        const partner=this.env.pos.selectedOrder.partner
        if(payment_method == 'Bank'){
        return  super.validateOrder(...arguments);
        }
        if(payment_method == 'Cash'){
        return  super.validateOrder(...arguments);
        }
        if (partner == null){
            this.showPopup('ErrorPopup', {
                                            title: this.env._t('choose customer'),
                                            body: this.env._t('Choose a customer'),
                                        });
        }
        else{
        if (payment_method == 'Customer Account'){
            const partner=this.env.pos.selectedOrder.partner
            var due =  partner.credit
            var limit = partner.limit
            if ((due > limit) && (limit != 0)){
                this.showPopup('ErrorPopup', {
                                        title: this.env._t('Limit Exceeds'),
                                        body: this.env._t('This customer exceeds the limit to purchase'),
                                    });
            }
            else if(limit == 0){
                return  super.validateOrder(...arguments);
            }
        }
        else{
        return  super.validateOrder(...arguments);
        }
}

        }
    }


Registries.Component.extend(PaymentScreen, posPaymentScreen);



});