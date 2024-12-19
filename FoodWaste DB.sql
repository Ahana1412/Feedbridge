-- CREATE DATABASE FoodWaste;
USE FoodWaste;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    role ENUM('donor', 'food_bank', 'volunteer', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE donor (
    DonorID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    DonorType ENUM('Individual', 'Restaurant', 'GroceryStore', 'Others') NOT NULL,
    ContactNo VARCHAR(15) NOT NULL,
    Address TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES users(id)
);

CREATE TABLE food (
    FoodID INT AUTO_INCREMENT PRIMARY KEY,
    DonorID INT NOT NULL,
    Name VARCHAR(100) NOT NULL, 
    Description VARCHAR(255),
    Quantity INT,
    DonationDate DATE NOT NULL,
    ExpiryDate DATE NOT NULL,
    RemainingShelfLife INT GENERATED ALWAYS AS (DATEDIFF(ExpiryDate, DonationDate)) STORED, -- Automatically calculated
    FoodType ENUM('Veg', 'Non-Veg') NOT NULL,
    ItemType ENUM('Ready-to-Eat', 'Grocery') NOT NULL,
    Perishability ENUM('Perishable', 'Non-Perishable') NOT NULL,
    FOREIGN KEY (DonorID) REFERENCES Donor(DonorID)
);

CREATE TABLE volunteer (
    VolunteerID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    ContactNo VARCHAR(15) NOT NULL,
    PreferredLocation VARCHAR(100),
    Availability ENUM('Weekdays', 'Weekends', 'Full-Time', 'Part-Time'),
    Address TEXT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES users(id)
);

CREATE TABLE foodbank (
    FoodBankID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Address TEXT NOT NULL,
    ContactNo VARCHAR(15) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES users(id)
);

CREATE TABLE orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    FoodID INT NOT NULL,
    FoodBankID INT NOT NULL,
    RequestDate DATE NOT NULL,
    Status ENUM('Pending', 'VolunteerAssigned', 'Completed') NOT NULL, 
    FOREIGN KEY (FoodID) REFERENCES food(FoodID),
    FOREIGN KEY (FoodBankID) REFERENCES foodbank(FoodBankID)
);

-- INSERT INTO users (username, password_hash, email, role) 
-- VALUES ('donor1', '02345d9e8754a6176fd1f1a74198e05b4ccef4a004ce69d811b9c87d60101b1096bea24b2ffc5422022ae497b3afa25f70d817413ee43614b2817b1ad7c6ded319293f36db3677cfdd9b10ed2a8468b7a1f8e200e11cb7af8b260b691ab0aeed', 'donor@example.com', 'donor');
-- INSERT INTO users (username, password_hash, email, role) 
-- VALUES ('foodbank1', '8d4f40d164d49279b8e91bc41a76c1fcb96ee29370f7cd5ad4699d92a13a4af9265fdfaf8a96cf4bcaa485056e2dff41fc1ea96a6d747dd6013a7d27b3a6e32cf432c3309253d53b1351286823e3aa00a1d3ed78985605395b16e5ca0ffc0a93', 'foodbank@example.com', 'food_bank');
-- INSERT INTO users (username, password_hash, email, role) 
-- VALUES ('volunteer1', '8576144b1f496856cfaafa66486a7ed2783b99509ecb756df4c73bb3275e428d0a8ae5b62ff58057e8fb86e36affbdd32cb04ede38775b91d85bff6e9a5842437dac3db1855da8e19b3507af181be09236eb914627aac25e07988d7777111a88', 'volunteer@example.com', 'volunteer');
-- INSERT INTO users (username, password_hash, email, role) 
-- VALUES ('admin1', '2198b1c97ec929694c248b104e627af834845a7bd696d990a2a3d7fbf79b400722cedb5cd8b49042cff4ab0562af0a727f4e0f9f0068c62253f3c25b387d5cf5070403dd9522647030840b12d91c5795b88c8fdbe8534b54ea02fcecb8f99283', 'admin@example.com', 'admin');

ALTER TABLE donor 
MODIFY COLUMN DonorType ENUM('Individual', 'Restaurant', 'GroceryStore', 'Others') NOT NULL;
