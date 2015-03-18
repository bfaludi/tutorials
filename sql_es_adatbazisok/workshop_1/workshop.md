# SQL és Adatbázisok Workshop I. (pgsql)


1. Másold le az adatbázist `<prefix>_email_history` és `<prefix>_user` néven.

		SELECT * INTO bfaludi_user FROM workshop_1.t_user;
		SELECT * INTO bfaludi_email_history FROM workshop_1.t_email_history;
	
2. Mondjátok meg hány `User` van.

		SELECT COUNT(*) FROM bfaludi_user;

3. Mondjátok meg, hogy hány olyan `User` van, ahol az `updated` korábbi, mint a `created`.

		SELECT COUNT(*) FROM bfaludi_user WHERE updated < created;
		
4. Cseréljük fel ezeknél a hibás eseteknél a `created`-et és az `update`-et.

		UPDATE bfaludi_user 
		SET created = updated, updated = created 
		WHERE updated < created;
		
5. Mondjuk meg hány egyedi `Email` cím található a rendszerben.

		SELECT COUNT( DISTINCT email ) FROM bfaludi_email_history;
		
6. Mondjuk meg hány emberhez tartozik `Email` cím.

		SELECT COUNT( DISTINCT user_id ) FROM bfaludi_email_history;
		
7. Kikhez tartozik több mint 4db `Email` cím?
		
		SELECT user_id
		FROM bfaludi_email_history
		GROUP BY 1
		HAVING COUNT(*) > 4

8. Mi az utolsó (legfrissebb updated, vagy ha az nincs legfrissebb created alapján) `Email` cím minden emberhez?

		SELECT 
			DISTINCT ON ( user_id )
			user_id,
			email
		FROM 
			bfaludi_email_history
		ORDER BY
			1, COALESCE( updated, created ) DESC;
			
9. ... és ha az utolsó három email címet szeretnénk megkapni?

		WITH 
		subq AS (
			SELECT 
				user_id,
				email,
				ROW_NUMBER() OVER (
					PARTITION BY
						user_id
					ORDER BY
						COALESCE( updated, created ) DESC
				) AS "row_number"
			FROM 
				bfaludi_email_history
		)
		
		SELECT *
		FROM subq
		WHERE row_number <= 2;

10. Szeretnénk a legfrisebb `Email` címet befrissíteni a `User` alá. Hogy tudjuk megtenni?

		WITH
		subq AS (
			SELECT 
				DISTINCT ON ( user_id )
				user_id,
				email AS "new_email"
			FROM 
				bfaludi_email_history
			ORDER BY
				1, COALESCE( updated, created ) DESC
		)
		
		UPDATE bfaludi_user
		SET email = subq.new_email
		FROM subq
		WHERE subq.user_id = bfaludi_user.id;

11. Mondjuk meg hogy mennyi `Email` cím került be havi bontásban a rendszerbe.

		SELECT
			DATE_PART('year', COALESCE( updated, created ) ) AS "year",
			DATE_PART('month', COALESCE( updated, created ) ) AS "month",
			COUNT(*)
		FROM
			bfaludi_email_history
		GROUP BY
			1, 2
		ORDER BY
			1, 2;

12. Adjuk meg minden `User`-hez, hogy mely `Email` címek kerültek be hozzá az elmúlt két hónapban.

		SELECT
			user_id,
			ARRAY_AGG( email ) AS "emails"
		FROM
			bfaludi_email_history
		WHERE
			COALESCE( updated, created ) >= CURRENT_TIMESTAMP - interval '2 month'
		GROUP BY
			user_id;

13. Hasonlítsuk össze a `User`-eket az alapján hogy azonos `Email` címük van-e és legalább az egyik név tagjuk megegyezik.

		SELECT
			*
		FROM
			bfaludi_user AS u1
		INNER JOIN
			bfaludi_user AS u2 ON ( u1.id > u2.id )
		WHERE
			u1.email = u2.email
			AND
			(
				u1.firstname = u2.firstname
				OR
				u1.lastname = u2.lastname
			);

14. Előbbi feladat kiegészítve, hogy az aktuális `Email` cím mellett vizsgáljuk az utóbbi két hónapban felvitt `Email` címeket is. Ha volt közös email cím tekintsük találatnak.

		WITH
		emails AS (
			SELECT
				user_id,
				ARRAY_AGG( email ) AS "emails"
			FROM
				bfaludi_email_history
			WHERE
				COALESCE( updated, created ) >= CURRENT_TIMESTAMP - interval '2 month'
			GROUP BY
				user_id
		),
		
		user_emails AS (
			SELECT
				u.*,
				ARRAY_APPEND( emails.emails, u.email ) AS "emails"
			FROM
				bfaludi_user AS u
			LEFT OUTER JOIN
				emails ON ( u.id = emails.user_id )
			WHERE
				u.email IS NOT NULL
		)
		
		SELECT
			*
		FROM
			user_emails AS u1
		INNER JOIN
			user_emails AS u2 ON ( u1.id > u2.id )
		WHERE
			u1.emails && u2.emails
			AND
			(
				u1.firstname = u2.firstname
				OR
				u1.lastname = u2.lastname
			);

