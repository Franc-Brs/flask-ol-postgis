var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        //source: new ol.source.OSM()
        source: new ol.source.Stamen({
            layer: 'toner',
          })
      }),
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([0, 0]),
      zoom: 0
    })
});

/*
var layer = new ol.layer.Vector({
    source: new ol.source.Vector({
        features: [
            new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([0, 0])),
                name: 'Null Island - just test popup',
            })
        ]
    })
});
map.addLayer(layer);
*/
// Pop-up
const element = document.getElementById('popup');

const popup = new ol.Overlay({
  element: element,
  positioning: 'bottom-center',
  stopEvent: false,
});
map.addOverlay(popup);

// display popup on click
map.on('click', function (evt) {
  const feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
    return feature;
  });
  if (feature) {
    //popup.setPosition(evt.coordinate);
    popup.setPosition(evt.coordinate);
    $(element).popover({
      placement: 'top',
      html: true,
      content: feature.get('name')? feature.get('name') :"no-name for this feature",
    });
    $(element).popover('show');
  } else {
    $(element).popover('dispose');
  }
});

// Close the popup when the map is moved
map.on('movestart', function () {
  $(element).popover('dispose');
});
