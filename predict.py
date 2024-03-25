from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import functions as F









# Importing the required libraries 
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder 
from pyspark.ml import Pipeline 

# Importing the evaluator 
from pyspark.ml.evaluation import BinaryClassificationEvaluator 

  


def prediction(df):

    print("--------------------------ML Prediction STreaming-------------------------")

    # Feature selection (assuming features are not in the first and last columns)
    features = df.select("Humidity", "Light", "CO2", "HumidityRatio")
    label = df.select("Occupancy") 
    print("Features: ",features)
    print("Label: ",label)

    assembler = VectorAssembler(inputCols=['Temperature', 
                                       'Humidity','Light', 
                                       'CO2','HumidityRatio'],
                                    outputCol='features') 

    log_reg = LogisticRegression(featuresCol='features', 
                             labelCol='Occupancy') 

    # Creating the pipeline 
    pipe = Pipeline(stages=[assembler, log_reg]) 

    # Splitting the data into train and test 
    train_data, test_data = df.randomSplit([0.7, .3]) 
    
    # Fitting the model on training data 
    fit_model = pipe.fit(train_data) 
    
    # Storing the results on test data 
    results = fit_model.transform(test_data) 

    # Calling the evaluator 
    res = BinaryClassificationEvaluator (rawPredictionCol='prediction',labelCol='Occupancy') 
    
    # Evaluating the AUC on results 
    ROC_AUC = res.evaluate(results) 
    print("AUC: ",ROC_AUC)

    return df

def apply_model(df, selected_model, plot_flag=True):
 
    print("--------------------------ML STreaming-------------------------")
    model_title, model_abbreviation = selected_model

    # Feature selection (assuming features are not in the first and last columns)
    features = df.select("Humidity", "Light", "CO2", "HumidityRatio")
    label = df.select("Occupancy") 
    print("Features: ",features)
    print("Label: ",label)

    assembler = VectorAssembler(inputCols=['Temperature', 
                                       'Humidity','Light', 
                                       'CO2','HumidityRatio'],
                                    outputCol='features') 


    # Train-test split using Spark functions for efficiency
    train, test = df.randomSplit([0.75, 0.25], seed=42)
    

    # Model selection and fitting
    model = None
    if model_title == "Logistic Regression":
        model = LogisticRegression(featuresCol='features', 
                             labelCol='Occupancy')
    elif model_title == "DecisionTree":
        model = DecisionTreeClassifier()
    elif model_title == "RandomForest":
        model = RandomForestClassifier(numTrees=10)  # Adjust numTrees as needed
    elif model_title == "K-Nearest Neighbors":
        model = KNeighborsClassifier(nNeighbors=int(features.count()**0.5), metric='minkowski', p=2)

    elif model_title == "Naive Bayes":
        model = GaussianNB()
    elif model_title == "Support Vector Machine":
        model = SVC(probability=True)
    elif model_title == "Gradient Boosting":
        model = GradientBoostingClassifier()
    elif model_title == "Multi-Layer Perceptron":
        model = MLPClassifier(hiddenLayerSizes=(8, 8, 8), activation='relu', solver='adam', maxIter=500)
    else:
        raise ValueError(f"Unsupported model: {model_title}")

    if model is not None:
        model_fit = model.fit(train)

        # Prediction and evaluation using Spark MLlib
        predictions = model_fit.transform(test)
        evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
        accuracy = evaluator.evaluate(predictions)

        if plot_flag:
            pass
            # Implement your preferred evaluation plot generation mechanism using Spark MLlib or other libraries

        # Store results (example using Spark SQL and a global variable is omitted, adjust for your use case)
        # result.loc[absTitle] = [modelTitle, tn, fp, fn, tp, round(accuracy * 100, 6)]

        print(f"Accuracy of {model_title} Classifier on test set: {accuracy:.6f}")



