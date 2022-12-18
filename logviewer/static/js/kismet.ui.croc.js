(
  typeof define === "function" ? function (m) { define("kismet-ui-croc-js", m); } :
  typeof exports === "object" ? function (m) { module.exports = m(); } :
  function(m){ this.kismet_ui_croc = m(); }
)(function () {

"use strict";

var exports = {};

// Flag we're still loading
exports.load_complete = 0;

/* Highlight rtl devices */
kismet_ui.AddDeviceRowHighlight({
    name: "EFF CROC",
    description: "EFF CROC",
    priority: 100,
    defaultcolor: "#ffb3cc",
    defaultenable: true,
    fields: [
        'kismet.device.base.phyname'
    ],
    selector: function(data) {
        return data['kismet.device.base.phyname'] === "CROC";
    }
});

kismet_ui.AddDeviceDetail("croc", "EFF CROC", 0, {
    filter: function(data) {
        return (data['kismet.device.base.phyname'] === "CROC");
    },
    draw: function(data, target) {
        target.devicedata(data, {
            "id": "crocData",
            "fields": [
            {
                field: "croc.device/croc.device.common/croc.device.mcc",
                title: "MCC",
                empty: "<i>Unknown</i>"
            },
            {
                field: "croc.device/croc.device.common/croc.device.mnc",
                title: "MNC",
                empty: "<i>Unknown</i>"
            },
            {
                field: "croc.device/croc.device.common/croc.device.tac",
                title: "TAC",
                filterOnZero: true,
            },
            {
                field: "croc.device/croc.device.common/croc.device.cid",
                title: "CID",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.phyid",
                title: "PHYID",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.earfcn",
                title: "EARFCN",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.rssi",
                title: "RSSI",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.frequency",
                title: "Frequency",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.enodeb_id",
                title: "ENODEB ID",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.sector_id",
                title: "Sector ID",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.cfo",
                title: "CFO",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.rsrq",
                title: "RSRQ",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.snr",
                title: "SNR",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.rsrp",
                title: "RSRP",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.tx_pwr",
                title: "TX Power",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.raw_sib1",
                title: "Raw SIB1",
                filterOnEmpty: true,
            },
           {
                field: "croc.device/croc.device.common/croc.device.timestamp",
                title: "Timestamp",
                filterOnEmpty: true,
            },
            ],
        });
    },
});

// We're done loading
exports.load_complete = 1;

return exports;

});
