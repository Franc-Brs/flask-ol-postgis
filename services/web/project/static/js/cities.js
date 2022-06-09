// Style of points layer

const styles = {
  'Point': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({color: 'rgba(255,0,0,30)',}),
      stroke: new ol.style.Stroke({color: 'red', width: 1}),
    })
  })
};

const styleFunction = function (feature) {
  return styles[feature.getGeometry().getType()];
};

// define api-call 

const retrievData = async () => {
  try {
    const res = await axios.get('http://localhost:5000/points_geom');
    return res;
  } catch(error) {
    console.log(error);
    return null;
  }
}

// Retrieve the data

(async () => {

  const response = await retrievData()

  const vectorSource = new ol.source.Vector({
    features: new ol.format.GeoJSON().readFeatures(response.data),
  });

  const vectorLayer = new ol.layer.Vector({
    source: vectorSource,
    style: styleFunction,
  });
  
  map.addLayer(vectorLayer);
})()