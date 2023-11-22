Question 9 pprasad1
SELECT 'Netflix', I.title,MAX( I.revenue)
FROM IMDBMovie I, NPHDMovies N
WHERE I.title = N.title AND
Netflix = 1
UNION
SELECT 'Hulu', I.title,MAX( I.revenue)
FROM IMDBMovie I, NPHDMovies N
WHERE I.title = N.title AND
Hulu = 1
UNION
SELECT 'PrimeVideo', I.title,MAX( I.revenue)
FROM IMDBMovie I, NPHDMovies N
WHERE I.title = N.title AND
PrimeVideo = 1
UNION
SELECT 'Disney', I.title,MAX( I.revenue)
FROM IMDBMovie I, NPHDMovies N
WHERE I.title = N.title AND
Disney = 1;