# Counting Words in Audio

A 2022 Erdős Institute data science project investigating whether audio features and statistical models can improve word counting from speech clips. The work compares silence-based counting, regression models, and validation baselines rather than claiming a production speech-recognition system.

[<img width="1536" height="864" alt="Counting Words in Audio" src="https://github.com/user-attachments/assets/ee0c3963-b8bf-4d77-98c0-0f4ac6f265b7" />](https://drive.google.com/file/d/1lejr31wBK4knTjxI_1BN81f3KYzHjGAP/view?usp=drive_link)


## Question and approach

Given a short audio clip, how accurately can we estimate its number of spoken words? We analyzed roughly 2,800 Mozilla Common Voice clips, explored signal-derived features, tuned a silence-based counter, and compared linear and multiclass approaches. The three-feature regression model reduced validation mean squared error against a fixed-parameter counter; its modest R² is an important limit on the strength of the prediction.

## Start here

- [Project summary and findings](Summary.ipynb)
- [Exploratory analysis](01_1_EDA_DongJoanne.ipynb)
- [Multiple linear regression](02_2_ML_Multiple_Linear_Regression.ipynb)
- [Model comparison](03_1_ValTest_of_ML_Models.ipynb)
- [Further validation](03_2_ValTest_of_MLR_Model.ipynb)

The repository includes intermediate notebooks, derived data, and experimental work from the original project. Read the summary first for context. This is a retrospective research exercise; it was not deployed as a speech service.

## Data and collaborators

The source was the [Common Voice 2 dataset on Kaggle](https://www.kaggle.com/datasets/danielgraham1997/commonvoice2). This was a team project at the Erdős Institute; notebook names preserve collaborators' contributions. See the notebooks for specific methods and results.
