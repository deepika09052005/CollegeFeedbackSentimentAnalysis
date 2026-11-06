
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching College Feedback project from GitHub'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python --version'
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Validate Python Files') {
            steps {
                bat 'python -m compileall -q app.py pages train_model.py generate_dataset.py'
                echo 'Python files validated successfully'
            }
        }

        stage('Verify ML Model') {
            steps {
                bat 'python -c "import joblib; joblib.load(\'model/sentiment_model.pkl\'); joblib.load(\'model/vectorizer.pkl\'); print(\'ML models loaded successfully\')"'
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
