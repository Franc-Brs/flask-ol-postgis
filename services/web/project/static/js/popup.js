// Pop-up
const element = document.getElementById('popup');

const popup = new ol.Overlay({
  element: element,
  positioning: 'bottom-center',
  stopEvent: false,
});
map.addOverlay(popup);

// display popup on click only for nullIsland layer
map.on('click', function (evt) {
  const feature = map.forEachFeatureAtPixel(evt.pixel, 
    function (feature, layer) {
      if (layer == nullIsland) {
        return feature;
      }
    },
    );
  if (feature) {
    //popup.setPosition(evt.coordinate);
    popup.setPosition(evt.coordinate);
    $(element).popover({
      placement: 'top',
      html: true,
      content: feature.get('name')? feature.get('name') :"no infos for this feature",
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