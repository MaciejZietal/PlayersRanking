# Creating a ranking of Premier League players

This project was made in order to create a ranking of offensive football players based on their individual statistics. This ranking was constructed using linear ordering: Hellwig's and TOPSIS methods.

## Code
- functions.py contains all created and used functions,
- hellwig.py contains data preparation and application of Hellwig's method,
- topsis.py contains data preparation and application of TOPSIS method,
- visualization.py visualizes the results.

## Versions
- All used packages and their versions are listed in  _requirements.txt_  file
- Python 3.8
- Anaconda 2020.07

## Data
Used data is from _https://fbref.com/_

## Results

In both methods top 5 best players are the same but the order is different, so those methods gave similar results.

![HellwigRanking](https://user-images.githubusercontent.com/77171262/162632040-77a378a6-ba04-4a53-ae75-2ff7236eef4e.png)

In Hellwig's method the best player is Bruno Fernandes, second is Mason Mount and third Harry Kane.

![TOPSISRanking](https://user-images.githubusercontent.com/77171262/162632047-e22eab5b-e0a7-429c-887d-90e01d64cb47.png)

In TOPSIS top3 is the same but Bruno is second while Kane is first.
