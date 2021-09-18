INSERT INTO packtypes(packTypeId, description, lovelaceCost)
SELECT 1, 'Test1', 90000000
UNION ALL SELECT 2, 'Test2', 25000000
UNION ALL SELECT 3, 'Test3', 333000000;

INSERT INTO nfts (policyId, assetName, metadataJson)
SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NFT1', '{}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NFT2', '{}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NFT3', '{}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NFT4', '{}';

INSERT INTO packs (packTypeId)
SELECT 1 
UNION ALL SELECT 2;

INSERT INTO packContents(packId, nftId)
SELECT 1, 1
UNION ALL SELECT 2, 2
UNION ALL SELECT 2, 3
UNION ALL SELECT 2, 4;
