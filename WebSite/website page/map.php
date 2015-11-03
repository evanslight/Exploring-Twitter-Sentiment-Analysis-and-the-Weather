<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!--This page is to present the instant tweets in the map-->
<!DOCTYPE html>
<html>
<head>
<script
src="http://maps.googleapis.com/maps/api/js">
</script>


<script>
var myCenter=new google.maps.LatLng(-28.082779, 134.721838);
var map;
var mapProp;
var marker;
var checkMap = false;

function initialize()
{
  mapProp = {
    center:myCenter,
    zoom:5,
    mapTypeId:google.maps.MapTypeId.ROADMAP
    };

  map=new google.maps.Map(document.getElementById("googleMap"),mapProp);

  checkMap = true;
}
google.maps.event.addDomListener(window, 'load', initialize);
</script>



<script>
function addPoint(){
  if(checkMap){

    var xmlhttp;
    var LatLng_point;
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function()
    {
      if (xmlhttp.readyState==4 && xmlhttp.status==200)
      {
          LatLng_point=JSON.parse(xmlhttp.responseText);
          // alert(LatLng_point);
      }
    }
    xmlhttp.open("GET","map_server.php",false);
    xmlhttp.send();

    // alert(LatLng_point.split(",")[0]);
    // alert(LatLng_point.split(",")[1]);

    var myCenter1=new google.maps.LatLng(LatLng_point.split(",")[0], LatLng_point.split(",")[1]);
    marker=new google.maps.Marker({
    position:myCenter1,
    });
    marker.setMap(map);
    checkMap = false;
  }
}

function removePoint(){
  if(!checkMap){
    marker.setMap(null);
       checkMap = true;
  }
}

setInterval(addPoint, 100);
setInterval(removePoint, 3000);
</script>
</head>

<body>
<div id="googleMap" style="width:1100px;height:600px;"></div>
</body>
</html>
