<!DOCTYPE html>
<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- this page shows the instant tweets fetched that are marked on the map.
also, weather conditions of main cities in melbourne are illustrated in the table -->
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
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
    zoom:4,
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

    var myCenter1=new google.maps.LatLng(LatLng_point[3], LatLng_point[4]);

    document.getElementById("userPic").innerHTML = "<img src=\""+LatLng_point[1]+"\" height=\"80\" width=\"80\">";
    document.getElementById("userName").innerHTML =  LatLng_point[0] ;
    document.getElementById("tweetCont").innerHTML =  LatLng_point[2] ;
    if(LatLng_point[5]=="1"){
      document.getElementById("tweetMood").innerHTML = "Positive ("+LatLng_point[5]+")" ;
    }
    if(LatLng_point[5]=="0"){
      document.getElementById("tweetMood").innerHTML = "Natural ("+LatLng_point[5]+")" ;
    }
    if(LatLng_point[5]=="-1"){
      document.getElementById("tweetMood").innerHTML = "Negative ("+LatLng_point[5]+")";
    }

    document.getElementById("tweetCity").innerHTML =  LatLng_point[6] ;

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
setInterval(removePoint, 5000);
</script>

        <script>
        function getWeather(str)
        {
          var xmlhttp;
          if (window.XMLHttpRequest)
            {xmlhttp=new XMLHttpRequest();}
          else
            {xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");}

          xmlhttp.onreadystatechange=function()
            {
              if (xmlhttp.readyState==4 && xmlhttp.status==200){
                document.getElementById("weatherArea").innerHTML=xmlhttp.responseText;
              }
            }
          xmlhttp.open("GET","getWeather.php?city="+str,true);
          xmlhttp.send();
        }

        function selectDate(str)
        {
          var xmlhttp;
          if (window.XMLHttpRequest)
            {xmlhttp=new XMLHttpRequest();}
          else
            {xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");}

          xmlhttp.onreadystatechange=function()
            {
              if (xmlhttp.readyState==4 && xmlhttp.status==200){
                document.getElementById("weatherArea").innerHTML=xmlhttp.responseText;
              }
            }
          xmlhttp.open("GET","getWeather_Date.php?comb="+str,true);
          xmlhttp.send();
        }


        </script>
    </head>
    
    <body onload="getWeather('Melbourne')">
    <!-- Nav starts -->
        <?php require("share/nav.html") ?>
    <!-- Nav ends -->

    <br><br>
    <div class="section">
      <div class="container">

        <div class="row" style="text-align:center;">
          <div  class="col-md-2"></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Melbourne.jpg" style="width:100%; height: 60px" onclick="getWeather('Melbourne'); melbourneFocus()">Melbourne</a></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Canberra.png" style="width:100%; height: 60px" onclick="getWeather('Canberra'); canberraFocus()">Canberra</a></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Brisbane.png" style="width:100%; height: 60px" onclick="getWeather('Brisbane'); brisbaneFocus()">Brisbane</a></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Sydney.png" style="width:100%; height: 60px" onclick="getWeather('Sydney'); sydneyFocus()">Sydney</a></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Perth.jpeg" style="width:100%; height: 60px" onclick="getWeather('Perth'); perthFocus()">Perth</a></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Adelaide.jpg" style="width:100%; height: 60px" onclick="getWeather('Adelaide'); adelaideFocus()">Adelaide</a></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Hobart.jpg" style="width:100%; height: 60px" onclick="getWeather('Hobart'); hobartFocus()">Hobart</a></div>
          <div  class="col-md-1"><a href="#"><img src="image/cityLogo/Darwin.jpg" style="width:100%; height: 60px" onclick="getWeather('Darwin'); darwinFocus()">Darwin</a></div>
          <div  class="col-md-2"></div>
        </div>

        <div class="row">
          <!-- Map starts -->
          <div class="col-md-7" style="margin-top: 2%">
            <div style="width:100%; overflow: hidden;">
              <div id="googleMap" style="width:650px;height:300px;"></div>
            </div>
          </div>
          <!-- Map ends -->

          <!-- AJAX RETRIEVED -->
          <div class="col-md-5">
          <!-- News starts --> 
            <div>
                <div id="weatherArea">
                </div>
            </div>
          <!-- News ends -->
          </div>
        </div>

        <div class="row">
          <div class="col-md-12">
              <h3>Instant Tweets</h3>
              <table class="table">
                  <tr class="success">
                    <th style="width: 100px;">User Avatar</th>
                    <th style="width: 100px;">User Name</th>
                    <th style="width: 50%;">Tweet Content</th>
                    <th>Tweet Location</th>
                    <th>Sentiment Analysis</th>
                  </tr>
                  <tr >
                    <td style="width: 100px;"><span id = "userPic"></span></td>
                    <td style="width: 100px;"><b><span id = "userName"></span></b></td>
                    <td style="width: 50%;"><span id = "tweetCont"></span></td>
                    <td><span id = "tweetCity"></span></td>
                    <td><span id = "tweetMood"></span></td>
                  </tr>
              </table>
          </div>
        </div><br><br>

      </div>
    </div>

    </body>
</html>

