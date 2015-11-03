<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- fetched data about melbourne is marked in heat map.
different date of data can be selected in calendar -->
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
    <?php require("share/nav.html") ?>
      <div class="section">
        <div class="container">
          <div class="row">
            <div class="col-md-1"></div>
              <div class="col-md-10" style="margin-left: 8%">
              <span style="margin-left: 30%">
                <button type="button" class="btn btn-success" onclick="{location.href='heatMap1.php'}">Heat Map</button>
                <button type="button" class="btn btn-primary" onclick="{location.href='heatMap1_s.php'}">Scenario</button>
              </span>
                <iframe src="./heatMap_Melb.php" width="100%" height="600px" style="border-width: 0px; border: soild;"></iframe>
              </div>
            <div class="col-md-1"></div>
          </div>
        </div>
      </div>
  </body>
</html>