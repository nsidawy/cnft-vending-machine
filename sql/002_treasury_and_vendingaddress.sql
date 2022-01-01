CREATE TABLE treasuries (
    address VARCHAR(128) NOT NULL
    , sharePercent FLOAT NOT NULL
    , PRIMARY KEY (address)
);

CREATE TABLE vendingAddresses (
    vendingAddressId INT NOT NULL
    , address VARCHAR(128) NOT NULL
    , signingKeyPath VARCHAR(4096) NOT NULL
    , PRIMARY KEY (vendingAddressId)
);

ALTER TABLE packTypes
ADD COLUMN vendingAddressId INT NULL;

ALTER TABLE packTypes
ADD CONSTRAINT FK_packTypes_vendingAddresses 
    FOREIGN KEY (vendingAddressId) REFERENCES vendingAddresses (vendingAddressId);

ALTER TABLE payments
ADD COLUMN vendingAddressId INT NULL;

ALTER TABLE payments
ADD CONSTRAINT FK_payments_vendingAddresses 
    FOREIGN KEY (vendingAddressId) REFERENCES vendingAddresses (vendingAddressId);
