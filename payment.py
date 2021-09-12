from utxo import Utxo

def return_payment(payment_id: int, payment_addr: str, utxo: Utxo):
    print(f"Returning payment {payment_id} {utxo}")
