<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- data fetched from main cities are marked on the map.
data about these cities are illustrated in different graphs below -->
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
            <div class="col-md-2"></div>
              <div class="col-md-8">
                 <iframe src="./heatMap_9c.php" width="100%" height="520px" style="border-width: 0px; border: soild;"></iframe>
                  <button type="button" class="btn btn-success" onclick="{location.href='cities/Melbourne.php'}">Detail Analysis</button>
              </div>
            <div class="col-md-2"></div>
          </div>
        </div>
      </div>
  </body>
</html>