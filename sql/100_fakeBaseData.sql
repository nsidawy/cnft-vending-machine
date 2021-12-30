INSERT INTO packtypes(packTypeId, description, lovelaceCost)
SELECT 1, 'Test1', 3000000
UNION ALL SELECT 2, 'Test2', 25000000
UNION ALL SELECT 3, 'Test3', 333000000;

INSERT INTO nfts (policyId, assetName, metadataJson)
SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NFT6', '{"name": "NFT5", "description": "Test", "image": "ipfs://QmPtr2FfkEDc2xg4VN6kWm5dLxxGXkJF3XWykd4NZrR4qS", "mediaType": "image/png"}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NFT10', '{"name": "NFT7", "description": "Test", "image": "ipfs://QmPtr2FfkEDc2xg4VN6kWm5dLxxGXkJF3XWykd4NZrR4qS", "mediaType": "image/png"}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NF11', '{"name": "NFT8", "description": "Test", "image": "ipfs://QmPtr2FfkEDc2xg4VN6kWm5dLxxGXkJF3XWykd4NZrR4qS", "mediaType": "image/png"}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'NFT2', '{"name": "NFT9", "description": "Test", "image": "ipfs://QmPtr2FfkEDc2xg4VN6kWm5dLxxGXkJF3XWykd4NZrR4qS", "mediaType": "image/png"}';

INSERT INTO packs (packTypeId)
SELECT 1 
UNION ALL SELECT 2;

INSERT INTO packContents(packId, nftId)
SELECT 1, 1
UNION ALL SELECT 2, 2
UNION ALL SELECT 2, 3
UNION ALL SELECT 2, 4;

INSERT INTO treasuries (address,sharePercent)
VALUES ('addr_test1qqwltpc0790swxldlqdp7rg7z9r0rat3kl32vhk6sgmgm6f3p5mx9t4n86t2gev4uvkdsldaa3tma8rcea7ve3re3zkqru95gy', 0.6)
    , ('addr_test1qre4g9zdak8ya7cestlazgvmrxt0kyq0u8jwnwjhxl4gcr33p5mx9t4n86t2gev4uvkdsldaa3tma8rcea7ve3re3zkqjwyf7u', 0.4);
