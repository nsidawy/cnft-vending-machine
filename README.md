# Cardano NFT Vending Machine

This repository contains a generic application for a Cardano NFT vending machine with the following functionality:

* Montiors addresses for incoming transactions.
* Matches payment amounts to a set of available NFT packs for sale.
* Automatically mints NFTs, sends the NFT(s) to the buyer, and sends funds to the seller.
* Handles automated refunds if incorrect funds are sent or NFTs have sold out.
* Supports complex payments that may include other NFTs.
* Completely configurable via a PostgreSql data model.

**Requires a local Cardano node running and Cardano CLI installed. Versions 1.34.0 and greater supported. (Cardano Node Github)[https://github.com/input-output-hk/cardano-node]  
