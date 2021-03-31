import mysql.connector

#====================Edit these details to fit your project======
hostName     = "sql4.freemysqlhosting.net"
userName     = "sql4401825"  #Change username to database username
passWord     = "7XBYZbyhdS"           #Change password to database password
databaseName = "sql4401825"      #Change database name to correct database for your project

#======DO NOT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING========
#=================CREATE DATABASE======================
# Connect to the MySQL Database.
mydb = mysql.connector.connect(
	host     = hostName,
	user     = userName,
	password = passWord
)

mycursor = mydb.cursor()

# Prints out current existing databases.
print("Databases: ")
mycursor.execute("SHOW DATABASES")
for x in mycursor:
	print(x[0])

#Doping database MYDATABASE if already exists.
mycursor.execute("DROP database IF EXISTS sql4401825")

# Create the database "manga"
mycursor.execute( "CREATE DATABASE sql4401825")

mydb.close()

#=================END CREATE DATABASE======================
#=================CREATE TABLES============================

mydb = mysql.connector.connect(
	host     = hostName,
	user     = userName,
	password = passWord,
	database = databaseName
)

mycursor = mydb.cursor()

mycursor.execute(
	"""CREATE TABLE genre (ID INT(100) NOT NULL, 
		Category VARCHAR(100) NOT NULL, 
		PRIMARY KEY (ID)
		)
	"""
)

mycursor.execute(
	"""CREATE TABLE manga (
		ID INT(100) NOT NULL AUTO_INCREMENT,
		Name varchar(100) NOT NULL,
		Author varchar(100) NOT NULL,
		Artist varchar(100) NOT NULL,
		Publication varchar(100) NOT NULL,
  		Status varchar(100) NOT NULL,
  		Description varchar(1000) NOT NULL,
  		Rating varchar(100) NOT NULL,
  		Ename varchar(100) NOT NULL,
  		ImageUrl varchar(300) NOT NULL,
		PRIMARY KEY (ID)
		)
	"""
)

mycursor.execute(
	"""
	CREATE TABLE manga_genre (
		manga_id int(11) NOT NULL,
  		genre_id int(11) NOT NULL,
  		PRIMARY KEY (manga_id, genre_id),
  		KEY genre_id (genre_id)
	)
	"""
)

#=================END CREATE TABLES========================
#=================INSERT INTO DATABASE=====================


genre_names_sql = "INSERT INTO genre (ID, Category) VALUES (%s,%s)"
genre_name_values = [
	(1, 'Action'),
	(2, 'Adventure'),
	(3, 'Comedy'),
	(4, 'Sport'),
	(5, 'Drama'),
	(6, 'Romance'),
	(7, 'Sci fi'),
	(8, 'Tragedy'),
	(9, 'Isekai'),
	(10,'Slice of Life'),
	(11, 'Fantasy')
]

mycursor.executemany(genre_names_sql, genre_name_values)
mydb.commit()
print(mycursor.rowcount, "was inserted into 'Genre'.")


manga_sql = "INSERT INTO manga (Name, Author, Artist, Publication, Status, Description, Rating, Ename, ImageUrl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
manga_values_sql = [
	('Arifureta Shokugyou de Sekai Saikyou Zero', 'Ryo Shirakome', 'Ataru Kamichi', '2018', 'Completed', 'This is the story of what happened long before Hajime was summoned to Tortus. Oscar Orcus is considered a third-rate Synergist by most people. He spends his days peacefully, working so he can send money back to an orphanage.All that changes when the whirlwind that is Miledi Reisen storms into his life. Miledi sees the hidden potential in Oscar, and invites him on her journey to defeat the gods. Oscar wants no part of any journey, and he refuses. But Miledi is persistent, and the situation changes drastically when the orphanage he wants to protect is attacked. In the end, what will our unlikely hero decide?', '7.4', 'Arifureta: From Commonplace to Worlds Strongest', 'https://storage.googleapis.com/mangaudible/temp/arifureta_shokugyou_de_sekai_s.jpg'),
	('Grand Blue', 'Kenji Inoue', 'Kimitake Yoshioka', '2020', 'Ongoing', 'A new life begins for Iori Kitahara as he begins his college career near the ocean in Izu city, full of excitement for his new life. He will be moving into his uncle\'\'s diving store Grand Blue. There he finds the beautiful ocean, beautiful women, and men that love diving and alcohol. Will Iori be able to live his dream college life?', '7.8', 'Grand Blue', 'https://storage.googleapis.com/mangaudible/temp/grand_blue.jpg'),
	('Imadoki no Wakai Mon wa', 'Yoshitani Kouhei', 'Yoshitani Kouhei', '2018', 'Completed', 'A sweet story of the overworked office employee Ayumi Mugita and her unexpectedly kind boss section-chief Hajime Ishizawa.', '6', 'The problem with kids these days', 'https://storage.googleapis.com/mangaudible/temp/imadoki_no_wakai_mon_wa.jpg'),
	('Isekai Tensei Soudouki', 'Takami Ryousen', 'Honoji', '2015', 'Ongoing', 'Balud Cornelius is the son of a noble of the Mauricia kingdom and inside him also dwell the souls of the warring states commander Oka Sadatoshi and animal ear otaku high schooler Oka Masaharu. With these 3 souls in a single body, he can exhibit extraordinary abilities when it comes to combat or managing the domain.', '8.43', 'Different World Reincarnation Riot Report', 'https://storage.googleapis.com/mangaudible/temp/isekai_tensei_soudouki.jpg'),
	('Karate Baka Isekai', 'Terui Elito', 'Jiro Tsunoda', '2019', 'Ongoing', 'A karate practitioner who has been transferred to another world refuses the cheat skills given by the goddess and he pursues his own karate in another world.', '6.6', 'Karate Idiot in Another World', 'https://storage.googleapis.com/mangaudible/temp/karate_baka_isekai.jpg'),
	('Kateikyoushi no Lelouch-san', 'Shitsukon', 'Urushisaki Kokoro', '2018', 'Ongoing', 'Lelouch and Nunnally lived in peace, until one day when C.C. — a spoiled young aristocrat with less common sense than a rock — moved in next door. And now at the bequest of his mother, Marianne, Lelouch has accepted responsibility for C.C.\'\'s education and entered into a contract to be her personal tutor...?! Ready, set, go — it is a lighthearted high school AU!', '8.5', 'Lelouch the Tutor', 'https://storage.googleapis.com/mangaudible/temp/kateikyoushi_no_lelouch-san.jpg'),
	('Koroshi Ai', 'Fe', 'Fe', '2015', 'Ongoing', 'The silent and stoic Chateau Dankworth is a bounty hunter. Her target: Son Ryang-ha, a notorious killer known for killing 18 high-class officials in a single night. To this day, his murders remain swift, efficient, and bloody. However, after Son Ryang-ha overpowers Chateau in their first encounter, he reveals his own intentions: he too is after her, aiming for her heart.Son Ryang-ha attempts to catch her eye are quite unique, to say the least. He offers gifts to her in the form of her current targets, tied up and battered, and will do anything to spend more time together. Reluctantly, Chateau goes along with this act, and so begins the cat-and-mouse game of love between two killers.', '9.2', 'Love of Kill', 'https://storage.googleapis.com/mangaudible/temp/koroshi_ai.jpg'),
	('Kuro no Souzou Shoukanshi', 'Ikui Sora', 'Hiroki', '2017', 'Ongoing', 'Due to a gods mistake, high schooler Tsuguna died before his time. In exchange, the god agreed to do him a favor in his next life. Tsuguna is reborn to a noble household in a world with magic. He has an unusual form of magic that he requested from the god, the ability to create summoned creatures. However, his dark Japanese hair and eyes mark him as a cursed child in this new world, and his powers are slow to appear. He is kept in a dark basement where he reads his familys books, until one day he finally uncovers the key to his powers. Finally, he can set off into the world with his summoned companion to level up his skills!', '9', 'The Black Create Summoner: Revolt of Reincarnated', 'https://storage.googleapis.com/mangaudible/temp/kuro_no_souzou_shoukanshi.jpg'),
	('Late bloomer', 'Isshin Tamaya', 'Isshin Tamaya', '2020', 'Ongoing', 'To be Updated Soon...', '7', 'Late Bloomer', 'https://storage.googleapis.com/mangaudible/temp/late_bloomer.jpg'),
	('Ore no Ie ga Maryoku Spot datta Ken - Sundeiru dake de Sekai Saikyou', 'Amaui Shiroichi', 'Nabeshima Tetsuhiro', '2018', 'Ongoing', 'Living carefree at home is the greatest shortcut...my house is the world\'\'s greatest Magic Power Spot. That being the case, both my house and I were summoned to another world by some guys who were aiming for it. However, I\'\'ve been living in this place for many years and my body is, apparently, abnormally overflowing with magic. Due to some unforeseen circumstances by those guys who summoned me, they quickly ran away. Be that as it may, there are still some ill-mannered people who covet the magic leaking out of my house. I won\'\'t give up my house to those people! I\'\'m going to wield my power as I please!', '7', 'About my house is a magic power spot', 'https://storage.googleapis.com/mangaudible/temp/ore_no_ie_ga_maryoku_spot_datt.jpg\r\n\r\n'),
	('Overlord', 'Maruyama Kugane', 'Miyama Fugin', '2016', 'Ongoing', 'The final hour of the popular virtual reality game Yggdrasil has come. However, Momonga, a powerful wizard and master of the dark guild Ainz Ooal Gown, decides to spend his last few moments in the game as the servers begin to shut down. To his surprise, despite the clock having struck midnight, Momonga is still fully conscious as his character and, moreover, the non-player characters appear to have developed personalities of their own! Confronted with this abnormal situation, Momonga commands his loyal servants to help him investigate and take control of this new world, with the hopes of figuring out what has caused this development and if there may be others in the same predicament.', '8', 'Overlord', 'https://storage.googleapis.com/mangaudible/temp/overlord.jpg'),
	('Rettou Gan No Tensei Majutsushi Shiitage Rareta Saikyou No Minashigo Ga Isekai De Musou Suru', 'Kankitsu Yusura', 'Yaya Hinata', '2018', 'Ongoing', 'Abel, a boy abandoned by his family because of the fear his unparalleled talent for magic evoked on them, was taken to an orphanage and taught magic by a former great magician.\r\nEventually, his ability far surpassed that of his teacher and after receiving an invitation from the magical society known as Chaos Raid he embarks on a journey with the fire hero, Maria and the water hero Daytona and later, the ash hero, Cain.\r\nThis is the story of Abel\'\'s childhood and adolescence before his reincarnation.', '6.5', 'The Reincarnation Magician of the Inferior Eyes', 'https://storage.googleapis.com/mangaudible/temp/rettou_gan_no_tensei_majutsush.jpg'),
	('Riffle Is Beautiful', 'Akki Sarumi', 'Salmiakki', '2015', 'Completed', 'Rifle-shooting sports are competitive activities testing accuracy and precision using a rifle. In Japan, carrying firearms is prohibited, so most of the participants are members of the defense force. When the use of rifles using a light beam instead of real bullets as ammunition became common, rifle-shooting competitions became accessible to the younger population, giving way to school contests.\r\nFirst-year high school student and marksmanship enthusiast Hikari Kokura has just transferred to Chidori High School. She tries to join the club of her choice, but finds out that the club no longer exists due to the low popularity of the sport. Distraught, she tries to restore the club and somehow manages to recruit three other members: her childhood friend Izumi Shibusawa, the half-Russian Erika Meinohama, and the stoic Yukio Igarashi.\r\nThis marks the beginning of the Chidori Rifle-Shooting Club, who have only one goal—to compete on the national stage!', '7', 'Rifle Is Beautiful', 'https://storage.googleapis.com/mangaudible/temp/rifle_is_beautiful.png'),
	('Salaryman ga Isekai ni Ittara Shitennou ni Natta Hanashi', 'Benigashira', 'Muramitsu', '2019', 'Ongoing ', 'A normal, ordinary, basic, generic, run of the mill salary man, gets summoned by the Demon King after an accident. What could possibly go wrong? Right?\r\n', '6', 'Story About a Salaryman Who Became one of the Four Heavenly Kings When he Went to Another World\'', 'https://storage.googleapis.com/mangaudible/temp/salaryman_ga_isekai_ni_ittara_.jpg'),
	('Tate no Yuusha no Nariagari', 'Yusagi Aneko', 'Aiya Kyu', '2014', 'Ongoing', 'Naofumi Iwatani, Naofumi Iwatani, an uncharismatic Otaku who spends his days on games and manga, suddenly finds himself summoned to a parallel universe! He discovers he is one of four heroes equipped with legendary weapons and tasked with saving the world from its prophesied destruction. As the Shield Hero, the weakest of the heroes, all is not as it seems. Naofumi is soon alone, penniless, and betrayed. With no one to turn to, and nowhere to run, he is left with only his shield. Now, Naofumi must rise to become the legendary Shield Hero and save the world!\r\n', '9', 'The Rising of the Shield Hero', 'https://storage.googleapis.com/mangaudible/temp/tate_no_yuusha_no_nariagari.jpg'),
	('Tensei Takenaka hanbei maina bushou ni tensei shita nakama-tachi to sengokuranse wo ikinuku', 'Aoyama Yuu', 'Kazumiya Akira', '2018', 'Ongoing', 'The two genius military advisors who led Toyotomi Hideyoshi to unify the nation, Kuroda Kanbei Yoshitaka and Takenaka Hambei Shigeharu. A dull and unmarried salaryman in his thirties wake up one day to find that he had become Takanaka HanbeL He had been reborn along with seven other men of the same age and circumstance! That night, he suddenly found himself in an empty room with a PC with a chatroom called Tea room open. Apparently, he could use this to chat with his fellow reincarnators?? Will they be able to survive in this era of battle and strife?', '8.6', 'Surviving The Sengoku Period With My Friends As Minor Warlords', 'https://storage.googleapis.com/mangaudible/temp/tensei_takenaka_hanbei.jpg'),
	('Tensei shitara Slime datta Ken Ibun Makuni Kurashi no Trinity', 'Tono', 'Tae', '2019', 'Ongoing', 'Against the odds, the little slime Rimiru has established his magical kingdom for all monsters, called Tempest, and it\'\'s thriving. But three visitors, Phos the fox girl, Stella the dragon girl, and Frey the winged girl, come to pay Tempest a visit, they\'\'re stunned at just how quickly it\'\'s developed.', '9', 'That Time I Got Reincarnated as a Slime Another Story: Trinity of the Magic Kingdom', 'https://storage.googleapis.com/mangaudible/temp/tensei_shitara_slime_datta_ken.jpg'),
	('World Customize Creator', 'Hero Tennki', 'Hijikata Yuu', '2018', 'Ongoing', 'Tagami Yusuke, led by a mysterious voice, is summoned to another world, Caltsio. He was just a young video-game lover, but Fate decided to make him become the Evil God of Calamity of this world, obtaining the ability to create and customize everything, Customize Creation.', '7', 'World Customize Creator', 'https://storage.googleapis.com/mangaudible/temp/world_customize_creator.jpg'),
	('Yuukyuu no Gusha Asley no, Kenja no Susume', 'Kenja no Susume', 'Hifumi', '2015', 'Ongoing', 'When he was young, he had failed at the Magic Academy and was looked down by others.However by chance, he discovered a mythological medicine, so he obtained an immortal body.In order to get revenge on the people who made fun of him, he began researching magic and magical artifacts different from the academy. After 5000 years of research, he has become an ancient magic user before he noticed.\r\nThe people he was seeking revenge were long gone, losing his purpose, Asley went on a journey to see the world after 5000 years with his familiar Pochi.With an unexpected turn of events after helping many humans, he is now living at the magic academy.A 5000 year old man with a young appearance Asley, how will he live his second life\'\'s youth?', '8', 'The Principle of a Philosopher by Eternal Fool asley', 'https://storage.googleapis.com/mangaudible/temp/yuukyuu_no_gusha_asley_no_kenj.jpg'),
	('Yuusha no Mago to Maou no Musume', 'Fudou Ran', 'Fudou Ran', '2017', 'Ongoing', 'After the great battle between the Demon King and the Hero, justice prevailed and the devils scattered. The Demon King was killed. A few years later, the Demon King\'\'s daughter went on a journey to find her father\'\'s heritage, and met the granddaughter of the Hero. Could this journey signal a new start for the two?', '8', 'Hero\'\'s Granddaughter and Demon Lord\'\'s Daughter, Sakurako & Darkneria', 'https://storage.googleapis.com/mangaudible/temp/yuusha_no_mago_to_maou_no_musu.jpg')
]

mycursor.executemany(manga_sql, manga_values_sql)
mydb.commit()
print(mycursor.rowcount, "was inserted into 'manga'.")

manga_genre_sql = "INSERT INTO manga_genre (manga_id, genre_id) VALUES (%s, %s)"
manga_genre_values = [ 
	(1, 1),
	(1, 2),
	(1, 9),
	(2, 3),
	(2, 4),
	(3, 3),
	(3, 5),
	(3, 10),
	(4, 1),
	(4, 2),
	(4, 3),
	(4, 6),
	(4, 11),
	(5, 1),
	(5, 3),
	(5, 4),
	(6, 1),
	(6, 5),
	(7, 1),
	(7, 6),
	(8, 1),
	(8, 3),
	(8, 5),
	(9, 1),
	(9, 3),
	(9, 4),
	(10, 1),
	(10, 3),
	(10, 6),
	(10, 11),
	(11, 2),
	(11, 5),
	(11, 11),
	(12, 1),
	(12, 6),
	(12, 11),
	(13, 3),
	(13, 4),
	(13, 10),
	(14, 2),
	(14, 3),
	(14, 6),
	(14, 9),
	(14, 11),
	(15, 2),
	(15, 5),
	(15, 9),
	(16, 2),
	(16, 3),
	(16, 5),
	(16, 10),
	(17, 2),
	(17, 3),
	(17, 11),
	(18, 1),
	(18, 2),
	(18, 3),
	(18, 5),
	(18, 6),
	(19, 1),
	(19, 2),
	(19, 3),
	(19, 6),
	(19, 11),
	(20, 1),
	(20, 2),
	(20, 5),
	(20, 11)
]

mycursor.executemany(manga_genre_sql, manga_genre_values)
mydb.commit()
print(mycursor.rowcount, "was inserted into 'manga_genre'.")
#=================END INSERT INTO DATABASE=================



def getData(query):
    mycursor.execute(query)
    fetchdata = mycursor.fetchall()
    return fetchdata
