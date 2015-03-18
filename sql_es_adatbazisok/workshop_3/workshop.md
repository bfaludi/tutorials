# SQL és Adatbázisok Workshop III. (mysql)

1. Másold le a t_user táblát <prefix>_user néven.

		CREATE TABLE bfaludi_user SELECT * FROM t_user;

2. Mondjátok meg hány `User` van.

		SELECT COUNT(*) FROM t_user;

3. Mondjátok meg, hogy hány olyan `User` van, ahol az `updated` korábbi, mint a `created`.

		SELECT COUNT(*) FROM t_user WHERE updated < created;
		
4. Cseréljük fel ezeknél a hibás eseteknél a `created`-et és az `update`-et.

		UPDATE t_user 
		SET created = updated, updated = created 
		WHERE updated < created;
		
5. Mondjuk meg hány egyedi `Email` cím található a rendszerben.

		SELECT COUNT( DISTINCT email ) FROM t_email_history;
		
6. Mondjuk meg hány emberhez tartozik `Email` cím.

		SELECT COUNT( DISTINCT user_id ) FROM t_email_history;
		
7. Kikhez tartozik több mint 4db `Email` cím?
		
		SELECT user_id
		FROM bfaludi_email_history
		GROUP BY 1
		HAVING COUNT(*) > 4

8. Mi az utolsó (legfrissebb updated, vagy ha az nincs legfrissebb created alapján) `Email` cím minden emberhez?

		SELECT 
			user_id,
			email
		FROM 
			( 
				SELECT 
					*
				FROM
					t_email_history
				ORDER BY
					COALESCE( updated, created ) DESC
			) AS t
		GROUP BY
			user_id;
			
9. ... és ha az utolsó három email címet szeretnénk megkapni?

		SELECT 
			user_id,
			email,
			row_number
		FROM
			( 
				SELECT
					user_id, 
					email,
					@row_num := IF(@prev_value=user_id,@row_num+1,1) AS row_number,
					@prev_value := user_id
				FROM 
					t_email_history,
					(SELECT @row_num := 1) x,
					(SELECT @prev_value := '') y
				ORDER BY 
					user_id, COALESCE( updated, created ) DESC
			) AS t
		WHERE
			row_number <= 3;

10. Szeretnénk a legfrisebb `Email` címet befrissíteni a `User` alá. Hogy tudjuk megtenni?

		UPDATE
			t_user AS u
		LEFT JOIN
			(
				SELECT 
					user_id,
					email
				FROM 
					( 
						SELECT 
							*
						FROM
							t_email_history
						ORDER BY
							COALESCE( updated, created ) DESC
					) AS t
				GROUP BY
					user_id
			) AS vw ON ( vw.user_id = u.id )
		SET
			u.email = vw.email;

11. Mondjuk meg hogy mennyi `Email` cím került be havi bontásban a rendszerbe.

		SELECT
			YEAR( COALESCE( updated, created ) ) AS "year",
			MONTH(COALESCE( updated, created ) ) AS "month",
			COUNT(*)
		FROM
			t_email_history
		GROUP BY
			1, 2
		ORDER BY
			1, 2;

12. Adjuk meg minden `User`-hez, hogy mely `Email` címek kerültek be hozzá az elmúlt két hónapban.

		SELECT
			user_id,
			GROUP_CONCAT( email ) AS "emails"
		FROM
			t_email_history
		WHERE
			COALESCE( updated, created ) >= DATE_SUB( CURDATE(), INTERVAL 2 MONTH )
		GROUP BY
			user_id;

13. Hasonlítsuk össze a `User`-eket az alapján hogy azonos `Email` címük van-e és legalább az egyik név tagjuk megegyezik.

		SELECT
			*
		FROM
			t_user AS u1
		INNER JOIN
			t_user AS u2 ON ( u1.id > u2.id )
		WHERE
			u1.email = u2.email
			AND
			(
				u1.firstname = u2.firstname
				OR
				u1.lastname = u2.lastname
			);
			
14. Előbbi feladat kiegészítve, hogy az aktuális `Email` cím mellett vizsgáljuk az utóbbi két hónapban felvitt Email címeket is. Ha volt közös email cím tekintsük találatnak.

	Nem nézünk rá példát, mivel megvalósítása horror, hisz a MySQL nem kezeli az ARRAY típust, így overlap-ot string-ek között kellene nézni. Megoldásához sok Temporary tábla szükséges, vagy nagyon sok halmazműveleti függvény.

15. Mennyi közös `VIN` található a `TVin1` és `TVin2` tábla között?

		SELECT
			COUNT(*)
		FROM
			t_vin_1
		INNER JOIN
			t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin );

16. Mennyi `VIN` lenne, ha összeraknánk a `TVin1` és `TVin2` tábla tartalmát?

		SELECT
			COUNT( DISTINCT vin )
		FROM
		(
			SELECT
				COALESCE( t_vin_1.vin, t_vin_2.vin ) vin
			FROM
				t_vin_1
			LEFT JOIN
				t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin )
			UNION
			SELECT
				COALESCE( t_vin_1.vin, t_vin_2.vin ) vin
			FROM
				t_vin_1
			RIGHT JOIN
				t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin )
		) AS vw;

17. Mennyi `VIN` van, ha összeraknánk a `TVin1` és `TVin2` tábla tartalmát, de a `TVin3`-ba levőket nem tennénk bele?

		SELECT
			COUNT( DISTINCT vw.vin )
		FROM
		(
			SELECT
				COALESCE( t_vin_1.vin, t_vin_2.vin ) vin
			FROM
				t_vin_1
			LEFT JOIN
				t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin )
			UNION
			SELECT
				COALESCE( t_vin_1.vin, t_vin_2.vin ) vin
			FROM
				t_vin_1
			RIGHT JOIN
				t_vin_2 ON ( t_vin_1.vin = t_vin_2.vin )
		) AS vw
		WHERE
			NOT EXISTS (
				SELECT
					1
				FROM
					t_vin_3
				WHERE
					t_vin_3.vin = vw.vin
			);

18. Mennyi egyedi VIN, és összesen mennyi rekord található a `TVin1` .. `TVin5` táblákban?

		SELECT 'TVin1', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_1
		UNION ALL
		SELECT 'TVin2', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_2
		UNION ALL
		SELECT 'TVin3', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_3
		UNION ALL
		SELECT 'TVin4', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_4
		UNION ALL
		SELECT 'TVin5', COUNT( DISTINCT vin ), COUNT(*) FROM t_vin_5;

19. Összesen mennyi egyedi VIN áll rendelkezésünkre a különböző fájlokban?

		SELECT COUNT( DISTINCT vin ) 
		FROM 
		(
			SELECT * FROM t_vin_1
			UNION ALL
			SELECT * FROM t_vin_2
			UNION ALL
			SELECT * FROM t_vin_3
			UNION ALL
			SELECT * FROM t_vin_4
			UNION ALL
			SELECT * FROM t_vin_5
		) vw;

20. Pakoljuk össze az értékeket egy `TVIn` táblába, hogy minden `VIN` egyszer szerepeljen, az utolsó `date_of_contact`-al.

		CREATE TABLE t_vin
		SELECT
			vin,
			date_of_contact,
			firstname,
			lastname
		FROM
			( 
				SELECT
					vw.vin,
					vw.date_of_contact,
					vw.firstname,
					vw.lastname
				FROM 
					(
						SELECT * FROM t_vin_1
						UNION ALL
						SELECT * FROM t_vin_2
						UNION ALL
						SELECT * FROM t_vin_3
						UNION ALL
						SELECT * FROM t_vin_4
						UNION ALL
						SELECT * FROM t_vin_5
					) AS vw
				WHERE
					vw.vin IS NOT NULL
				ORDER BY
					1,2 DESC
			) AS t
		GROUP BY
			vin;

21. Mennyi olyan `VIN` található, amelyik 17 karakter hosszú és a 7-9 karekterek `K12`-t tartalmaznak?

		SELECT
			COUNT(*)
		FROM
			t_vin
		WHERE
			CHAR_LENGTH(vin) = 17
			AND
			UPPER(vin) LIKE '______K12________';

22. Mennyi olyan `VIN` van, ahol legalább az első 3 karakter nem betű és az utolsó 7 karakter nem szám, vagy nem 17 karakter hosszú?

		SELECT
			*
		FROM
			t_vin
		WHERE
			CHAR_LENGTH(vin) != 17
			OR
			vin NOT REGEXP '^[A-Z]{3,}.*[0-9]{7}$';

23. Írjunk egy lekérdezést a `TUser` táblán, mely megmondja kinek-ki a szülő rekordja.

		DELIMITER $$
		CREATE FUNCTION hierarchy_connect_by_parent_eq_prior_id(value INT) RETURNS INT
		NOT DETERMINISTIC
		READS SQL DATA
		BEGIN
		    DECLARE _id INT;
		    DECLARE _parent INT;
		    DECLARE _next INT;
		    DECLARE CONTINUE HANDLER FOR NOT FOUND SET @id = NULL;
		
		    SET _parent = @id;
		    SET _id = -1;
		
		    IF @id IS NULL THEN
		        RETURN NULL;
		    END IF;
		
		    LOOP
		        SELECT MIN(id)
		        INTO  @id
		        FROM t_hierarcy_user
		        WHERE parent_id = _parent AND id > _id;
		
		        IF @id IS NOT NULL OR _parent = @start_with THEN
		            SET @level = @level + 1;
		            RETURN @id;
		        END IF;
		
		        SET @level := @level - 1;
		        SELECT id, parent_id
		        INTO _id, _parent
		        FROM t_hierarcy_user
		        WHERE id = _parent;
		    END LOOP;       
		END $$
		DELIMITER ;
		
		SELECT 
			CONCAT(REPEAT('    ', level-1), 
			CAST(hi.id AS CHAR)) AS treeitem, 
			parent_id, 
			level
		FROM
			(
		        SELECT
					hierarchy_connect_by_parent_eq_prior_id(id) AS id, 
					@level AS level
		        FROM 
					(
		                SELECT  
							@start_with := 0,
		                    @id := @start_with,
		                    @level := 0
		            ) vars, 
					t_hierarcy_user
		        WHERE
					@id IS NOT NULL
		    ) AS ho
		JOIN
			t_hierarcy_user AS hi ON ( hi.id = ho.id );