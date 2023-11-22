Question 7 pprasad1
SELECT Title
FROM IMDBMovie
WHERE INSTR(Actors, Director) AND Title IN
(SELECT Title
FROM NPHDMovies
WHERE Netflix = 0 AND Hulu = 0 AND PrimeVideo = 0 AND Disney = 0
UNION
SELECT Title
FROM IMDBMovie
WHERE Title NOT IN (SELECT Title
FROM NPHDMovies));