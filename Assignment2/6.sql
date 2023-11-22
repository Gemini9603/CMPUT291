Question 6 pprasad1
SELECT I.Director
FROM IMDBMovie I, NPHDMovies N
WHERE I.title = N.title AND
N.Disney = 1
GROUP BY I.Director
HAVING COUNT(*) > 1;
