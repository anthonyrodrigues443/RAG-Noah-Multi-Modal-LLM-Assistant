def has_letters_and_numbers(s):
    has_letter = False
    has_digit = False

    for char in s:
        if char.isalpha():
            has_letter = True
        elif char.isdigit():
            has_digit = True
        
        # If both are found, short-circuit the loop
        if has_letter and has_digit :
            return True
    
    return False
