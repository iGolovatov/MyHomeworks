-- 1. Лысые злодеи 90-х годов
SELECT name, APPEARANCES, Year
FROM MarvelCharacters
WHERE HAIR LIKE 'Bald'
    AND ALIGN LIKE 'Bad Characters'
    AND Year BETWEEN 1990 AND 1999
ORDER BY Year;

-- 2. Герои с тайной идентичностью и необычными глазами
-- На выходе получилось 1028 строк (в задании 1027)
SELECT name, Year, EYE
FROM MarvelCharacters
WHERE identify LIKE '%Secret%'
    AND EYE NOT IN ('Blue Eyes', 'Brown Eyes', 'Green Eyes')
    AND Year IS NOT NULL
ORDER BY Year;

-- 3. Персонажи с изменяющимся цветом волос
SELECT name, HAIR
FROM MarvelCharacters
WHERE HAIR LIKE '%Variable Hair%'
ORDER BY HAIR;

-- 4. Женские персонажи с редким цветом глаз
SELECT name, EYE
FROM MarvelCharacters
WHERE SEX LIKE '%Female Characters%'
    AND EYE IN ('Gold Eyes', 'Amber Eyes')
ORDER BY EYE;

-- 5. Персонажи без двойной идентичности, сортированные по году появления
SELECT name, FIRST_APPEARANCE
FROM MarvelCharacters
WHERE IDENTIFY LIKE '%No Dual Identity%'
ORDER BY FIRST_APPEARANCE DESC;

-- 6. Герои и злодеи с необычными прическами
SELECT name, align, HAIR
FROM MarvelCharacters
WHERE HAIR NOT IN ('Brown Hair', 'Black Hair', 'Blond Hair', 'Red Hair')
    AND align IN ('Good Characters', 'Bad Characters')
ORDER BY name;

-- 7. Персонажи, появившиеся в определенное десятилетие
SELECT name, Year
FROM MarvelCharacters
WHERE Year BETWEEN 1960 AND 1969
ORDER BY Year;

-- 8. Персонажи с уникальным сочетанием цвета глаз и волос
SELECT name, EYE, HAIR
FROM MarvelCharacters
WHERE EYE IN ('Yellow Eyes')
    AND HAIR IN ('Red Hair')
ORDER BY name;

-- 9. Персонажи с ограниченным количеством появлений
SELECT name, APPEARANCES
FROM MarvelCharacters
WHERE APPEARANCES < 10
ORDER BY APPEARANCES DESC;

-- 10. Персонажи с наибольшим количеством появлений
SELECT name, APPEARANCES
FROM MarvelCharacters
ORDER BY APPEARANCES DESC
LIMIT 5;


