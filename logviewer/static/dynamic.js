var local_uri_prefix = "./";
if (typeof(KISMET_URI_PREFIX) !== 'undefined')
local_uri_prefix = KISMET_URI_PREFIX;
var kismet_ui_adsb;
var kismet_ui_bluetooth;
var kismet_ui_btle;
var kismet_ui_datasources;
var kismet_ui_dot11;
var kismet_ui_meter;
var kismet_ui_rtl433;
var kismet_ui_uav;
var kismet_ui_zwave;
async function load_dynamics() {
kismet_ui_adsb = await import(`${local_uri_prefix}js/kismet.ui.adsb.js`);
kismet_ui_bluetooth = await import(`${local_uri_prefix}js/kismet.ui.bluetooth.js`);
kismet_ui_btle = await import(`${local_uri_prefix}js/kismet.ui.btle.js`);
kismet_ui_datasources = await import(`${local_uri_prefix}js/kismet.ui.datasources.js`);
kismet_ui_dot11 = await import(`${local_uri_prefix}js/kismet.ui.dot11.js`);
kismet_ui_meter = await import(`${local_uri_prefix}js/kismet.ui.meter.js`);
kismet_ui_rtl433 = await import(`${local_uri_prefix}js/kismet.ui.rtl433.js`);
kismet_ui_uav = await import(`${local_uri_prefix}js/kismet.ui.uav.js`);
kismet_ui_zwave = await import(`${local_uri_prefix}js/kismet.ui.zwave.js`);
}
