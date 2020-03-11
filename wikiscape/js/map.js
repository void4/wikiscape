var po = org.polymaps;

var div = document.getElementById("map");

function getTile(c) {
  //console.log(c)
  var url = "tiles/{Z}-{X}-{Y}.png"
    .replace("{Z}", c.zoom)
    .replace("{X}", c.column)
    .replace("{Y}", c.row)

  //console.log(url)
  return url;
}

var layer = po.image().url(getTile);

var map = po.map()
    .container(div.appendChild(po.svg("svg")))
    .zoomRange([0,11])
    .zoom(1)
    .add(layer);
          //.tileSize({x: 256, y: 256});


map.add(po.interact())
.add(po.hash());


map.on("move", function() {
  // get the current zoom
  var z = map.zoom();
  // show/hide parcels
  //parcels.visible(z >= 16);
  //console.log(z)
});

lastpage = null;
lastmouse = {};

$(div).mousedown(function(e) {
  lastmouse = e;
});

$(div).mouseup(function(e) {

  // prevent drag actions from opening links
  if (e.clientX == lastmouse.clientX && e.clientY == lastmouse.clientY) {
    if (lastpage !== null) {
      var win = window.open('https://en.wikipedia.org/wiki/'+lastpage, '_blank');
      if (win) {
          //Browser has allowed it to be opened
          win.focus();
      } else {
          //Browser has blocked it
          alert('Please allow popups for this website');
      }
    }
  }
});

$(div).mousemove(function(e) {

  // Get column, row and zoom level of mouse position
  var crz = map.locationCoordinate(map.pointLocation(map.mouse(e)));

  // Normalize the column and row values to the 0..1 range
  var zoomMultiplier = Math.pow(2, crz.zoom-1);

  var x01 = crz.column/zoomMultiplier;
  var y01 = crz.row/zoomMultiplier;

  // Multiply with the original image width and height
  var originalWidth = 32768;
  var originalHeight = 32768;

  var mx = x01*originalWidth;
  var my = y01*originalHeight;

  // Now we have the mouse coordinates on the original image!
  //console.log(mx, my);

  $.get("/getmouse", {x:mx, y:my}, function(data) {
    console.log(data)
    lastpage = data;
  })
})
