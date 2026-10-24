# functions.py

def get_valid_string(prompt):
    """Ensures the user doesn't enter empty strings."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: Input cannot be empty or whitespace.")

def get_valid_integer(prompt, min_value=1):
    """Ensures the user enters a valid positive integer."""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_value:
                return value
            else:
                print(f"Error: Value must be greater than or equal to {min_value}.")
        except ValueError:
            print("Error: Invalid input. Please enter a valid number.")

def format_currency(amount):
    """Formats numbers like 2400 to 2,400"""
    return f"Rs. {amount:,}"