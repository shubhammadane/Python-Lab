# IMRS-Movie-recommendation-system

## Group Members

Aditya Khamkar  - BT24F05F002 <br>
Chaitanya Bakhal- BT24F05F006 <br>
Amaan Chaudhari - BT24F05F012 <br>

## Indian Movie Recommendation System

A content-based movie recommendation system specifically designed for Indian cinema. This application uses machine learning techniques to recommend movies based on genre, director, and actors, providing personalized suggestions for Bollywood and regional Indian films.

## Features

- **Content-Based Recommendations**: Uses TF-IDF vectorization and cosine similarity to find similar movies
- **Interactive Web Interface**: Built with Streamlit for easy user interaction
- **Advanced Filtering**: Filter recommendations by genre, actor, director, and rating range
- **Movie Posters**: Integrated with OMDB API to display movie posters
- **Responsive Design**: Clean and modern UI with custom styling
- **Real-time Search**: Search and get recommendations instantly

## Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for OMDB API)

### Setup
1. Clone or download this repository
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application
Start the Streamlit app by running:

```bash
streamlit run app.py
```
OR
```bash
python -m streamlit run app.py
```
The application will open in your default web browser at `http://localhost:8501`

### How to Use
1. **Select a Movie**: Choose a movie from the dropdown list that you like
2. **Get Recommendations**: Click the "Get Recommendations" button
3. **Apply Filters** (Optional):
   - Filter by specific genre
   - Filter by actor
   - Filter by director
   - Set minimum rating
4. **Browse Results**: View recommended movies with posters, ratings, and details

## Data Source

The recommendation system uses a dataset of Indian movies with the following information:
- Movie name
- Genre
- Director
- Lead actors (Actor 1, Actor 2)
- IMDb rating
- Number of votes
- Year of release

Data is sourced from IMDb ratings for Indian movies and cleaned using the data cleaning script in the `data cleaning method/` folder.

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms (TF-IDF, cosine similarity)
- **NumPy**: Numerical computing
- **Requests**: HTTP library for API calls
- **OMDB API**: Movie poster and additional information

## How It Works

1. **Data Processing**: Movie features (genre, director, actors) are combined into a text string
2. **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency) converts text into numerical vectors
3. **Similarity Calculation**: Cosine similarity measures the angle between vectors to find similar movies
4. **Recommendation Generation**: Top 100 similar movies are retrieved and filtered based on user preferences
5. **API Integration**: OMDB API fetches movie posters and additional details

## Project Structure

```
IMRS/
├── app.py                 # Main Streamlit application
├── cleanData.csv         # Cleaned movie dataset
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── data cleaning method/
    ├── dataCleaning.py      # Data cleaning script
    └── IMDbRatings_IndianMovies.csv  # Raw dataset
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- IMDb for movie data
- OMDB API for movie posters and information
- Streamlit for the web framework
- Scikit-learn for machine learning algorithms

## Genre Types
Action, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, Musical, Mystery, News, Romance, Sci-Fi, Sport, Thriller, War, Western, Period, Social, Spy
