# Cardano NFT Vending Machine

This repository contains a generic application for a Cardano NFT vending machine.

It has the following functionality:
* Montiors addresses for incoming transactions.
* Matches payment amounts to a set of available NFT packs for sale.
* Automatically mints NFTs, sends the NFT(s) to the buyer, and sends funds to the seller.
* Handles automated refunds if incorrect funds are sent or NFTs have sold out.
* Supports complex payments that may include other NFTs.
* Completely configurable via a PostgreSql data model.
