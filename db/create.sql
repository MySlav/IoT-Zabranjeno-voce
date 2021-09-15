/****** #Voce******/


CREATE TABLE [dbo].[Voce] (
[ID][int] NOT NULL IDENTITY(1,1),
[Ime][varchar](50),
[slika][varbinary](max),
[BeaconUUID][varchar](100),
[BeaconMajor][int],
[BeaconMinor][int],
[OsnovnaCijena][decimal](5,2),
[TrenutnaKlasa][int],
PRIMARY KEY (ID)
)

INSERT INTO Voce (Ime, slika, BeaconUUID,BeaconMajor,BeaconMinor, OsnovnaCijena,TrenutnaKlasa)
VALUES 
('Banana', cast(1 AS VARBINARY(MAX)), 'fda50693-a4e2-4fb1-afcf-c6eb07647825', 5, 6,   9.99,3),
('Limun', cast(2 AS VARBINARY(MAX)), 'fda50693-a4e2-4fb1-afcf-c6eb07647825', 2, 2, 12.99,2);

/****** #Popusti******/


CREATE TABLE [dbo].[Popusti] (
[ID][int] NOT NULL IDENTITY(1,1),
[ID_voce] [int] NOT NULL,
[Ime_Klase][varchar](50),
[Klasa] [int],
[Popust] [decimal](3,2),
PRIMARY KEY (ID),
FOREIGN KEY (ID_voce) REFERENCES [dbo].[Voce](ID)
)

INSERT INTO Popusti (ID_voce, Ime_Klase, Klasa, Popust)
VALUES 
(1, 'Zuto-zelena banana', 1, 0.00),
(1, 'Zuta banana s malo fleka', 2, 0.00),
(1, 'Zuta banana s dosta fleka', 3, 0.30),
(1, 'Pocrnila banana', 4, 0.60),
(1, 'Crna banana', 5, 0.90),
(2, 'Novi limun', 1, 0.00),
(2, 'Stari limun', 2, 0.60);

/****** #Opazaji******/


CREATE TABLE [dbo].[Opazaji] (
[ID][int] NOT NULL IDENTITY(1,1),
[ID_voca] [int] NOT NULL,
[slikaPI][varbinary](max),
[KlasaModel] [int],
[Vrijeme] [datetime],
PRIMARY KEY (ID),
FOREIGN KEY (ID_voca) REFERENCES [dbo].[Voce](ID)
)

ALTER TABLE dbo.Popusti
  ADD CONSTRAINT uq_Popusti UNIQUE(ID_voce, Klasa);