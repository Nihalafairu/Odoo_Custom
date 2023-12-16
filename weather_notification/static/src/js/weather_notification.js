/** @odoo-module **/
import { registry } from "@web/core/registry";
import core from 'web.core';
import SystrayMenu from 'web.SystrayMenu';
import { Component,useState, onWillStart } from "@odoo/owl";
import Widget from 'web.Widget';
import rpc from 'web.rpc';
var qweb = core.qweb
class SystrayIcon extends Component {
    setup() {
    this.state = useState({
        weather:null,
        api_keys:null,
        temp:null,
        humidity:null,
        place:null,
        main:null,
        icon:null,
        city:null,
    })

    var self = this
    var settings = await rpc.query({
        model:'res.config.settings',
        method:'conf_details'
    })
    .then(function(result){
    self.state.weather = result['weather']
    self.state.city = result['city']
    self.state.api_keys = result['api_keys']

    });
    })
    }
    _onClick(ev){
        var self = this
        if  (!this.state.city){
            if (navigator.geolocation){
                navigator.geolocation.getCurrentPosition(successFunction, errorFunction);
            }
            else{
                Dialog.alert(this, _t("It seems like Geolocation, which is required for this page, is not enabled in your browser."));

            }

            function successFunction(position){
            var lat = position.coords.latitude;
            var long = position.coords.longitude;
            var api = "";
            rpc.query({
            model:'res.config.settings',
            method:'search_read'
            })
            .then(function(result){incomingStock
                let api_key = result['api_keys']
                fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${long}&appid=${api_key}`
                )
                .then(response => response.json())
                .then ((data)=>{
                self.state.temp = data['main']['temp']
                self.state.humidity = data['main']['humidity']
                self.state.place = data['name']
                self.state.main = data['weather'][0]['main']
                self.state.icon = data['weather'][0]['icon']
                })
                })
                }
            function errorFunction(position){
            Dialog.alert(this, _t("Error trying to connect to Odoo."));
            }

        }
        else{
            console.log("p")
            var self = this
            var city = self.state.city
            var api_keys = self.state.api_keys
            fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${api_keys}`
            )
            .then(response => response.json())
            .then ((data)=>{
            self.state.temp = data['main']['temp']
            self.state.humidity = data['main']['humidity']
            self.state.place = data['name']
            self.state.main = data['weather'][0]['main']
            self.state.icon = data['weather'][0]['icon']
            })
        }
    }
}
SystrayIcon.template = "IconSystrayDropdown";
export const systrayItem = { Component: SystrayIcon,};
registry.category("systray").add("SystrayIcon", systrayItem);

