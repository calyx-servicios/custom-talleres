odoo.define('custom_ed.custom', function (require) {
    "use strict";

    var core = require('web.core');
    var rpc = require('web.rpc');
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    
    var ajax = require('web.ajax');
    
    var concurrency = require('web.concurrency');
    var field_utils = require('web.field_utils');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var time = require('web.time');
    var utils = require('web.utils');

    var QWeb = core.qweb;
    var _t = core._t;
    var Mutex = concurrency.Mutex;
    var round_di = utils.round_decimals;
    var round_pr = utils.round_precision;

    var exports = {};


    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        

        set_table: function(table) {
            if (table){
                if (this.order_to_transfer_to_different_table) {
                    this.order_to_transfer_to_different_table.add_new_transfer(
                        new exports.Transferline ({}, {
                            pos: this.pos, 
                            order: this.order_to_transfer_to_different_table, 
                            source:this.order_to_transfer_to_different_table.table, destiny:table}));
                    
                }
            }
            
            return  _super_posmodel.set_table.call(this,table);
        },
    });

        
    exports.Transferline = Backbone.Model.extend({
        initialize: function(attributes, options) {
            this.pos = options.pos;
            this.order = options.order;
            this.source = options.source;
            this.destiny = options.destiny;
            
            if (options.json) {
                this.init_from_JSON(options.json);
                return;
            }
        },
        init_from_JSON: function(json){
            
            this.source = this.pos.tables_by_id[json.source_id];
            this.destiny = this.pos.tables_by_id[json.destiny_id];
        },
        
        export_as_JSON: function(){
            return {
                source_id: this.source.id,
                destiny_id: this.destiny.id,
                
            };
        },
        
    });

    var TransferlineCollection = Backbone.Collection.extend({
        model: exports.Transferline,
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
    initialize: function(){
        if (!this.transfers){
            this.transfers = new TransferlineCollection();
            this.transfers.on('change', function(){ this.save_to_db("transfers:change"); }, this);
            this.transfers.on('add',    function(){ this.save_to_db("transfers:add"); }, this);
            this.transfers.on('remove', function(){ this.save_to_db("transfers:rem"); }, this);
        }
        
        _super_order.initialize.apply(this,arguments);
        this.save_to_db();
        
    },
    remove_transfer: function( transfer ){
        this.assert_editable();    
        this.transfers.remove(transfer);
    },

    add_new_transfer: function(transfer){
        this.assert_editable();
        this.transfers.add(transfer);
        
    },
    init_from_JSON: function(json) {
        _super_order.init_from_JSON.apply(this,arguments);
        
        
        var transfers = json.transfer_ids;
        if (transfers){
            for (var i = 0; i < transfers.length; i++) {
                var transfer = transfers[i][2];
                var new_transfer = new exports.Transferline({},{pos: this.pos, order: this, json: transfer});
                this.add_new_transfer(new_transfer);
            }
        }
    
    },
    export_as_JSON: function() {
        var json=_super_order.export_as_JSON.apply(this,arguments);

        
        if (this.transfers){
            var transferLines;
            transferLines = [];
            this.transfers.each(_.bind( function(item) {
                if (item.destiny && item.source){
                    if (item.destiny!=item.source){
                        return transferLines.push([0, 0, item.export_as_JSON()]);
                    }
                    
                }
                
            }, this));
            json.transfer_ids=transferLines
            
        }
        return json

       
    },

    });

    
});