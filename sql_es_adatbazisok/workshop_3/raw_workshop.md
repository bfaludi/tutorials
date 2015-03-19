# SQL és Adatbázisok Workshop III. (mysql)

1. Másold le a `t_user` táblát `<prefix>_user` néven.

		CREATE TABLE bfaludi_user SELECT * FROM t_user;

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

14. Előbbi feladat kiegészítve, hogy az aktuális `Email` cím mellett vizsgáljuk az utóbbi két hónapban felvitt Email címeket is. Ha volt közös email cím tekintsük találatnak.
	
15. Mennyi közös `VIN` található a `TVin1` és `TVin2` tábla között?

16. Mennyi `VIN` lenne, ha összeraknánk a `TVin1` és `TVin2` tábla tartalmát?

17. Mennyi `VIN` van, ha összeraknánk a `TVin1` és `TVin2` tábla tartalmát, de a `TVin3`-ba levőket nem tennénk bele?

18. Mennyi egyedi VIN, és összesen mennyi rekord található a `TVin1` .. `TVin5` táblákban?

19. Összesen mennyi egyedi VIN áll rendelkezésünkre a különböző fájlokban?

20. Pakoljuk össze az értékeket egy `TVIn` táblába, hogy minden `VIN` egyszer szerepeljen, az utolsó `date_of_contact`-al.

21. Mennyi olyan `VIN` található, amelyik 17 karakter hosszú és a 7-9 karekterek `K12`-t tartalmaznak?

22. Mennyi olyan `VIN` van, ahol legalább az első 3 karakter nem betű és az utolsó 7 karakter nem szám, vagy nem 17 karakter hosszú?

23. Írjunk egy lekérdezést a `TUser` táblán, mely megmondja kinek-ki a szülő rekordja.
