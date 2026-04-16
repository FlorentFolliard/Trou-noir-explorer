-- Requêtes SQL pour skyserver.sdss (1ere requête : 5000 étoiles, 2eme requête : 5000 quasars)
-- Cette requête nous permet d'avoir un .csv de base qui contient les données brutes de 5000 étoiles et 5000 quasars.
-- On veut autant d'étoiles que de quasars pour mieux identifier les données qui caractérisent les étoiles et les torus noirs.

SELECT TOP 5000
    p.objid, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z, s.class, s.z as redshift
FROM PhotoObj AS p
JOIN SpecObj AS s ON p.objid = s.bestObjID
WHERE s.class = 'STAR' 
  AND p.u BETWEEN 0 AND 30
  AND p.g BETWEEN 0 AND 30

------------------------------------

  SELECT TOP 5000
    p.objid, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z, s.class, s.z as redshift
FROM PhotoObj AS p
JOIN SpecObj AS s ON p.objid = s.bestObjID
WHERE s.class = 'QSO' 
  AND p.u BETWEEN 0 AND 30
  AND p.g BETWEEN 0 AND 30