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
      projection: 'EPSG:4326',
      center: ol.proj.fromLonLat([0, 0]),
      zoom: 0
    })
});