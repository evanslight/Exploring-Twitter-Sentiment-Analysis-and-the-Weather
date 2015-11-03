Author: Hao DUAN<548771> Yu SUN<629341>  
Date: 30 Oct 2015  

[Folders Description]

[Baseline]
use commend below to run the program, the accuracy will be returned for naive bayes
   $python sentiment_term_frequency.py

[Eveluation Program]
use commend below to run the program, the eveluation for different models will be returned
	$Eveluation.py

[TrainData Set]
Actually, we provied our traindata set as local file in this system,but if the trainning set lost
Please used the install.py to get the tweets which has been labeled by us.

[Main Process]
This file has been located in different function folder, and this just a sample how the program likes.

[OptimizeParameter]
./OptimizeParameter
before run this programs, you have to have following directories and files 
./learningcurve ./Data/train_real_2000 ./Data/test_real_600
Sentimentanalysis_parameter_gridsearch.py: Search the optimized parameters for each model. Just run it and type the model you
would like to tune
learning_curve.py: draw learning curve for these model