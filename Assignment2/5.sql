Question 5 pprasad1
SELECT COUNT(N.Title)
FROM IMDBMovie I, NPHDMovies N
WHERE I.title = N.title AND
N.Netflix = 1 AND N.Hulu = 0 AND N.PrimeVideo = 0 AND N.Disney = 0 AND
I.Genre LIKE '%Drama%';
