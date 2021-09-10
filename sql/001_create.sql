CREATE TABLE nfts (
    nftId INT GENERATED ALWAYS AS IDENTITY
    , assetName VARCHAR(16) NOT NULL
    , metaDataJson VARCHAR(16000) NOT NULL
    , PRIMARY KEY (nftId)
);

CREATE TABLE packTypes (
    packTypeId INT NOT NULL
    , description VARCHAR(32) NOT NULL
    , lovelaceCost BIGINT NOT NULL
    , PRIMARY KEY (packTypeId)
);

CREATE TABLE packs (
    packId INT GENERATED ALWAYS AS IDENTITY
    , packTypeId INT NOT NULL
    , paymentTxId VARCHAR(64) NULL
    , mintingTxId VARCHAR(64) NULL
    , PRIMARY KEY (packId)
    , CONSTRAINT FK_packs_packTypes FOREIGN KEY (packTypeId) 
        REFERENCES packTypes(packTypeId)
    , CONSTRAINT CK_packs_tx CHECK (mintingTxId IS NULL OR (paymentTxId IS NOT NULL AND mintingTxId IS NOT NULL))
);

CREATE TABLE packContents (
    packId INT NOT NULL
    , nftId INT NOT NULL
    , PRIMARY KEY (packId, nftId)
    , CONSTRAINT FK_nftContents_packs FOREIGN KEY (packId)
        REFERENCES packs(packId)
    , CONSTRAINT FK_packContents_nfts FOREIGN KEY  (nftId)
        REFERENCES nfts(nftId)
);

CREATE TABLE insufficientFundsForReturn (
    txId VARCHAR(64) NOT NULL
    , indexId INT NOT NULL
    , utxo VARCHAR(128) GENERATED ALWAYS AS (txId || '#' ||CAST(indexId AS VARCHAR(64))) STORED
    , PRIMARY KEY (txId, indexId)
);

CREATE TABLE errorLog (
    txId VARCHAR(64) NOT NULL
    , indexId INT NOT NULL
    , utxo VARCHAR(128) GENERATED ALWAYS AS (txId || '#' ||CAST(indexId AS VARCHAR(64))) STORED
    , errorMessage VARCHAR(4800) NOT NULL
);
