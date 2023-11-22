Question 4 pprasad1
SELECT COUNT(*)
FROM NPHDMovies
WHERE Netflix*Hulu*PrimeVideo=1 OR Netflix*Hulu*Disney=1 OR
Netflix*PrimeVideo*Disney=1 OR Hulu*PrimeVideo*Disney=1;
