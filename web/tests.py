from django.test import TestCase
from utils.check_code import create_validate_code

img,code = create_validate_code()

print(code)
