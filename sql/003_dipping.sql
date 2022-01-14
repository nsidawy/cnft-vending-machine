ALTER TABLE nfts
ADD CONSTRAINT UQ_nfts UNIQUE (policyId, nftId);

CREATE TABLE dips (
    paymentId INT NOT NULL
    , burnedNuggetNftId INT NOT NULL
    , burnedSauceNftId INT NOT NULL
    , dippedNuggetNftId INT NOT NULL
    , CONSTRAINT FK_dips_payments FOREIGN KEY (paymentId)
        REFERENCES payments (paymentId)
    , CONSTRAINT FK_dips_burnedNugget FOREIGN KEY (burnedNuggetNftId)
        REFERENCES nfts (nftId)
    , CONSTRAINT FK_dips_burnedSauce FOREIGN KEY (burnedSauceNftId)
        REFERENCES nfts (nftId)
    , CONSTRAINT FK_dips_dippedNugget FOREIGN KEY (dippedNuggetNftId)
        REFERENCES nfts (nftId)
);
