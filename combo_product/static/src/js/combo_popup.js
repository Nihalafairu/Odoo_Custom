/** @odoo-module **/
import { Gui } from 'point_of_sale.Gui';
import { useListener } from "@web/core/utils/hooks" ;
import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
import Registries from 'point_of_sale.Registries';
import { _t } from 'web.core';
import rpc from 'web.rpc';
import { parse } from 'web.field_utils';
import { Component, useState,useRef, onMounted} from "@odoo/owl";
import { Orderline } from 'point_of_sale.models';

class ComboPos extends AbstractAwaitablePopup {
    setup() {

        this.root = useRef("comboDetails")

        this.state = useState({
        required_categ :{},
        optional_categ :{},
        count :{},
        product_id : [],
        product_name : [],
        select_pro : false
        })

        onMounted(() => {
        this.click_combo();
        })
        super.setup();
    }
//    -------------pop up details ----------------------------------------------
    click_combo(){
        var self = this
        var combo_id = this.props.combo_id
        var combo_details = rpc.query({
            model:'pos.combo',
            method:'get_combo_details',
            args:[combo_id]
        }).then(function(result){
        var li_re={}
        var li_op={}
        var count={}
        var id = []
        for(var j in result['required']){
            li_re[result['required'][j]['category_id']]= result['required'][j]['product']
        }
        for(var i in result['optional']){
            li_op[result['optional'][i]['category_id']]= result['optional'][i]['product']
            id[result['optional'][i]['id']] = result['optional'][i]['id']
            count[result['optional'][i]['category_id']]= result['optional'][i]['count']
        }

        self.state.product_id['id'] = id
        self.state.required_categ['required'] = li_re
        self.state.optional_categ['optional'] = li_op
        self.state.count['category'] = count

        })
        }
//      ------------------ show ribbon to optional products when selected ------------------------------------------------
    async showRibbon(data,count){
        var self = this
        var index = self.state.product_name.indexOf(data)

        if (self.state.product_name.includes(data) ){
            self.state.product_name.splice(index, 1)
        }
        else{
            self.state.product_name.push(data)
        }
        var selected_count = self.state.product_name.length
        if (selected_count > count && count != 0){
            this.showPopup('ErrorPopup', {
                                            title: this.env._t('Product limit exceeds'),
                                            body: this.env._t('Choose  only ' + count + '  product'),
                                        });
            self.state.product_name.splice(index, 1)
        }

        }
//    --------------combo products added to order line -------------------------------------------------------
    confirmOrder(data){
        var self = this
        var combo_products = []
        var optional = []
        for(var i in self.state.required_categ['required']){
        for(var j in self.state.required_categ['required'][i]){
        combo_products.push(j)
        }
        }
        for(var name in self.state.product_name){
        optional.push(self.state.product_name[name])
        }
        var product = self.props.product_detail

        product['combo_pro'] = combo_products
        product['optional'] = optional
        var order = self.env.pos.get_order();
        order.add_product(product)
        order.selected_orderline.customerNote="Combo Products"
        self.confirm()

    }

//    -----------------------------------------------------------------------
    }
        ComboPos.template = 'ComboPos';
        ComboPos.defaultProps = {
            confirmText: 'Confirm',
            cancelText: 'Cancel',
            title: 'Assign Sales Person',
            body: '',
        };
Registries.Component.add(ComboPos);
return ComboPos;


