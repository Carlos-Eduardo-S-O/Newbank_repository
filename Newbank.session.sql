DROP DATABASE IF EXISTS newbank;
CREATE DATABASE newbank;
USE newbank;

CREATE TABLE users(
    id INT AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    login VARCHAR(120) NOT NULL,
    password VARCHAR(120) NOT NULL,
    account_number INT NOT NULL,
    balance FLOAT NOT NULL,
    publickey VARCHAR(500) NOT NULL,
    datetime DATETIME NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE notification(
    id INT AUTO_INCREMENT,
    notification TEXT NOT NULL,
    user INT NOT NULL,
    datetime DATETIME NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(user) REFERENCES users(id)
);


INSERT INTO users(login, name, password, publickey, account_number, balance, datetime) VALUES ("Carlos", "Carlos Eduardo", "1234", "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzp0IsBU1yWmAdiJ9DWH8\ns8+TqRD2Tk/p7gbJbzVwZMLoPbmuHystyVyWSDNUV3DrwaZdtPj7IeDetmH2N8TC\nJWSL9qKm9vpJEDWY0cyhZQmGj69Uqss3IVqxYNi9wmr2cLtXKdOH6Z81nz02k5JF\nyozWyajSiRBOvjzT4sQAaq3BAwPkQKz2Xa3o9uecukfKy6iwWSipe/JqStEIMk8l\nHG1jtr3u/eCDllW2F9XIGJrACG9BDnNogBkUR1YAkK6gsaYAUzWpdAtvCAr5y6z9\npSwoC/FHwiXQ416ukOawFKIgrkRhcfzz3G9oumnG1wm9jmxw9XKpix+lajfq0OUP\nEwIDAQAB\n-----END PUBLIC KEY-----", 1, 188900.00, NOW());

INSERT INTO notification (notification, datetime, user) VALUES ("Seu saldo foi acrescido em R$20.", NOW(), 1);
INSERT INTO notification (notification, datetime, user) VALUES ("Recebemos o pagamento da sua fatura.", NOW(), 1);

SELECT notification 
FROM notification 
ORDER BY datetime DESC LIMIT 1;

SELECT name, balance FROM users;

CREATE VIEW latest_notification AS
    SELECT id, notification, user
    FROM notification 
    ORDER BY datetime DESC;

CREATE VIEW user_list AS 
    SELECT id, name, balance, publickey
    FROM users;

CREATE VIEW user_login AS
    SELECT id, publickey, login, password 
    FROM users;


