Question 8 pprasad1
SELECT year, COUNT(*)
FROM IMDBMovie I, NPHDMovies N
WHERE I.title=N.title AND
PrimeVideo = 1 AND
I.Genre LIKE '%Drama%'
GROUP BY year
UNION
SELECT year, 'null'
FROM IMDBMovie I, NPHDMovies N
WHERE I.Genre NOT LIKE '%Drama%' AND
year NOT IN (SELECT year
                        FROM IMDBMovie I, NPHDMovies N
                        WHERE I.title=N.title AND
                        PrimeVideo = 1 AND
                        I.Genre LIKE '%Drama%'
                        GROUP BY year)
GROUP BY year;