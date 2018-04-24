-- Insert requests
-- Mon Apr 23

-- Insert adress
INSERT INTO adresse (destinataire, voie, code_postal, ville, renseignement_supplementaire, telephone, numero_voie)
VALUES (FAKE DATA);

-- Insert role
INSERT INTO role (nom)
VALUES (NOM);

-- Insert employee

INSERT INTO utilisateur (nom, prenom, mail, password, date_creation, date_suppression)
VALUES (VALEURS);

INSERT INTO employe (id_utilisateur)
SELECT utilisateur.id
FROM utilisateur
ORDER BY utilisateur.id
LIMIT 1;

UPDATE employe
SET id_role =
  (SELECT role.id FROM role WHERE nom = VALEUR)
WHERE id_utilisateur =
  (SELECT id_utilisateur FROM employe ORDER BY id_utilisateur DESC LIMIT 1);

-- Insert customer

INSERT INTO utilisateur (nom, prenom, mail, password, date_creation, date_suppression)
VALUES (VALEURS);

INSERT INTO client (id_utilisateur)
SELECT utilisateur.id
FROM utilisateur
ORDER BY utilisateur.id
LIMIT 1;

UPDATE client
SET id_adresse_livraison =
  (SELECT )
