
"use strict";

var local_uri_prefix = ""; 
if (typeof(KISMET_URI_PREFIX) !== 'undefined')
    local_uri_prefix = KISMET_URI_PREFIX;

kismet_ui_tabpane.AddTab({
    id: 'heatmap',
    tabTitle: 'Heat Map',
    expandable: false,
    createCallback: function(div) {
        var url = new URL(parent.document.URL);
        url.searchParams.append('parent_url', url.origin)
        url.searchParams.append('local_uri_prefix', local_uri_prefix);
        url.searchParams.append('KISMET_PROXY_PREFIX', KISMET_PROXY_PREFIX);
        url.pathname = `${local_uri_prefix}${KISMET_PROXY_PREFIX}russ_map_panel.html`;

        div.append(
            $('<iframe>', {
                width: '100%',
                height: '100%',
                src: url.href,
            })
        );
    },
    priority: -100,

}, 'center');

