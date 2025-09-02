DROP DATABASE IF EXISTS mealplanner;
CREATE DATABASE mealplanner;
USE mealplanner;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE diseases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease_id INT,
    meal_name VARCHAR(100) NOT NULL,
    description TEXT,
    FOREIGN KEY (disease_id) REFERENCES diseases(id)
);

INSERT INTO diseases (name) VALUES ('Diabetes'), ('Hypertension'), ('Gluten Intolerance');

INSERT INTO meals (disease_id, meal_name, description) VALUES
(1, 'Grilled Chicken Salad', 'Lean protein with vegetables, suitable for diabetes.'),
(2, 'Steamed Fish with Veggies', 'Low-sodium dish for hypertension.'),
(3, 'Quinoa Salad', 'Gluten-free whole grain with veggies.');