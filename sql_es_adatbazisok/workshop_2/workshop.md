# SQL és Adatbázisok Workshop II. (pgsql)

1. Mennyi közös `VIN` található a `TVin1` és `TVin2` tábla között?

		SELECT
			COUNT(*)
		FROM
			t_vin_1
		INNER JOIN
			t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin );

2. Mennyi `VIN` lenne, ha összeraknánk a `TVin1` és `TVin2` tábla tartalmát?

		SELECT
			COUNT( DISTINCT COALESCE( t_vin_1.vin, t_vin_2.vin ) )
		FROM
			t_vin_1
		FULL OUTER JOIN
			t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin );

3. Mennyi `VIN` van, ha összeraknánk a `TVin1` és `TVin2` tábla tartalmát, de a `TVin3`-ba levőket nem tennénk bele?

		SELECT
			COUNT( DISTINCT COALESCE( t_vin_1.vin, t_vin_2.vin ) )
		FROM
			t_vin_1
		FULL OUTER JOIN
			t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin )
		WHERE
			NOT EXISTS (
				SELECT
					1
				FROM
					t_vin_3
				WHERE
					t_vin_3.vin = COALESCE( t_vin_1.vin, t_vin_2.vin )
			);

4. Mennyi egyedi VIN, és összesen mennyi rekord található a `TVin1` .. `TVin5` táblákban?

		SELECT 'TVin1', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_1
		UNION ALL
		SELECT 'TVin2', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_2
		UNION ALL
		SELECT 'TVin3', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_3
		UNION ALL
		SELECT 'TVin4', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_4
		UNION ALL
		SELECT 'TVin5', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_5;

5. Összesen mennyi egyedi VIN áll rendelkezésünkre a különböző fájlokban?

		WITH 
		merged AS (
			SELECT * FROM t_vin_1
			UNION ALL
			SELECT * FROM t_vin_2
			UNION ALL
			SELECT * FROM t_vin_3
			UNION ALL
			SELECT * FROM t_vin_4
			UNION ALL
			SELECT * FROM t_vin_5
		)
		
		SELECT COUNT( DISTINCT vin ) FROM merged;

6. UNION vs UNION ALL, mi különbség?
	
		WITH 
		merged AS (
			SELECT * FROM t_vin_1
			UNION
			SELECT * FROM t_vin_2
			UNION
			SELECT * FROM t_vin_3
			UNION
			SELECT * FROM t_vin_4
			UNION
			SELECT * FROM t_vin_5
		)
		
		SELECT COUNT(*) FROM merged;

7. Pakoljuk össze az értékeket egy `TVIn` táblába, hogy minden `VIN` egyszer szerepeljen, az utolsó `date_of_contact`-al.

		WITH 
		merged AS (
			SELECT * FROM t_vin_1
			UNION ALL
			SELECT * FROM t_vin_2
			UNION ALL
			SELECT * FROM t_vin_3
			UNION ALL
			SELECT * FROM t_vin_4
			UNION ALL
			SELECT * FROM t_vin_5
		)
		
		SELECT
			DISTINCT ON( vin )
			vin,
			date_of_contact,
			firstname,
			lastname
		INTO
			t_vin
		FROM
			merged
		WHERE
			vin IS NOT NULL
		ORDER BY
			1, 2 DESC NULLS LAST;

8. Mennyi olyan `VIN` található, amelyik 17 karakter hosszú és a 7-9 karekterek `K12`-t tartalmaznak?

		SELECT
			COUNT(*)
		FROM
			t_vin
		WHERE
			LENGTH(vin) = 17
			AND
			vin ILIKE '______K12________';

9. Mennyi olyan `VIN` van, ahol legalább az első 3 karakter nem betű és az utolsó 7 karakter nem szám, vagy nem 17 karakter hosszú?

		SELECT
			COUNT(*)
		FROM
			t_vin
		WHERE
			LENGTH(vin) != 17
			OR
			vin NOT SIMILAR TO '[A-Z]{3,}%[0-9]{7}';

10. Írjunk egy lekérdezést a `TUser` táblán, mely megmondja kinek-ki a szülő rekordja.

		WITH RECURSIVE 
		first_level AS (
		    (
		        SELECT 
		            id, 
		            firstname,
		            lastname, 
		            parent_id, 
		            array[id] AS path, 
		            array_length(array[id], 1) as p_length 
		        FROM 
		            t_user
		        WHERE
		            parent_id IS NULL
		    )
		    UNION
		    (
		        SELECT 
		            e.id, 
		            e.firstname,
		            e.lastname, 
		            e.parent_id, 
		            (fl.path || e.id), 
		            array_length(fl.path || e.id, 1) as p_length
		        FROM
		            (
		                SELECT 
		                    id, 
		                    firstname,
		                    lastname,
		                    parent_id 
		                FROM 
		                    t_user
		            ) AS e, 
		            first_level AS fl
		        WHERE 
		            e.parent_id = fl.id
		    )
		)
		
		SELECT 
		    * 
		FROM 
		    first_level 
		ORDER BY 
		    path;