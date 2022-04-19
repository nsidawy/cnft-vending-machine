INSERT INTO vendingAddresses (vendingAddressId, address, signingKeyPath)
VALUES (1, 'addr_test1vqxc7z6s6rj3y5xteemduvhfz8t53csakgu0q9nl3zam9ng9rnnzp', 'cardano/receive.skey')
    , (2, 'addr_test1vpvezmxpgqda4zrcr9q6naj453fm5a2j5rk3r08dh33n4rshazg52', 'cardano/receive2.skey');

INSERT INTO packtypes(packTypeId, description, lovelaceCost, vendingAddressId)
SELECT 1, 'Test1', 10000000, 2
UNION ALL SELECT 2, 'Test2', 25000000, 2
UNION ALL SELECT 3, 'Test3', 333000000, 2;

INSERT INTO nfts (policyId, assetName, metadataJson)
SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'Nugget_1', '{"name": "Nugget #00001", "mediaType": "image/png", "image": "ipfs://QmWqfEUVVbRTJFWAjf83HDqhzJZRdA4oH91Y95wDYRB1As", "attributes": {"Rarity": "Uncommon", "Base Shape": "Heart", "Color": "Spicy", "Batter Vector": "[1, 1, 1, 1, 1, 1]", "Background": "GradientD", "Crispiness": "15.1709%", "Hat": "Devil Horns", "Sauce 1": "None", "Sauce 2": "None", "Id": "1", "Batch": "1"}, "description": ["Generative nuggets and delicious sauces", "living on the Cardano Blockchain.", "Dipping is encouraged."]}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'Nugget_2', '{"name": "Nugget #00002", "mediaType": "image/png", "image": "ipfs://QmcLyRkuUQiSzAu9xJNDffMuixLKngELnd26Yqmzw28q12", "attributes": {"Rarity": "Common", "Base Shape": "Oval", "Color": "Spicy", "Batter Vector": "[1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]", "Background": "White", "Crispiness": "20.4278%", "Hat": "Top Hat (A)", "Sauce 1": "None", "Sauce 2": "None", "Id": 2, "Batch": 1}, "description": ["Generative nuggets and delicious sauces", "living on the Cardano Blockchain.", "Dipping is encouraged."]}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'Nugget_3', '{"name": "Nugget #00003", "mediaType": "image/png", "image": "ipfs://Qmf7cSTf7B4tgCPA2P5vht26EVq3AynCYZeVdjWKeQYHx6", "attributes": {"Rarity": "Common", "Base Shape": "Boot", "Color": "Spicy", "Batter Vector": "[0, 1, 1, 0, 0, 0, 1, 0, 1, 1]", "Background": "None", "Crispiness": "39.7118%", "Hat": "None", "Sauce1": "None", "Sauce 2": "None", "Id": 3, "Batch": 1}, "description": ["Generative nuggets and delicious sauces", "living on the Cardano Blockchain.", "Dipping is encouraged."]}' 
UNION ALL SELECT '424deb9056d16add0ae37cc654f8f4ae17e99efa9dd9fe5f8df1823c', 'Sauce_1', '{"name": "Fancy Ketchup #39", "image": "ipfs://QmbBG7XtMBHsKMqXCPebMo8Nv7jbNL1r789KHowS7s9gs1", "mediaType": "image/jpeg", "files": [{"src": "ipfs://QmPQnDGmeqh1aVCo2iz4WumNT4F1XstBqo5pD6nqgnLEGK", "name": "FancyKetchup", "mediaType": "video/mp4"}], "attributes": {"Rarity": "Common", "Id": "104", "Batch": "1", "Type": "Fancy Ketchup"}, "description": ["Generative nuggets and delicious sauces", "living on the Cardano Blockchain.", "Dipping is encouraged."]}';

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
