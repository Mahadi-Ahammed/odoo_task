/** @odoo-module */
/*global L*/
import { Component, xml,useRef, useEffect  } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";


export class MapViewWidget extends Component {
    static template = "test_prec.MapViewWidget";
    static props = {
        ...standardWidgetProps,
        latField: { type: String },
        lonField: { type: String },
    };
    setup() {
        // this.state = useState({
        //     latitude: this.props.record.data[this.props.latField],
        //     longitude: this.props.record.data[this.props.lonField],
        // });
        // this.latitude = this.props.record.data[this.props.latField];
        // this.longitude = this.props.record.data[this.props.lonField];
        // const offset = 0.01;
        // // const lon = this.longitude - offset;
        // // const lat = this.latitude;
        // this.bbox = `${this.longitude - offset},${this.latitude - offset},${this.longitude + offset},${this.latitude + offset}`;
        this.mapRef = useRef("map");
        this.leafletMap = null;
        this.markers = [];
        useEffect(() => {
            this.leafletMap = L.map(this.mapRef.el, {
                zoom: 13,
                center: [this.props.record.data[this.props.latField], this.props.record.data[this.props.lonField]]
            });
            this.leafletMap.attributionControl.setPrefix(
                '<a href="https://leafletjs.com" title="A JavaScript library for interactive maps">Leaflet</a>'
            );
            L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: "&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>"
            }).addTo(this.leafletMap);
            L.marker([this.props.record.data[this.props.latField], this.props.record.data[this.props.lonField]]).addTo(this.leafletMap);
            return () => {
                this.leafletMap.remove();
            }
        }, 
        () => [this.props.record.data[this.props.lonField], this.props.record.data[this.props.latField]]);
    }
}
export const mapViewWidget = {
    component: MapViewWidget,
    extractProps: ({ attrs }) => ({
        latField: attrs.latField || "latitude",
        lonField: attrs.lonField || "longitude",
    }),
    additionalClasses: ["o_map_view_widget"],
}

registry.category("view_widgets").add("map_view_widget", mapViewWidget);
