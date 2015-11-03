<!-- Author: Hao DUAN<548771> Yu SUN <629341> -->
<!-- Date: 30 Oct 2015 -->
<!-- this is the description page of all features we studied -->
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
        </script>
    </head>
    
    <body>
    <!-- Nav starts -->
        <?php require("share/nav.html") ?>
    <!-- Nav ends -->

        <div class="section">
            <div class="container">
                <div class="row">
                    <h2 id = "title1" style="text-align:center;">Word-based Analysis</h2>
                    <div class="col-md-4 hoverSection1">
                        <h3>Pattern</h3>
                        <p>This is scored by python package: pattern.en.sentiment, which
                            <br>contains a dictionary for adjectives that occur frequently
                            <br>and their correspding sentiemnt polarity.</p>
                    </div>
                    <div class="col-md-4 hoverSection1">
                        <h3>Positive Words%</h3>
                        <p>The number of positive word evaluated by pattern.en.sentiment
                            <br>divides by the total number of words in a sentence</p>
                    </div>
                    <div class="col-md-4 hoverSection1">
                        <h3>Negative Words%</h3>
                        <p>The number of positive word evaluated by pattern.en.sentiment
                            <br>divides by the total number of words in a sentence.</p>
                    </div>
                </div>
            </div>
        </div><br><br>

        <div class="section">
            <div class="container">
                <div class="row">
                    <h2 id = "title2" style="text-align:center;">Picture-based Analysis</h2>
                    <div class="col-md-4 hoverSection2">
                        <h3>B% G%</h3>
                        <p>Blue color pixels value divide by total of pixels value
                            <br>Green color pixels value divide by total of pixels value</p>
                    </div>
                    <div class="col-md-4 hoverSection2">
                        <h3>(R+G+B)/3</h3>
                        <p>Evaluate a picture is birght or dark.</p>
                    </div>
                    <div class="col-md-4 hoverSection2">
                        <h3>Open CV</h3>
                        <p>Smile and face detection to recognition,
                            <br>based on haar features and cascade classifier.</p>
                    </div>
                </div>
            </div>
        </div>
 
    </body>

</html>