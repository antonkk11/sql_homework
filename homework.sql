CREATE TABLE IF NOT EXISTS genres (
id SERIAL PRIMARY KEY,
name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS artists (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS artist_genres (
artist_id INTEGER REFERENCES artists(id),
genre_id INTEGER REFERENCES genres(id),
PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE IF NOT EXISTS albums (
id SERIAL PRIMARY KEY,
title VARCHAR(100) NOT NULL,
release_year INTEGER NOT NULL
artists_name INTEGER REFERENCES artists(id)
);

CREATE TABLE IF NOT EXISTS album_artists (
album_id INTEGER REFERENCES albums(id),
artist_id INTEGER REFERENCES artists(id),
PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE IF NOT EXISTS tracks (
id SERIAL PRIMARY KEY,
title VARCHAR(100) NOT NULL,
duration INTEGER NOT NULL,
album_id INTEGER REFERENCES albums(id)
);

CREATE TABLE IF NOT EXISTS collections (
id SERIAL PRIMARY KEY,
title VARCHAR(100) NOT NULL,
year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS collection_tracks (
collection_id INTEGER REFERENCES collections(id),
track_id INTEGER REFERENCES tracks(id),
PRIMARY KEY (collection_id, track_id)
);