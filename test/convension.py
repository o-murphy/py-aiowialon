def snake_to_camel(snake_str):
    components = snake_str.split('_')
    # Capitalize the first letter of each component except the first one
    camel_case_str = ''.join(x.title() for x in components)
    # Ensure the first letter is lowercase
    return camel_case_str[0].lower() + camel_case_str[1:]
