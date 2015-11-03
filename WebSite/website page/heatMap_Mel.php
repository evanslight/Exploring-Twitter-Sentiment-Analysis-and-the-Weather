<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- weather condition analysis of >Melbourne Suburbs displayed in graphs -->
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
                <button type="button" class="btn btn-success" onclick="{location.href='heatMap_cities.php'}">8 Cities</button>
                <button type="button" class="btn btn-primary" onclick="{location.href='heatMap_Mel.php'}">Melbourne Suburbs</button>
              </span><br>
              <h4 style="margin-left: 11%">Emotion Situation For Different Weather Condition (Melbourne Suburbs)</h4>
                <iframe src="melboure_suburb_weather_condition.html" width="100%" height="900px" style="border-width: 0px; border: soild;"></iframe>
              </div>
            <div class="col-md-1"></div>
          </div>
        </div>
      </div>
  </body>
</html>