/** @odoo-module **/
import { useBus, useService } from "@web/core/utils/hooks";
import {registry} from '@web/core/registry';
import { loadJS } from "@web/core/assets";
import rpc from 'web.rpc';
import { Component, useState,useRef, onMounted, onWillStart, onPatched } from "@odoo/owl";
export class InventoryDashboard extends Component {
   setup() {
   this.root = useRef("incomingStock")
   this.root1 = useRef("outgoingStock")
   this.root2 = useRef("productExpense")
   this.root3 = useRef("stockValuation")
   this.root4 = useRef("filter")
   this.root5 = useRef("internalTransfers")

   this.state = useState({
   stock_incoming:null,
   product_name:[],
   quantity:[],
   product_name_out:[],
   quantity_out:[],
   location:{},
   loc_wise_product:[],
   product_exp:[],
   cost:[],
   stock:[],
   qty:[],
   change:null,
   chart_inc:null,
   chart_out:null,
   pro_name:[],
   pro_quant:[]
   })
   onWillStart(async ()=>{
    await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
})

    onMounted(() => {
    this._incoming_stock();
    this._outgoing_stock();
    this._locationWiseStock();
    this._expense_details();
    this._stockValuation();
    this._internalTransfers();

    });
   }
//   --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   _incoming_stock(){

    var self = this
    let arg=0
    var in_stock = rpc.query({
        model:'inventory.dashboard',
        method:'incoming_stock',
        args:[arg]
    })
    .then(function(result){
    $.each(result,function(index,value){
     $.each(value,function(k_index,k_value){
      self.state.product_name.push(k_index)
      self.state.quantity.push(k_value)
    })

    })


   self.state.chart_inc = new Chart(self.root.el, {
    type: 'bar',
    data: {
        labels: self.state.product_name,
        datasets: [{
            label: 'Incoming Stock',
            data:  self.state.quantity ,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    })

     })
     }
//     --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    _outgoing_stock(){
    var self = this
    let arg=0
    var out_stock = rpc.query({
        model:'inventory.dashboard',
        method:'outgoing_stock',
         args:[arg]
    }).then(function(result){
    $.each(result,function(index,value){
     $.each(value,function(k_index,k_value){
      self.state.product_name_out.push(k_index)
      self.state.quantity_out.push(k_value)
    })

    })
    self.state.chart_out = new Chart(self.root1.el, {
    type: 'bar',
    data: {
        labels: self.state.product_name_out,
        datasets: [{
            label: 'Outgoing Stock',
            data:  self.state.quantity_out ,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    })


    })
    }
//    -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    _locationWiseStock(){
    var self = this
    var loc_wise_stock = rpc.query({
        model:'inventory.dashboard',
        method:'location_stock'
    }).then(function(result){
        $.each(result,function(index,value){
            $.each(value,function(ik_index,ik_value){
                if (ik_value != null ){
                    self.state.location[ik_index]=ik_value
                }
            })
        })
    })
    }
//    -----------------------------
    _expense_details(){
    var self = this
    var out_stock = rpc.query({
        model:'inventory.dashboard',
        method:'product_expense'
    }).then(function(result){
    $.each(result,function(index,value){
     $.each(value,function(k_index,k_value){
      self.state.product_exp.push(k_index)
      self.state.cost.push(k_value)
    })

    })
    new Chart(self.root2.el, {
    type: 'line',
    data: {
        labels: self.state.product_exp,
        datasets: [{
            label: 'Product Expense',
            data:  self.state.cost ,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    })


    })
    }
//    --------------------------------------------------------------------------------
    _stockValuation(){
    var self = this
    var out_stock = rpc.query({
        model:'inventory.dashboard',
        method:'stock_valuation'
    }).then(function(result){
    $.each(result,function(index,value){
     $.each(value,function(k_index,k_value){
      self.state.stock.push(k_index)
      self.state.qty.push(k_value)
    })

    })
    new Chart(self.root3.el, {
    type: 'doughnut',
    data: {
        labels: self.state.stock,
        datasets: [{
            label: 'Stock Valuation',
            data:  self.state.qty ,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    })


    })
    }

//    -----------------------------------------------------------------------------------
    onPeriodChange(ev){
    var self = this
    var change=ev.target.value
    self.state.change = ev.target.value
    this.filter_incoming_stock(change);
    this.filter_outgoing_stock(change);
    }
//    ----------------------------------------------------------------------------------------
    filter_incoming_stock(change){
        var self = this
        self.state.chart_inc.destroy()
        self.state.product_name=[]
        self.state.quantity=[]
    var arg=change
    var in_stock = rpc.query({
        model:'inventory.dashboard',
        method:'incoming_stock',
        args:[arg]
    })
    .then(function(result){
    $.each(result,function(index,value){
     $.each(value,function(k_index,k_value){
      self.state.product_name.push(k_index)
      self.state.quantity.push(k_value)
    })
    })

    self.state.chart_inc=new Chart(self.root.el, {
    type: 'bar',
    data: {
        labels: self.state.product_name,
        datasets: [{
            label: 'Incoming Stock',
            data:  self.state.quantity ,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    })



     })
     }
//     -------------------------------------------------------------------------------------------------------
    filter_outgoing_stock(change){
        var self = this
        self.state.chart_out.destroy()
        self.state.product_name_out=[]
        self.state.quantity_out=[]


        var arg=change
        var out_stock = rpc.query({
            model:'inventory.dashboard',
            method:'outgoing_stock',
             args:[arg]
        }).then(function(result){
        $.each(result,function(index,value){
         $.each(value,function(k_index,k_value){
          self.state.product_name_out.push(k_index)
          self.state.quantity_out.push(k_value)
        })

        })
        self.state.chart_out = new Chart(self.root1.el, {
        type: 'bar',
        data: {
            labels: self.state.product_name_out,
            datasets: [{
                label: 'Outgoing Stock',
                data:  self.state.quantity_out ,
                backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(255, 159, 64, 0.2)',
                  'rgba(255, 205, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(201, 203, 207, 0.2)'
                ],
                borderColor: [
                  'rgb(255, 99, 132)',
                  'rgb(255, 159, 64)',
                  'rgb(255, 205, 86)',
                  'rgb(75, 192, 192)',
                  'rgb(54, 162, 235)',
                  'rgb(153, 102, 255)',
                  'rgb(201, 203, 207)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
        })


        })
    }
//   ---------------------------------------------------------------------------------------------------------
    _internalTransfers(){
    var self = this
    var in_stock = rpc.query({
        model:'inventory.dashboard',
        method:'internal_transfers',
    })
    .then(function(result){
     console.log(result)
    $.each(result,function(index,value){
     $.each(value,function(k_index,k_value){
      self.state.pro_name.push(k_index)
      self.state.pro_quant.push(k_value)
    })

    })
    new Chart(self.root5.el, {
    type: 'radar',
    data: {
        labels: self.state.pro_name,
        datasets: [{
            label: 'Internal Transfers',
            data:  self.state.pro_quant ,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
    })

     })
    }
//    ----------------------------------------------------------------------------


}
registry.category("actions").add("custom_dashboard_tags", InventoryDashboard);
InventoryDashboard.template = 'dashboard.InventoryDashboard';