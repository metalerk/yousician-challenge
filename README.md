# Yousician challenge

API REST made as test challenge for Yousician.

## API Reference

- GET /songs
  - Returns a list of songs with some details on them
  
  @params:
    * **page** : int (optional) <br>
    Display a specific page
    * **per_page** : int (optional) <br>
    Specify how much items are displayed on each page

  @return:
    * **songs** : array <br>
    Contains the song objects list.
    * **total** : int <br>
    Number of song objects.
    * **current_page** : int (optional) <br>
    Show current page only if page and per_page parameters are provided.
    * **total_pages** : int (optional)<br>
    Show total pages only if page and per_page parameters are provided.
    
  Example:
  ```sh
  curl -H "Accept: application/json" -X GET http://localhost:8080/songs
  ```
    
  With parameters:
    
  ```sh
  curl -H "Accept: application/json" -X GET   http://localhost:8080/songs?page=1&per_page=4
  ```

- GET /songs/avg/difficulty
  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.
  
  @params:
    * **level** : int (optional) <br>
    Limits only certain items with that level.
    Specify how much items are displayed on each page.

  @return:
    * **average_difficulty** : int <br>
    Song average difficulty. If level is not specified it will return all songs average.

  Example:
    
  ```sh
  curl -H "Accept: application/json" -X GET http://localhost:8080/songs/avg/difficulty?level=3
  ```

- GET /songs/search
  - Takes in parameter a 'message' string to search.
  - Return a list of songs. It searches in song's artist and title fields and is case insensitive.

  @params:
  * **message** : string <br>

  @return:
    * **songs** : array <br>
    Contains the song objects list.
    * **total** : int <br>
    Number of song objects.

  Example:
    
  ```sh
  curl -H "Accept: application/json" -X GET http://localhost:8080/songs/search?message=tHe%20yoUSicIaNs
  ```

- POST /songs/rating
  - Takes in parameter a "song_id" and a "rating"
  - This call adds a rating to the song. Ratings are between 1 and 5.
  
  @params:
    * **song_id** : string <br>
    Song ID for searching. Must be 24 characters.
    * **rating** : int <br>
    Should be beetween 1 and 5

    @return:
    * **updated** : boolean <br>
    If update is done it will return ```true```, otherwise returns ```false```.

  Example:
    
  ```sh
  curl -H "Accept: application/json" -X POST --data song_id=599f5b281e6d956381505bb1&rating=5 http://localhost:8080/songs/rating
  ```

- GET /songs/avg/rating/<song_id>
  - Returns the average, the lowest and the highest rating of the given song id.
  
  @params:
    * **song_id** : string <br>
    Song ID for searching. Must be 24 characters.

  @return:
    * **average_rating** : int <br>
    Average rating given to the song.
    * **max_rating** : int <br>
    Maximum rating value given to the song.
    * **min_rating** : int <br>
    Minimum rating value given to the song.
    
  Example:
    
  ```sh
  curl -H "Accept: application/json" -X GET http://localhost:8080/songs/avg/rating/599f5b281e6d956381505bb3
  ```
