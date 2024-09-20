import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

csv_file_path = "/mnt/data/historical_user_data.csv"
df = pd.read_csv(csv_file_path)

num_new_data_points = 100

new_data = {
    'Gender': np.random.choice(['Male', 'Female', 'Non-binary'], num_new_data_points),
    'Year of Study': np.random.randint(1, 5, num_new_data_points),
    'Branch': np.random.choice(['Computer Science', 'Electronics', 'Mechanical', 'Civil'], num_new_data_points),
    'Type of Schooling till 10th Grade': np.random.choice(['CBSE', 'State Board', 'ICSE'], num_new_data_points),
    'Percentage in Class 10th': np.random.uniform(50, 100, num_new_data_points),
    'Percentage in Class 12th': np.random.uniform(50, 100, num_new_data_points),
    'Programming Languages Known': np.random.randint(1, 6, num_new_data_points),
    'Actively Involved in Specific Technology': np.random.choice(['Yes', 'No'], num_new_data_points),
    'Exposure to Data Structures and Algorithms': np.random.randint(1, 6, num_new_data_points),
    'Exposure to GitHub': np.random.randint(1, 6, num_new_data_points),
    'Participation in Hackathons': np.random.randint(1, 6, num_new_data_points),
    'Made Software Projects': np.random.choice(['Yes', 'No'], num_new_data_points),
    'Course Title': np.random.choice(['Intro to Python', 'Advanced Algorithms', 'Web Development', 'Data Science'], num_new_data_points),
    'Course Organization': np.random.choice(['Udemy', 'Coursera', 'edX', 'LinkedIn Learning'], num_new_data_points),
    'Course Certificate Type': np.random.choice(['Free', 'Paid'], num_new_data_points),
    'Course Rating': np.random.uniform(1, 5, num_new_data_points),
    'Course Difficulty': np.random.choice(['Beginner', 'Intermediate', 'Advanced'], num_new_data_points),
    'Additional Data': [[0.6, 0.7, 0.5, 0.8], [0.8, 0.9, 0.6, 0.7], [0.5, 0.6, 0.4, 0.9], [0.7, 0.8, 0.6, 0.9]] * (num_new_data_points // 4)
}

new_df = pd.DataFrame(new_data)

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

def process_text(text):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    words = [ps.stem(word) for word in words]
    return ' '.join(words)

new_df['Processed Course Title'] = new_df['Course Title'].apply(process_text)
new_df['Processed Branch'] = new_df['Branch'].apply(process_text)

new_csv_file_path = "/mnt/data/new_historical_user_data_nltk_processed.csv"
new_df.to_csv(new_csv_file_path, index=False)

new_json_file_path = "/mnt/data/new_historical_user_data_nltk_processed.json"
new_df.to_json(new_json_file_path, orient='records')

new_csv_file_path, new_json_file_path
