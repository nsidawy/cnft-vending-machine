ALTER TABLE nfts
ADD CONSTRAINT UQ_nfts UNIQUE (policyId, nftId);
