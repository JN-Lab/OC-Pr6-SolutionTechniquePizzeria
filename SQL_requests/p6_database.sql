-- MySQL Script generated by MySQL Workbench
-- Fri Apr 20 16:14:20 2018
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema p6_project
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema p6_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `p6_project` DEFAULT CHARACTER SET utf8 ;
USE `p6_project` ;

-- -----------------------------------------------------
-- Table `p6_project`.`utilisateur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`utilisateur` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`utilisateur` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(45) NOT NULL,
  `prenom` VARCHAR(45) NOT NULL,
  `mail` VARCHAR(100) NOT NULL,
  `password` CHAR(40) CHARACTER SET 'utf8' NOT NULL COMMENT 'A passer en CHAR(40) si SHA1 ou CHAR(32) si md5',
  `date-creation` DATE NOT NULL,
  `date-suppression` DATE NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
ROW_FORMAT = Default;


-- -----------------------------------------------------
-- Table `p6_project`.`adresse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`adresse` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`adresse` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `destinataire` VARCHAR(100) NOT NULL,
  `voie` VARCHAR(5) NOT NULL,
  `code_postal` INT NOT NULL,
  `ville` VARCHAR(45) NOT NULL,
  `renseignement_supplementaire` VARCHAR(200) NULL,
  `telephone` VARCHAR(15) NULL,
  `numero_voie` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`client`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`client` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`client` (
  `id_utilisateur` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_adresse_livraison` INT UNSIGNED NOT NULL,
  `id_adresse_facturation` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_utilisateur`),
  INDEX `fk_client_id_adresse_livraison_adresse_id` (`id_adresse_livraison` ASC),
  INDEX `fk_client_id_adresse_facturation_adresse_id` (`id_adresse_facturation` ASC),
  CONSTRAINT `fk_client_id_adresse_livraison_adresse_id`
    FOREIGN KEY (`id_adresse_livraison`)
    REFERENCES `p6_project`.`adresse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_id_adresse_facturation_adresse_id`
    FOREIGN KEY (`id_adresse_facturation`)
    REFERENCES `p6_project`.`adresse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_client_id_utilisateur_utilisateur_id`
    FOREIGN KEY (`id_utilisateur`)
    REFERENCES `p6_project`.`utilisateur` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`role`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`role` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`role` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`employe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`employe` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`employe` (
  `id_utilisateur` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_role` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_utilisateur`),
  INDEX `fk_employe_id_role_role_id` (`id_role` ASC),
  CONSTRAINT `fk_employe_id_utilisateur_utilisateur_id`
    FOREIGN KEY (`id_utilisateur`)
    REFERENCES `p6_project`.`utilisateur` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_employe_id_role_role_id`
    FOREIGN KEY (`id_role`)
    REFERENCES `p6_project`.`role` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`type_livraison`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`type_livraison` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`type_livraison` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type_livraison` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`statut_paiement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`statut_paiement` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`statut_paiement` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `statut_paiement` VARCHAR(15) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`mode_reglement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`mode_reglement` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`mode_reglement` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `mode_reglement` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`commande`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`commande` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`commande` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `prix_ttc` DECIMAL(6,2) NOT NULL,
  `tva` DECIMAL(4,2) NOT NULL,
  `date` DATETIME NOT NULL,
  `id_adresse_livraison` INT UNSIGNED NOT NULL,
  `id_adresse_facturation` INT UNSIGNED NOT NULL,
  `id_type_livraison` INT UNSIGNED NOT NULL,
  `id_statut_paiement` INT UNSIGNED NOT NULL,
  `id_mode_reglement` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_commande_id_adresse_livraison_adresse_id` (`id_adresse_livraison` ASC),
  INDEX `fk_commande_id_adresse_facturation_adresse_id` (`id_adresse_facturation` ASC),
  INDEX `fk_commande_id_type_livraison_type_livraison_id` (`id_type_livraison` ASC),
  INDEX `fk_commande_id_statut_paiement_statut_paiement_id` (`id_statut_paiement` ASC),
  INDEX `fk_commande_id_mode_reglement_mode_reglement_id` (`id_mode_reglement` ASC),
  CONSTRAINT `fk_commande_id_adresse_livraison_adresse_id`
    FOREIGN KEY (`id_adresse_livraison`)
    REFERENCES `p6_project`.`adresse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_commande_id_adresse_facturation_adresse_id`
    FOREIGN KEY (`id_adresse_facturation`)
    REFERENCES `p6_project`.`adresse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_commande_id_type_livraison_type_livraison_id`
    FOREIGN KEY (`id_type_livraison`)
    REFERENCES `p6_project`.`type_livraison` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_commande_id_statut_paiement_statut_paiement_id`
    FOREIGN KEY (`id_statut_paiement`)
    REFERENCES `p6_project`.`statut_paiement` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_commande_id_mode_reglement_mode_reglement_id`
    FOREIGN KEY (`id_mode_reglement`)
    REFERENCES `p6_project`.`mode_reglement` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
ROW_FORMAT = Default;


-- -----------------------------------------------------
-- Table `p6_project`.`statut_commande`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`statut_commande` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`statut_commande` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `statut` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`evolution_preparation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`evolution_preparation` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`evolution_preparation` (
  `id_commande` INT UNSIGNED NOT NULL,
  `id_statut_commande` INT UNSIGNED NOT NULL,
  `date_debut_operation` DATETIME NOT NULL,
  `date_fin_operation` DATETIME NOT NULL,
  PRIMARY KEY (`id_commande`, `id_statut_commande`),
  INDEX `fk_evolution_preparation_id_statut_commande_statut_commande_id` (`id_statut_commande` ASC),
  INDEX `fk_evolution_preparation_id_commande_commande_id` (`id_commande` ASC),
  CONSTRAINT `fk_evolution_preparation_id_commande_commande_id`
    FOREIGN KEY (`id_commande`)
    REFERENCES `p6_project`.`commande` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_evolution_preparation_id_statut_commande_statut_commande_id`
    FOREIGN KEY (`id_statut_commande`)
    REFERENCES `p6_project`.`statut_commande` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
PACK_KEYS = Default;


-- -----------------------------------------------------
-- Table `p6_project`.`restaurant`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`restaurant` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`restaurant` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(45) NULL,
  `id_adresse_location` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_restaurant_id_adresse_location_adresse_id` (`id_adresse_location` ASC),
  CONSTRAINT `fk_restaurant_id_adresse_location_adresse_id`
    FOREIGN KEY (`id_adresse_location`)
    REFERENCES `p6_project`.`adresse` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`staff`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`staff` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`staff` (
  `id_restaurant` INT UNSIGNED NOT NULL,
  `id_utilisateur` INT UNSIGNED NOT NULL,
  `date_debut` DATE NOT NULL,
  `date_fin` DATE NOT NULL,
  PRIMARY KEY (`id_restaurant`, `id_utilisateur`),
  INDEX `fk_staff_id_utilisateur_employe_id_utilisateur` (`id_utilisateur` ASC),
  INDEX `fk_staff_id_restaurant_restaurant_id` (`id_restaurant` ASC),
  CONSTRAINT `fk_staff_id_restaurant_restaurant_id`
    FOREIGN KEY (`id_restaurant`)
    REFERENCES `p6_project`.`restaurant` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_staff_id_utilisateur_employe_id_utilisateur`
    FOREIGN KEY (`id_utilisateur`)
    REFERENCES `p6_project`.`employe` (`id_utilisateur`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`ingredient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`ingredient` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`ingredient` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(80) NOT NULL,
  `prix_unitaire` DECIMAL(10,2) NOT NULL,
  `quantite_globale` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`stock_ingredient_par_boutique`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`stock_ingredient_par_boutique` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`stock_ingredient_par_boutique` (
  `ingredient_id` INT UNSIGNED NOT NULL,
  `restaurant_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`ingredient_id`, `restaurant_id`),
  INDEX `fk_stock_ingredient_par_boutique_restaurant_id_restaurant_id` (`restaurant_id` ASC),
  INDEX `fk_stock_ingredient_par_boutique_ingredient_id_ingredient_id` (`ingredient_id` ASC),
  CONSTRAINT `fk_stock_ingredient_par_boutique_ingredient_id_ingredient_id`
    FOREIGN KEY (`ingredient_id`)
    REFERENCES `p6_project`.`ingredient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_stock_ingredient_par_boutique_restaurant_id_restaurant_id`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `p6_project`.`restaurant` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`recette`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`recette` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`recette` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `recette` MEDIUMTEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`pizza`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`pizza` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`pizza` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(45) NOT NULL,
  `description` VARCHAR(250) NULL,
  `prix_unitaire` DECIMAL(6,2) NULL,
  `id_recette` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pizza_id_recette_recette_id` (`id_recette` ASC),
  CONSTRAINT `fk_pizza_id_recette_recette_id`
    FOREIGN KEY (`id_recette`)
    REFERENCES `p6_project`.`recette` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`quantite_ingredient_par_pizza`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`quantite_ingredient_par_pizza` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`quantite_ingredient_par_pizza` (
  `id_ingredient` INT UNSIGNED NOT NULL,
  `id_pizza` INT UNSIGNED NOT NULL,
  `quantite_necessaire` DECIMAL(10,2) NULL,
  PRIMARY KEY (`id_ingredient`, `id_pizza`),
  INDEX `fk_pizza_idx` (`id_pizza` ASC),
  INDEX `fk_quantite_ingredient_par_pizza_id_ingredient_ingredient_id` (`id_ingredient` ASC),
  CONSTRAINT `fk_quantite_ingredient_par_pizza_id_ingredient_ingredient_id`
    FOREIGN KEY (`id_ingredient`)
    REFERENCES `p6_project`.`ingredient` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quantite_ingredient_par_pizza_id_pizza_pizza_id`
    FOREIGN KEY (`id_pizza`)
    REFERENCES `p6_project`.`pizza` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`quantite_pizza_par_commande`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`quantite_pizza_par_commande` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`quantite_pizza_par_commande` (
  `id_pizza` INT UNSIGNED NOT NULL,
  `id_commande` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_pizza`, `id_commande`),
  INDEX `fk_quantite_pizza_par_commande_id_commande_commande_id` (`id_commande` ASC),
  INDEX `fk_quantite_pizza_par_commande_id_pizza_pizza_id` (`id_pizza` ASC),
  CONSTRAINT `fk_quantite_pizza_par_commande_id_pizza_pizza_id`
    FOREIGN KEY (`id_pizza`)
    REFERENCES `p6_project`.`pizza` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quantite_pizza_par_commande_id_commande_commande_id`
    FOREIGN KEY (`id_commande`)
    REFERENCES `p6_project`.`commande` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`disponibilite_pizza_par_boutique`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`disponibilite_pizza_par_boutique` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`disponibilite_pizza_par_boutique` (
  `id_pizza` INT UNSIGNED NOT NULL,
  `id_restaurant` INT UNSIGNED NOT NULL,
  `disponibilite` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id_pizza`, `id_restaurant`),
  INDEX `fk_disponibilite_pizza_par_boutique_id_restaurant_restaurant_id` (`id_restaurant` ASC),
  INDEX `fk_disponibilite_pizza_par_boutique_id_pizza_pizza_id` (`id_pizza` ASC),
  CONSTRAINT `fk_disponibilite_pizza_par_boutique_id_pizza_pizza_id`
    FOREIGN KEY (`id_pizza`)
    REFERENCES `p6_project`.`pizza` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_disponibilite_pizza_par_boutique_id_restaurant_restaurant_id`
    FOREIGN KEY (`id_restaurant`)
    REFERENCES `p6_project`.`restaurant` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`categorie_pizza`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`categorie_pizza` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`categorie_pizza` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom_categorie` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`categorie_par_pizza`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`categorie_par_pizza` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`categorie_par_pizza` (
  `id_pizza` INT UNSIGNED NOT NULL,
  `id_categorie` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_pizza`, `id_categorie`),
  INDEX `fk_categorie_par_pizza_id_categorie_categorie_pizza_id` (`id_categorie` ASC),
  INDEX `fk_categorie_par_pizza_id_pizza_pizza_id` (`id_pizza` ASC),
  CONSTRAINT `fk_categorie_par_pizza_id_pizza_pizza_id`
    FOREIGN KEY (`id_pizza`)
    REFERENCES `p6_project`.`pizza` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_categorie_par_pizza_id_categorie_categorie_pizza_id`
    FOREIGN KEY (`id_categorie`)
    REFERENCES `p6_project`.`categorie_pizza` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`sous_cat_par_cat`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`sous_cat_par_cat` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`sous_cat_par_cat` (
  `id_cat_parent` INT UNSIGNED NOT NULL,
  `id_cat_enfant` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_cat_parent`, `id_cat_enfant`),
  INDEX `fk_sous_cat_par_cat_id_cat_enfant_cat_pizza_id` (`id_cat_enfant` ASC),
  INDEX `fk_sous_cat_par_cat_id_cat_parent_cat_pizza_id` (`id_cat_parent` ASC),
  CONSTRAINT `fk_sous_cat_par_cat_id_cat_parent_cat_pizza_id`
    FOREIGN KEY (`id_cat_parent`)
    REFERENCES `p6_project`.`categorie_pizza` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sous_cat_par_cat_id_cat_enfant_cat_pizza_id`
    FOREIGN KEY (`id_cat_enfant`)
    REFERENCES `p6_project`.`categorie_pizza` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `p6_project`.`instruction_recette`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `p6_project`.`instruction_recette` ;

CREATE TABLE IF NOT EXISTS `p6_project`.`instruction_recette` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `instruction` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;