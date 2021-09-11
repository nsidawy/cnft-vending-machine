--NFTs that will be minted on sale
CREATE TABLE nfts (
    nftId INT GENERATED ALWAYS AS IDENTITY
    , assetName VARCHAR(16) NOT NULL
    , metaDataJson VARCHAR(16000) NOT NULL
    , PRIMARY KEY (nftId)
);

--Types of packs that can be bought from the bending machine
CREATE TABLE packTypes (
    packTypeId INT NOT NULL
    , description VARCHAR(32) NOT NULL
    , lovelaceCost BIGINT NOT NULL
    , PRIMARY KEY (packTypeId)
);

--Record of all incoming UTXOs
CREATE TABLE payments (
    paymentId INT GENERATED ALWAYS AS IDENTITY
    , txId VARCHAR(64) NOT NULL
    , indexId INT NOT NULL
    , utxo VARCHAR(128) GENERATED ALWAYS AS (txId || '#' ||CAST(indexId AS VARCHAR(64))) STORED
    , lovelace INT NOT NULL
    , otherAssets VARCHAR(4096) NOT NULL
    , paymentAddress VARCHAR(128) NOT NULL
    , PRIMARY KEY (paymentId)
    , CONSTRAINT UQ_payments UNIQUE (txId, indexId)
);

--Packs and information about whether they were sold or not
CREATE TABLE packs (
    packId INT GENERATED ALWAYS AS IDENTITY
    , packTypeId INT NOT NULL
    , paymentId INT
    , mintingTxId VARCHAR(64) NULL
    , PRIMARY KEY (packId)
    , CONSTRAINT FK_packs_packTypes FOREIGN KEY (packTypeId) 
        REFERENCES packTypes(packTypeId)
    , CONSTRAINT FK_packs_payments FOREIGN KEY (paymentId) 
        REFERENCES payments(paymentId)
    , CONSTRAINT CK_packs_tx CHECK (mintingTxId IS NULL OR (paymentId IS NOT NULL AND mintingTxId IS NOT NULL))
);

--Describes what NFTs are contained in which packs. All NFTs should be pre-assigned to packs
CREATE TABLE packContents (
    packId INT NOT NULL
    , nftId INT NOT NULL
    , PRIMARY KEY (packId, nftId)
    , CONSTRAINT FK_nftContents_packs FOREIGN KEY (packId)
        REFERENCES packs(packId)
    , CONSTRAINT FK_packContents_nfts FOREIGN KEY  (nftId)
        REFERENCES nfts(nftId)
);

--Log of payments that can't be returned since they contain insufficient funds
--to cover min utxo & fee
CREATE TABLE insufficientFundsForReturn (
    paymentId INT NOT NULL
    , PRIMARY KEY (paymentId)
    , CONSTRAINT FK_insufficentFuns_payments FOREIGN KEY (paymentId) 
        REFERENCES payments(paymentId)
);

--Log of errors that occur trying to process a payment
CREATE TABLE errorLog (
    paymentId INT NOT NULL
    , errorMessage VARCHAR(4800) NOT NULL
    , CONSTRAINT FK_errorLog_payments FOREIGN KEY (paymentId) 
        REFERENCES payments(paymentId)
);
