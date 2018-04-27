-- MySQL script
-- Some SQL request to test the database

-- ---------------------------------------------
-- Requests on users
-- ---------------------------------------------

-- Select all customers and the name of their city

SELECT utilisateur.mail, utilisateur.date_creation, adresse.ville
FROM client
INNER JOIN utilisateur
    ON client.id_utilisateur = utilisateur.id
INNER JOIN adresse
    ON client.id_adresse_livraison = adresse.id;

-- Select all employees with their role

SELECT utilisateur.prenom, utilisateur.nom, role.nom
FROM employe
INNER JOIN utilisateur
    ON employe.id_utilisateur = utilisateur.id
INNER JOIN role
    ON employe.id_role = role.id;

-- Select all the employees with their role from a restaurant

SELECT utilisateur.prenom, utilisateur.nom, role.nom
FROM employe
INNER JOIN utilisateur
    ON employe.id_utilisateur = utilisateur.id
INNER JOIN role
    ON employe.id_role = role.id
INNER JOIN staff
    ON employe.id_utilisateur = staff.id_utilisateur
WHERE staff.id_restaurant IN (
    SELECT restaurant.id FROM restaurant
    WHERE restaurant.nom LIKE "%Paris13"
);

-- ---------------------------------------------
-- Requests on orders
-- ---------------------------------------------

-- Select all the orders from a restaurant where the orders status is 'en preparation'
SELECT commande.id, restaurant.nom
FROM commande
INNER JOIN restaurant
    ON commande.id_restaurant = restaurant.id
INNER JOIN evolution_preparation
    ON commande.id = evolution_preparation.id_commande
WHERE id_statut_commande IN (
    SELECT id FROM statut_commande
    WHERE statut_commande = "en attente"
)
ORDER BY restaurant.nom;

-- Select all the orders from a restaurant where it tooks more than 1 hour go trough the status 'en preparation'

-- Calculate the average time it takes for a restaurant to start an order (from 'en attente' to "en prepartion")

-- --------------------------------------------
-- Ingredients management for a restaurant
-- --------------------------------------------

-- Select all the ingredients from a restaurant
SELECT ingredient.nom, stock_ingredient_par_restaurant.quantite_allouee
FROM stock_ingredient_par_restaurant
INNER JOIN ingredient
    ON stock_ingredient_par_restaurant.id_ingredient = ingredient.id
INNER JOIN restaurant
    ON stock_ingredient_par_restaurant.id_restaurant = restaurant.id
WHERE restaurant.nom LIKE "%PARIS9";

-- Select the restaurants where the quantity allocated for an ingredient is < to 10% from the global quantity

-- Requests to pass an ingredient to zero with impact on pizza availablity

-- Select all the pizza from a restaurant which are not available