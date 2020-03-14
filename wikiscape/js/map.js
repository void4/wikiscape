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
    .zoomRange([0,15])
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

lastmouse = {};

$(div).mousedown(function(e) {
  lastmouse = e;
});

var originalWidth = 32768;
var originalHeight = 32768;

$(div).mouseup(function(e) {

  // prevent drag actions from opening links
  if (e.clientX == lastmouse.clientX && e.clientY == lastmouse.clientY) {

    // Get column, row and zoom level of mouse position
    var crz = map.locationCoordinate(map.pointLocation(map.mouse(e)));

    // Normalize the column and row values to the 0..1 range
    var zoomMultiplier = Math.pow(2, crz.zoom-1);

    var x01 = crz.column/zoomMultiplier;
    var y01 = crz.row/zoomMultiplier;

    // Multiply with the original image width and height
    var mx = x01*originalWidth;
    var my = y01*originalHeight;

    // Now we have the mouse coordinates on the original image!
    //console.log(mx, my);

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

  var point = map.locationPoint(map.coordinateLocation({column, row}));

  return point;
}

$("#searchsubmit").click(function() {
  console.log("Click")
  $.get("/search", {"search": $("#searchinput").val()}, function(data) {
    console.log(data)
    map.center(xy2coords(data.x, data.y, data.z));
    map.zoom(data.z);
  })
})

$("#searchinput").autocomplete({
  minLength: 3,
  appendTo: $("#appendto"),
  position: { my: "left bottom", at: "left top", collision: "flip" },
  source: "/suggest"
})
