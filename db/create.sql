/****** #Voce******/


CREATE TABLE [dbo].[Voce] (
[ID][int] NOT NULL IDENTITY(1,1),
[Ime][varchar](50),
[slika][varchar](max),
[BeaconUUID][varchar](100),
[BeaconMajor][int],
[BeaconMinor][int],
[OsnovnaCijena][decimal](5,2),
[TrenutnaKlasa][int],
PRIMARY KEY (ID)
)

INSERT INTO Voce (Ime, slika, BeaconUUID,BeaconMajor,BeaconMinor, OsnovnaCijena,TrenutnaKlasa)
VALUES 
('Banana', cast(1 AS varchar(MAX)), 'fda50693-a4e2-4fb1-afcf-c6eb07647825', 5, 6,   9.99,3),
('Limun', cast(2 AS varchar(MAX)), 'fda50693-a4e2-4fb1-afcf-c6eb07647825', 2, 2, 12.99,2);

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

ALTER TABLE dbo.Popusti
  ADD CONSTRAINT uq_Popusti UNIQUE(ID_voce, Klasa);
  
INSERT INTO Popusti (ID_voce, Ime_Klase, Klasa, Popust)
VALUES 
(1, 'Zuto-zelena Banana', 1, 0.00),
(1, 'Zuta Banana', 2, 0.00),
(1, 'Zuta Banana - Malo Fleka', 3, 0.30),
(1, 'Zuta Banana - Dosta Fleka', 4, 0.60),
(1, 'Pocrnila Banana', 5, 0.90),
(2, 'Novi Limun', 1, 0.00),
(2, 'Stari Limun', 2, 0.60);

/****** #Opazaji******/


CREATE TABLE [dbo].[Opazaji] (
[ID][int] NOT NULL IDENTITY(1,1),
[ID_voca] [int] NOT NULL,
[slikaPI][varchar](max),
[KlasaModel] [int],
[Vrijeme] [datetime],
PRIMARY KEY (ID),
FOREIGN KEY (ID_voca) REFERENCES [dbo].[Voce](ID)
)

/****** #Users******/


CREATE TABLE [dbo].[Users] (
[ID][int] NOT NULL IDENTITY(1,1),
[Password][varchar](max),
[Name][varchar](100)
PRIMARY KEY (ID)
)

INSERT INTO [dbo].Users (Password, Name)
VALUES 
('sha256$F6JLqcUm$88064d1b678973c24694592f7f02013bcd0dead8cbbc75a2882e44e04b0b32d1', 'admin');
