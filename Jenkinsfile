
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching project from GitHub'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"C:\\CollegeFeedbackSentimentAnalysis\\venv\\Scripts\\python.exe" --version'
                bat '"C:\\CollegeFeedbackSentimentAnalysis\\venv\\Scripts\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Validate Python Files') {
            steps {
                bat '"C:\\CollegeFeedbackSentimentAnalysis\\venv\\Scripts\\python.exe" -m compileall -q app.py pages train_model.py generate_dataset.py'
                echo 'Python files validated successfully'
            }
        }

        stage('Verify ML Model') {
            steps {
                bat '"C:\\CollegeFeedbackSentimentAnalysis\\venv\\Scripts\\python.exe" -c "import joblib; joblib.load(\'model/sentiment_model.pkl\'); joblib.load(\'model/vectorizer.pkl\'); print(\'ML models loaded successfully\')"'
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }
        failure {
            echo 'CI Pipeline failed. Check the console output.'
        }
    }
}
