<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- heat map for 8 australian cities on different data are displayed-->
<!DOCTYPE html>
<html>
  <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&signed_in=true&libraries=visualization&key=AIzaSyAUp8jbEBYbF8fEszgTtCJUowIrK6KKV3U"></script>
            <!-- GET couchdb-->
      <script src="getCouchDB.js"></script>
  <link rel="stylesheet" href="http://apps.bdimg.com/libs/jqueryui/1.10.4/css/jquery-ui.min.css">
  <script src="http://apps.bdimg.com/libs/jquery/1.10.2/jquery.min.js"></script>
  <script src="http://apps.bdimg.com/libs/jqueryui/1.10.4/jquery-ui.min.js"></script>
  <link rel="stylesheet" href="http://www.runoob.com/try/demo_source/jqueryui/style.css">
  <script>
  $(function() {
    $( "#datepicker" ).datepicker();
  });
  </script>

    <script>
// Adding 500 Data Points
var map, pointarray, heatmap;


var taxiData = [];

function initialize() {

  //http://115.146.93.74:5984/tweet_db/_design/map/_view/dailygeo?group_level=2

  var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(-28.987536, 135.314300),
    mapTypeId: google.maps.MapTypeId.SATELLITE
  };

  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  var pointArray = new google.maps.MVCArray(taxiData);

  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
  });

  heatmap.setMap(map);
}



function changeOpacity() {
 // heatmap.set('opacity', heatmap.get('opacity') ? null : 0.2);
 heatmap.setMap(heatmap.getMap() ? null : map);
}

google.maps.event.addDomListener(window, 'load', initialize);

<!-- CODE FOR DEAL COUCHDB DATA-->
function dealdata(data){
  //== set json data to global

  var i=0;
  for(i in data.rows){
    // label1= parseInt(data.rows[i].value[1]);
    // label2= parseInt(data.rows[i].value[0]);
    taxiData[i]=new google.maps.LatLng(data.rows[i].value[1],data.rows[i].value[0]);
  }
 heatmap.setMap(map);
}

    </script>
  </head>

  <body>

<?php
  $date=$_GET["date"];
  if(empty($date)){
      $date = 1;
      $handle = fopen("http://127.0.0.1:5984/cities/_design/mapreduce/_view/australia?key=%22$date%20Oct%202015%22","rb");
      $content = "";
      while(!feof($handle)){
        $content.=fread($handle,100000);
      }
      fclose($handle);

      echo "<script>";
      echo "dealdata(".$content.");";
      echo "</script>";
  }else{
      $handle = fopen("http://127.0.0.1:5984/cities/_design/mapreduce/_view/australia?key=%22$date%20Oct%202015%22","rb");
      $content = "";
      while(!feof($handle)){
        $content.=fread($handle,100000);
      }
      fclose($handle);

      echo "<script>";
      echo "dealdata(".$content.");";
      echo "</script>";
  }
?>
<script>
  function getdate(str){
      var str=str.split("/")[1];
      if(str[0] == 0){
        str=str[1];
      }
      window.location.href = "heatMap_9c.php?date="+str;
  }
</script>
<br>
    <div class="section">
      <div class="container">
        <div class="row">
          <div  class="col-md-2"></div>
          <div  class="col-md-8">
            <span style="font-size:26px;">Heat Map For 8 Australian Cities on</span>

            <?php
            if(empty($date)){
              $date = 1;
            }
            echo "<input type=\"text\" id=\"datepicker\" onchange=\"getdate(this.value)\" value=\"Oct/".$date."/2015\">";
            ?>
            <div style="width:100%; overflow: hidden;">
              <div id="map-canvas" style="width:750px;height:450px;"></div>
            </div>
          </div>
          <div  class="col-md-2"></div>
        </div>
      </div>
    </div>

  </body>
</html>