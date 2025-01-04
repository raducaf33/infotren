from faker import Faker

fake = Faker()

# Generate a fake credit card number and details
credit_card = fake.credit_card_full()
print(credit_card)