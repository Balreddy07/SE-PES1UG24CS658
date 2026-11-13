
def parse_booking(text):
    if not isinstance(text, str):
        return None

    if text.count(':') != 1:
        return None

    pet, days = text.split(':')
    pet = pet.strip()

    if not pet:
        return None

    try:
        days = float(days.strip())
    except (ValueError, TypeError):
        return None

    if not pet or not (days >= 0 and days < float('inf')):
        return None

    return pet.title(), days


def stay_average(days_csv):
    if not isinstance(days_csv, str) or not days_csv.strip():
        return None

    try:
        values = [int(r.strip()) for r in days_csv.split(',')]
    except (ValueError, TypeError):
        return None

    if not values or any(value < 0 for value in values):
        return None

    return sum(values) // len(values)


def payable_fee(text):
    if not isinstance(text, str):
        return None

    if text.count('|') != 1:
        return None

    fee, discount = text.split('|')

    try:
        fee = float(fee.strip())
        discount = float(discount.strip())
    except (ValueError, TypeError):
        return None

    if not (0 <= fee < float('inf')) or not (0 <= discount < float('inf')):
        return None

    total = fee * 1.18 - discount
    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result)

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
