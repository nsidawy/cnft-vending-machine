import pquery

class Dip:
    def __init__(self, payment_id: int, burned_nugget_nft_id: int, burned_sauce_nft_id: int, dipped_nugget_nft_id: int):
        self.payment_id = payment_id
        self.burned_nugget_nft_id = burned_nugget_nft_id
        self.burned_sauce_nft_id = burned_sauce_nft_id
        self.dipped_nugget_nft_id = dipped_nugget_nft_id

    def __str__(self):
        return f'Dip {{ PaymentId: {self.payment_id}, BurnedNuggetNftId: {self.burn}, burnedSauceNftId: {self.burned_sauce_nft_id}, dippedNuggetNftId: {self.dippedNuggetNftId} }}'

    def __repr__(self):
        return str(self)

def insert(payment_id: int, burned_nugget_nft_id: int, burned_sauce_nft_id: int, dipped_nugget_nft_id: int):
    pquery.write(f"""
        INSERT INTO dips (paymentId, burnedNuggetNftId, burnedSauceNftId, dippedNuggetNftId)
        VALUES ({payment_id}, {burned_nugget_nft_id}, {burned_sauce_nft_id}, {dipped_nugget_nft_id
        })
    """)
