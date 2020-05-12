var map = L.map('map').setView([79.4, -134.6], 4);

var hash = new L.Hash(map);

L.tileLayer("tiles/{z}|{x}|{y}.png", {
  maxZoom: 17,
  tileSize: 256,
  zoomOffset: -1
}).addTo(map);

var div = document.getElementById("map");

function getTile(c) {
  //console.log(c)
  var url = "tiles/{Z}|{X}|{Y}.png"
    .replace("{Z}", c.zoom)
    .replace("{X}", c.column)
    .replace("{Y}", c.row)

  //console.log(url)
  return url;
}

function textLayer() {
  var layer = po.layer(load);

  function load(tile, projection) {

    d3.json(`/tilemeta/${tile.zoom}|${tile.column}|${tile.row}`, function(json) {

      console.log(tile, projection)
      projection = projection(tile).locationPoint;

      // Add an svg:g for each station.
      var g = d3.select(tile.element = po.svg("g")).selectAll("g")
          .data(d3.entries(json))
        .enter().append("svg:g")
          .attr("transform", transform);

      for (textinfo of json) {
        // Add a circle.
        g.append("svg:circle")
            .attr("r", 4.5);

        // Add a label.
        g.append("svg:text")
            .attr("x", 7)
            .attr("dy", ".31em")
            .text(function(d) { return d.text; });
        }

      function transform(d) {
        var latlon = xy2coords(d.x, d.y, d.z);
        d = projection({lon: latlon.lon, lat: latlon.lat});
        return "translate(" + d.x + "," + d.y + ")";
      }

    });

  }

  return layer;
}

map.on("move", function() {
  // get the current zoom
  //var z = map.zoom();
  // show/hide parcels
  //parcels.visible(z >= 16);
  //console.log(z)
});

lastmouse = {};

$(div).mousedown(function(e) {
  lastmouse = e;
});

var originalWidth = 32768;
var originalHeight = 32768;

var tilesize = 256

// todo use locate for exploration?

const latlngToTilePixel = (latlng, crs, zoom, tileSize, pixelOrigin) => {
    const layerPoint = crs.latLngToPoint(latlng, zoom).floor()
    const tile = layerPoint.divideBy(tileSize).floor()
    const tileCorner = tile.multiplyBy(tileSize).subtract(pixelOrigin)
    const tilePixel = layerPoint.subtract(pixelOrigin).subtract(tileCorner)

    return [tile, tilePixel]
}


$(div).mouseup(function(e) {

  // prevent drag actions from opening links
  if (e.clientX == lastmouse.clientX && e.clientY == lastmouse.clientY) {

    var latlon = map.mouseEventToLatLng(e);
    console.log(latlon)
    var coords = latlngToTilePixel(latlon, map.options.crs, map.getZoom()+1, tilesize, map.getPixelOrigin())
    var mx = (coords[0].x*tilesize+coords[1].x)/Math.pow(2, map.getZoom()-1)/256*originalWidth;
    var my = (coords[0].y*tilesize+coords[1].y)/Math.pow(2, map.getZoom()-1)/256*originalHeight;


	console.log(mx, my);

    $.get("/getmouse", {x:mx, y:my}, function(data) {
      console.log(data)
      var win = window.open('https://en.wikipedia.org/wiki/'+data, '_blank');
      if (win) {
          //Browser has allowed it to be opened
          win.focus();
      } else {
          //Browser has blocked it
          alert('Please allow popups for this website');
      }
    })
  }

});

function xy2coords(x, y, z) {
  var x01 = x/originalWidth;
  var y01 = y/originalHeight;

  var zoomMultiplier = Math.pow(2, z-1);

  var column = x01*zoomMultiplier;
  var row = y01*zoomMultiplier;

  //console.log(column, row);

  var cl = map.coordinateLocation({column, row, zoom:z});
  //console.log(cl);
  //var point = map.locationPoint(cl);

  return cl;
}

$("#searchsubmit").click(function() {
  //console.log("Click")
  $.get("/search", {"search": $("#searchinput").val()}, function(data) {
    //console.log(data)
    var latlon = xy2coords(data.x, data.y, data.z);
    //console.log(latlon);
    map.center(latlon);
    map.zoom(data.z);
  })
})

$("#searchinput").autocomplete({
  minLength: 3,
  appendTo: $("#appendto"),
  position: { my: "left bottom", at: "left top", collision: "flip" },
  source: "/suggest"
})
