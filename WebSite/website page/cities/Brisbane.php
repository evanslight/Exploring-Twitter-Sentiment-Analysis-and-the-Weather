<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- Thie page is to invoke the brisbane html-->
<!DOCTYPE html>
<html>
    
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    </head>

    <body>
        <?php require("../share/nav_city.html") ?>
        <div class="section">
            <div class="container"><br><br>
                <div class="row">
                    <div class="col-md-1"></div>
                    <div class="col-md-10">
                    <div class="row" style="text-align:center;">
                      <div  class="col-md-2"></div>
                      <div  class="col-md-1"><a href="Melbourne.php"><img src="../image/cityLogo/Melbourne.jpg" style="width:100%; height: 60px" onclick="getData('Melbourne');">Melbourne</a></div>
                      <div  class="col-md-1"><a href="Canberra.php"><img src="../image/cityLogo/Canberra.png" style="width:100%; height: 60px" onclick="getData('Canberra');">Canberra</a></div>
                      <div  class="col-md-1"><a href="Brisbane.php"><img src="../image/cityLogo/Brisbane.png" style="width:100%; height: 60px" onclick="getData('Brisbane');">Brisbane</a></div>
                      <div  class="col-md-1"><a href="Sydney.php"><img src="../image/cityLogo/Sydney.png" style="width:100%; height: 60px" onclick="getData('Sydney');">Sydney</a></div>
                      <div  class="col-md-1"><a href="Perth.php"><img src="../image/cityLogo/Perth.jpeg" style="width:100%; height: 60px" onclick="getData('Perth');">Perth</a></div>
                      <div  class="col-md-1"><a href="Adelaide.php"><img src="../image/cityLogo/Adelaide.jpg" style="width:100%; height: 60px" onclick="getData('Adelaide');">Adelaide</a></div>
                      <div  class="col-md-1"><a href="Hobart.php"><img src="../image/cityLogo/Hobart.jpg" style="width:100%; height: 60px" onclick="getData('Hobart');">Hobart</a></div>
                      <div  class="col-md-1"><a href="Darwin.php"><img src="../image/cityLogo/Darwin.jpg" style="width:100%; height: 60px" onclick="getData('Darwin');">Darwin</a></div>
                      <div  class="col-md-2"></div>
                    </div><br>

                    
                    <iframe src="./Brisbane.html" width="100%" height="1000px" style="border-width: 0px; border: soild;"></iframe>
                    

                    </div>
                    <div class="col-md-1"></div>
                </div>
            </div>
        </div>
    </body>

</html>