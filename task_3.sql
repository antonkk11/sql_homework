-- Количество исполнителей в каждом жанре
SELECT g.name AS genre, COUNT(ag.artist_id) AS artists_count
FROM genre g
LEFT JOIN artist_genre ag ON g.id = ag.genre_id
GROUP BY g.name;

-- Количество треков, вошедших в альбомы 2019–2020 годов
SELECT COUNT(t.id) AS tracks_count
FROM track t
JOIN album a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

-- Средняя продолжительность треков по каждому альбому
SELECT a.title AS album, ROUND(AVG(t.duration)) AS avg_duration_sec
FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY a.title;

-- Исполнители, которые не выпустили альбомы в 2020 году
SELECT ar.name AS artist
FROM artist ar
WHERE ar.id NOT IN (
  SELECT aa.artist_id
  FROM artist_album aa
  JOIN album a ON aa.album_id = a.id
  WHERE a.release_year = 2020
);

-- Названия сборников, в которых присутствует Queen
SELECT DISTINCT c.title AS collection
FROM collection c
JOIN collection_track ct ON c.id = ct.collection_id
JOIN track t ON ct.track_id = t.id
JOIN album a ON t.album_id = a.id
JOIN artist_album aa ON a.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE ar.name = 'Queen';