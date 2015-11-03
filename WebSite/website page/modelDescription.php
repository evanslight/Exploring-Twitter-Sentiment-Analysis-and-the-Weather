<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- this is the description page of all models we studied -->
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
            $(document).ready(function(){
                 $(".hoverSection1").hover(function(){
                     $("#title1").css("text-shadow", "2px 2px 3px rgb(132,132,255)");
                 },function(){
                     $("#title1").css("text-shadow", "0 0 0 rgb(111,111,111)");
                 });
            });

            $(document).ready(function(){
                 $(".hoverSection2").hover(function(){
                     $("#title2").css("text-shadow", "2px 2px 3px rgb(132,132,255)");
                 },function(){
                     $("#title2").css("text-shadow", "0 0 0 rgb(111,111,111)");
                 });
            });

            $(document).ready(function(){
                 $(".hoverSection3").hover(function(){
                     $("#title3").css("text-shadow", "2px 2px 3px rgb(132,132,255)");
                 },function(){
                     $("#title3").css("text-shadow", "0 0 0 rgb(111,111,111)");
                 });
            });
        </script>
    </head>
    
    <body>
    <!-- Nav starts -->
        <?php require("share/nav.html") ?>
    <!-- Nav ends -->

        <div class="section">
            <div class="container">
                <div class="row">
                    <h2 id = "title1" style="text-align:center;">Logistic Regression</h2>
                    <div class="col-md-1"></div>
                    <div class="col-md-10 hoverSection1">
                        <p>Logistic regression measures the relationship between the categorical 
                            dependent variable and one or more independent variables by 
                            estimating probabilities using a logistic function, which is the cumulative 
                            logistic distribution.(Wiki visited on 20/10/2015)</p>
                    </div>
                    <div class="col-md-1"></div>
                </div>

                <div class="row">
                    <h2 id = "title2" style="text-align:center;">Support Vector Machine</h2>
                    <div class="col-md-1"></div>
                    <div class="col-md-10 hoverSection2">
                        <p>A Support Vector Machine (SVM) is a discriminative classifier formally 
                            defined by a separating hyperplane. In other words, given labeled 
                            training data (supervised learning), the algorithm outputs an optimal hyperplane 
                            which categorizes new examples. (Wiki visited on 20/10/2015)</p>
                    </div>
                    <div class="col-md-1"></div>
                </div>

                <div class="row">
                    <h2 id = "title3" style="text-align:center;">Random Forest</h2>
                    <div class="col-md-1"></div>
                    <div class="col-md-10 hoverSection3">
                        <p>Random forests are an ensemble learning method for classification, 
                            regression and other tasks, that operate by constructing a multitude of 
                            decision trees at training time and outputting the class that is the 
                            mode of the classes (classification) or mean prediction (regression) of 
                            the individual trees.(Wiki visited on 20/10/2015)</p>
                    </div>
                    <div class="col-md-1"></div>
                </div>
            </div>
        </div>

    </body>
</html>