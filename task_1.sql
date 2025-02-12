-- Исполнители
INSERT INTO artist (id, name) 
VALUES 
(1, 'The Beatles'),
(2, 'Queen'),
(3, 'Taylor Swift'),
(4, 'Linkin Park');

-- Жанры
INSERT INTO genre (id, name)
VALUES
(1, 'Rock'),
(2, 'Pop'),
(3, 'Jazz');

-- Альбомы
INSERT INTO album (id, title, release_year)
VALUES
(1, 'Abbey Road', 1969),
(2, 'A Night at the Opera', 1975),
(3, 'Folklore', 2020);

-- Треки
INSERT INTO track (id, title, duration, album_id)
VALUES
(1, 'Come Together', 259, 1),
(2, 'Bohemian Rhapsody', 354, 2),
(3, 'My Tears Ricochet', 219, 3),
(4, 'In the End', 216, 4),
(5, 'Hey Jude', 431, 1),
(6, 'Love Story', 235, 3);

-- Сборники
INSERT INTO collection (id, title, release_year)
VALUES
(1, 'Best of Rock', 2018),
(2, 'Pop Hits', 2019),
(3, 'Golden Classics', 2020),
(4, 'Modern Mix', 2021);

-- Связи (примеры)
INSERT INTO artist_genre (artist_id, genre_id)
VALUES
(1, 1), (2, 1), (3, 2), (4, 1);

INSERT INTO artist_album (artist_id, album_id)
VALUES
(1, 1), (2, 2), (3, 3), (4, 4);

INSERT INTO collection_track (collection_id, track_id)
VALUES
(1, 1), (1, 2), (2, 3), (2, 6), (3, 5), (4, 4);