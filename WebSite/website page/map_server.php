<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!--this code used to access the instant tweets in couch db-->
<?php
    $handle = fopen("http://127.0.0.1:5984/cities/_all_docs/_changes?descending=true&limit=1&include_docs=true&skip=1","rb");
    $content = "";
    while(!feof($handle)){
      $content.=fread($handle,100000);
    }
    fclose($handle);
    $content=json_decode($content,true);

    $userName = $content["rows"][0]["doc"]["userName"];
    $userUrl = $content["rows"][0]["doc"]["userImage"]; 
    $userContent = $content["rows"][0]["doc"]["text"];
    $userLoc_L0 = $content["rows"][0]["doc"]["geoInfo"]["locations"][1];
    $userLoc_L1 = $content["rows"][0]["doc"]["geoInfo"]["locations"][0];
    $userMood = $content["rows"][0]["doc"]["prediction"];
    $userCity = $content["rows"][0]["doc"]["city"];

    $map_data = array($userName,$userUrl,$userContent,$userLoc_L0,$userLoc_L1,$userMood,$userCity);
    echo json_encode($map_data);
?>