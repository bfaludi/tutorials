# SQL és Adatbázisok Workshop I.


1. Másold le az adatbázist `<prefix>_email_history` és `<prefix>_user` néven.

		SELECT * INTO bfaludi_user FROM workshop_1.t_user;
		SELECT * INTO bfaludi_email_history FROM workshop_1.t_email_history;
	
2. Mondjátok meg hány `User` van.

3. Mondjátok meg, hogy hány olyan `User` van, ahol az `updated` korábbi, mint a `created`.
	
4. Cseréljük fel ezeknél a hibás eseteknél a `created`-et és az `update`-et.
		
5. Mondjuk meg hány egyedi `Email` cím található a rendszerben.
	
6. Mondjuk meg hány emberhez tartozik `Email` cím.
		
7. Kikhez tartozik több mint 4db `Email` cím?

8. Mi az utolsó (legfrissebb updated, vagy ha az nincs legfrissebb created alapján) `Email` cím minden emberhez?
			
9. ... és ha az utolsó három email címet szeretnénk megkapni?

10. Szeretnénk a legfrisebb `Email` címet befrissíteni a `User` alá. Hogy tudjuk megtenni?

11. Mondjuk meg hogy mennyi `Email` cím került be havi bontásban a rendszerbe.

12. Adjuk meg minden `User`-hez, hogy mely `Email` címek kerültek be hozzá az elmúlt két hónapban.

13. Hasonlítsuk össze a `User`-eket az alapján hogy azonos `Email` címük van-e és legalább az egyik név tagjuk megegyezik.

14. Előbbi feladat kiegészítve, hogy az aktuális `Email` cím mellett vizsgáljuk az utóbbi két hónapban felvitt `Email` címeket is. Ha volt közös email cím tekintsük találatnak.

