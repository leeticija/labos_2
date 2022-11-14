PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE orders(
    order_id INTEGER NOT NULL PRIMARY KEY,
    order_name TEXT,
    order_common_name TEXT,
    wings TEXT,
    total_order_species INTEGER,
    total_order_families INTEGER,
    metamorphosis TEXT
  );
INSERT INTO orders VALUES(1,'Microcoryphia','Bristletails','None',450,2,'None');
INSERT INTO orders VALUES(2,'Zygentoma','Silverfish, Firebrats','None',370,5,'None');
INSERT INTO orders VALUES(3,'Ephemeroptera','Mayflies','Two pair',2000,19,'Incomplete');
INSERT INTO orders VALUES(4,'Odonata','Damselflies, Dragonflies','Two pair',5000,29,'Incomplete');
INSERT INTO orders VALUES(5,'Plecoptera','Stoneflies','Two pair',2000,10,'Incomplete');
INSERT INTO orders VALUES(6,'Phasmida','Walkingsticks','Wings either greatly reduced or lacking',3000,2,'Gradual');
INSERT INTO orders VALUES(7,'Orthoptera','Crickets, Grasshoppers, and Katydids','Two pair or wingless',24000,29,'Gradual');
INSERT INTO orders VALUES(8,'Dermaptera','Earwigs','Two pair or wingless',2000,8,'Gradual');
INSERT INTO orders VALUES(9,'Mantodea','Mantids','Two pair or wingless',1800,8,'Gradual');
INSERT INTO orders VALUES(10,'Blattodea','Cockroaches and termites','Two pair or wingless',4000,5,'Gradual');
CREATE TABLE insects(
    insect_id INTEGER NOT NULL PRIMARY KEY,
    genus TEXT,
    specie TEXT,
    binomial_name TEXT,
    order_id INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id)
  );
INSERT INTO insects VALUES(1,'Mantis','religiosa','Mantis religiosa',9);
INSERT INTO insects VALUES(2,'Anax','imperator','Anax imperator',4);
INSERT INTO insects VALUES(3,'Allacrotelsa','spinulata','Allacrotelsa spinulata',2);
INSERT INTO insects VALUES(4,'Petrobius','brevistylus','Petrobius brevistylus',1);
INSERT INTO insects VALUES(5,'Caenis','hilaris','Caenis hilaris',3);
INSERT INTO insects VALUES(6,'Alloperla','petasata','Alloperla petasata',5);
INSERT INTO insects VALUES(7,'Timema','californicum','Timema californicum',6);
INSERT INTO insects VALUES(8,'Arethaea','phantasma','Arethaea phantasma',7);
INSERT INTO insects VALUES(9,'Forficula','auricularia','Forficula auricularia',8);
INSERT INTO insects VALUES(10,'Parcoblatta','americana','Parcoblatta americana',10);
INSERT INTO insects VALUES(11,'Tenodera','sinensis','Tenodera sinensis',9);
INSERT INTO insects VALUES(12,'Argia','emma','Argia emma',4);
INSERT INTO insects VALUES(13,'Pseudosermyle','catalinae','Pseudosermyle catalinae',6);
INSERT INTO insects VALUES(14,'Utaperla','gaspesiana','Utaperla gaspesiana',5);
INSERT INTO insects VALUES(15,'Eurycotis','floridiana','Eurycotis floridiana',10);
INSERT INTO insects VALUES(16,'Pachydiplax','longipennis','Pachydiplax longipennis',4);
INSERT INTO insects VALUES(17,'Brachymesia','furcata','Brachymesia furcata',4);
INSERT INTO insects VALUES(18,'Brachymesia','gravida ','Brachymesia gravida ',4);
INSERT INTO insects VALUES(19,'Gryllotalpa','gryllotalpa','Gryllotalpa gryllotalpa',7);
INSERT INTO insects VALUES(20,'Gryllotalpa','major','Gryllotalpa major',7);
INSERT INTO insects VALUES(21,'Neocurtilla ','hexadactyla','Neocurtilla  hexadactyla',7);
INSERT INTO insects VALUES(22,'Machiloides ','banksi','Machiloides  banksi',2);
INSERT INTO insects VALUES(23,'Callibaetis ','ferrugineus ','Callibaetis ferrugineus',3);
INSERT INTO insects VALUES(24,'Callibaetis ','pallidus','Callibaetis  pallidus',3);
INSERT INTO insects VALUES(25,'Callibaetis ','skokianus','Callibaetis  skokianus',3);
COMMIT;
