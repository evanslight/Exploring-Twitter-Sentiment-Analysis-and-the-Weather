<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- this page allows user to try the sentiment analysis function that model can provide.
the input can be random text entered and output is presented in persentage -->
<!DOCTYPE html>
<html>
    
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
        <style>
            .hoverSection1:hover{
                background-color: rgb(235,235,235);
            }
            .hoverSection2:hover{
                background-color: rgb(235,235,235);
            }
            .hoverSection3:hover{
                background-color: rgb(235,235,235);
            }
        </style>
        <script>
            // $(document).ready(function(){
            //      $(".hoverSection1").hover(function(){
            //          $("#title1").css("text-shadow", "2px 2px 3px rgb(132,132,255)");
            //      },function(){
            //          $("#title1").css("text-shadow", "0 0 0 rgb(111,111,111)");
            //      });
            // });

            // $(document).ready(function(){
            //      $(".hoverSection2").hover(function(){
            //          $("#title2").css("text-shadow", "2px 2px 3px rgb(132,132,255)");
            //      },function(){
            //          $("#title2").css("text-shadow", "0 0 0 rgb(111,111,111)");
            //      });
            // });

            // $(document).ready(function(){
            //      $(".hoverSection3").hover(function(){
            //          $("#title3").css("text-shadow", "2px 2px 3px rgb(132,132,255)");
            //      },function(){
            //          $("#title3").css("text-shadow", "0 0 0 rgb(111,111,111)");
            //      });
            // });
        </script>
    </head>
    
    <body>
    <!-- Nav starts -->
        <?php require("share/nav.html"); 
        ?>
    <!-- Nav ends -->

        <div class="section">
            <div class="container">

                <div class="row">
                    <form class="form-inline" action="testYourself.php" method="POST">
                        <label for="userInput">Enter Your Text: &nbsp;</label>
                        <input type="text" class="form-control" name="userInput" id="userInput" style="width: 70%;">
                      <button type="submit" class="btn btn-default">Analyse</button>
                    </form>
                </div><br>

                <div class="row">
                    <div class="col-md-4 hoverSection1">
                        <h2 id = "title1" style="text-align:center;">Random Forest</h2>
                        <table class="table table-hover">
                          <tr>
                            <th>Positive(1):</th>
                            <td><span id="rf_positive"></span></td>
                          </tr>
                          <tr>
                            <th>Nature(0):</th>
                            <td><span id="rf_nature"></span></td>
                          </tr>
                          <tr>
                            <th>Negative(-1):</th>
                            <td><span id="rf_negative"></span></td>
                          </tr>
                        </table>
                    </div>

                    <div class="col-md-4 hoverSection2">
                        <h2 id = "title2" style="text-align:center;">Support Vector Machine</h2>
                        <table class="table table-hover">
                          <tr>
                            <th>Positive(1):</th>
                            <td><span id="clf_positive"></span></td>
                          </tr>
                          <tr>
                            <th>Nature(0):</th>
                            <td><span id="clf_nature"></span></td>
                          </tr>
                          <tr>
                            <th>Negative(-1):</th>
                            <td><span id="clf_negative"></span></td>
                          </tr>
                        </table>
                    </div>

                    <div class="col-md-4 hoverSection3">
                        <h2 id = "title3" style="text-align:center;">Logistic Regression</h2>
                        <table class="table table-hover">
                          <tr>
                            <th>Positive(1):</th>
                            <td><span id="logreg_positive"></span></td>
                          </tr>
                          <tr>
                            <th>Nature(0):</th>
                            <td><span id="logreg_nature"></span></td>
                          </tr>
                          <tr>
                            <th>Negative(-1):</th>
                            <td><span id="logreg_negative"></span></td>
                          </tr>
                        </table>
                    </div>                    
                </div>

                <div class="row">
                    <h3>
                        Final Result is: <span style="color: red;" id = "finalResult"></span>
                    </h3>
                </div>

            </div>
        </div>

<?php 
   $userInput = $_POST["userInput"];

    if(!empty($userInput)){

        require_once('php_python.php');
        $result = ppython($userInput);
        $result=json_decode($result,true);

        $finalResult = $result["finalResult"];

        $rf_netural = $result["rf"]["netural"];
        $rf_positive = $result["rf"]["positive"];
        $rf_negative = $result["rf"]["negative"];

        $max_rf = $rf_netural;
        if($max_rf < $rf_positive){
            $max_rf = $rf_positive;
            if($max_rf < $rf_negative){
                $max_rf = $rf_negative;
                echo "
                <script>
                    document.getElementById(\"rf_negative\").innerHTML=\"<b style=\\\"color: red;\\\">".$rf_negative."</b>\";
                    document.getElementById(\"rf_nature\").innerHTML=\"".$rf_netural."\";
                    document.getElementById(\"rf_positive\").innerHTML=\"".$rf_positive."\";
                </script>";
            }else{
                echo "
                <script>
                    document.getElementById(\"rf_positive\").innerHTML=\"<b style=\\\"color: red;\\\">".$rf_positive."</b>\";
                    document.getElementById(\"rf_nature\").innerHTML=\"".$rf_netural."\";
                    document.getElementById(\"rf_negative\").innerHTML=\"".$rf_negative."\";
                </script>";
            }
        }elseif ($max_rf < $rf_negative) {
            $max_rf = $rf_negative;
                echo "
                <script>
                    document.getElementById(\"rf_negative\").innerHTML=\"<b style=\\\"color: red;\\\">".$rf_negative."</b>\";
                    document.getElementById(\"rf_nature\").innerHTML=\"".$rf_netural."\";
                    document.getElementById(\"rf_positive\").innerHTML=\"".$rf_positive."\";
                </script>";
        }else{
            echo "
            <script>
                document.getElementById(\"rf_nature\").innerHTML=\"<b style=\\\"color: red;\\\">".$rf_netural."</b>\";
                document.getElementById(\"rf_positive\").innerHTML=\"".$rf_positive."\";
                document.getElementById(\"rf_negative\").innerHTML=\"".$rf_negative."\";
            </script>";
        }

        $clf_netural = $result["clf"]["netural"];
        $clf_positive = $result["clf"]["positive"];
        $clf_negative = $result["clf"]["negative"];

        $max_clf = $clf_netural;
        if($max_clf < $clf_positive){
            $max_clf = $clf_positive;
            if($max_clf < $clf_negative){
                $max_clf = $clf_negative;
                echo "
                <script>
                    document.getElementById(\"clf_negative\").innerHTML=\"<b style=\\\"color: red;\\\">".$clf_negative."</b>\";
                    document.getElementById(\"clf_nature\").innerHTML=\"".$clf_netural."\";
                    document.getElementById(\"clf_positive\").innerHTML=\"".$clf_positive."\";
                </script>";
            }else{
                echo "
                <script>
                    document.getElementById(\"clf_positive\").innerHTML=\"<b style=\\\"color: red;\\\">".$clf_positive."</b>\";
                    document.getElementById(\"clf_nature\").innerHTML=\"".$clf_netural."\";
                    document.getElementById(\"clf_negative\").innerHTML=\"".$clf_negative."\";
                </script>";
            }
        }elseif ($max_clf < $clf_negative) {
            $max_clf = $clf_negative;
                echo "
                <script>
                    document.getElementById(\"clf_negative\").innerHTML=\"<b style=\\\"color: red;\\\">".$clf_negative."</b>\";
                    document.getElementById(\"clf_nature\").innerHTML=\"".$clf_netural."\";
                    document.getElementById(\"clf_positive\").innerHTML=\"".$clf_positive."\";
                </script>";
        }else{
            echo "
            <script>
                document.getElementById(\"clf_nature\").innerHTML=\"<b style=\\\"color: red;\\\">".$clf_netural."</b>\";
                document.getElementById(\"clf_positive\").innerHTML=\"".$clf_positive."\";
                document.getElementById(\"clf_negative\").innerHTML=\"".$clf_negative."\";
            </script>";
        }

        $logreg_netural = $result["logreg"]["netural"];
        $logreg_positive = $result["logreg"]["positive"];
        $logreg_negative = $result["logreg"]["negative"];

        $max_logreg = $logreg_netural;
        if($max_logreg < $logreg_positive){
            $max_logreg = $logreg_positive;
            if($max_logreg < $logreg_negative){
                $max_logreg = $logreg_negative;
                echo "
                <script>
                    document.getElementById(\"logreg_negative\").innerHTML=\"<b style=\\\"color: red;\\\">".$logreg_negative."</b>\";
                    document.getElementById(\"logreg_nature\").innerHTML=\"".$logreg_netural."\";
                    document.getElementById(\"logreg_positive\").innerHTML=\"".$logreg_positive."\";
                </script>";
            }else{
                echo "
                <script>
                    document.getElementById(\"logreg_positive\").innerHTML=\"<b style=\\\"color: red;\\\">".$logreg_positive."</b>\";
                    document.getElementById(\"logreg_nature\").innerHTML=\"".$logreg_netural."\";
                    document.getElementById(\"logreg_negative\").innerHTML=\"".$logreg_negative."\";
                </script>"; 
            }
        }elseif ($max_logreg < $logreg_negative) {
            $max_logreg = $logreg_negative;
                echo "
                <script>
                    document.getElementById(\"logreg_negative\").innerHTML=\"<b style=\\\"color: red;\\\">".$logreg_negative."</b>\";
                    document.getElementById(\"logreg_nature\").innerHTML=\"".$logreg_netural."\";
                    document.getElementById(\"logreg_positive\").innerHTML=\"".$logreg_positive."\";
                </script>";
        }else{
            echo "
            <script>
                document.getElementById(\"logreg_nature\").innerHTML=\"<b style=\\\"color: red;\\\">".$logreg_netural."</b>\";
                document.getElementById(\"logreg_positive\").innerHTML=\"".$logreg_positive."\";
                document.getElementById(\"logreg_negative\").innerHTML=\"".$logreg_negative."\";
            </script>";
        }

        echo "
        <script>
            document.getElementById(\"finalResult\").innerHTML=\"<b style=\\\"color: red;\\\">".$finalResult."</b>\";
        </script>";
    }
 
?>
    </body>
</html>
