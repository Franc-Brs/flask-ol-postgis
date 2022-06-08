//style
var styles = {
    Point: new ol.style.Style({
      image: new ol.style.Circle({
        radius: 1,
        stroke: new ol.style.Stroke({
          color: "rgba(17,158,76,0.8)", //#F3C35D
          width: 15
        })
      })
    })
};

var styleFunction = function(feature) {
    return styles[feature.getGeometry().getType()];
};

// soruce for the layer
var vectorSource = new ol.source.VectorSource({
    format: new ol.format.GeoJSON(),
    loader: vectorLoader,
    projection: "EPSG:4326"
});

//call to the endpoint
axios.get('http://localhost:5000/points')
    .then(response => {
        console.log(response.data)
        //L.geoJSON(response.data, {}).addTo(map);
        const vectorSource = new ol.source.Vector({
            features: new ol.format.GeoJSON().readFeatures(response.data),
        });
})