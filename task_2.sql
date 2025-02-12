--Самый длинный трек
SELECT title, duration
FROM track
WHERE duration = (SELECT MAX(duration) FROM track);

--Треки не короче 3,5 минут (210 секунд)
SELECT title
FROM track
WHERE duration >= 210;

--Сборники 2018–2020
SELECT title
FROM collection
WHERE release_year BETWEEN 2018 AND 2020;

--Исполнители с именем из одного слова
SELECT name
FROM artist
WHERE name NOT LIKE '% %';

--Треки с «мой» или «my»
SELECT title
FROM track
WHERE LOWER(title) LIKE '%мой%' OR LOWER(title) LIKE '%my%';

