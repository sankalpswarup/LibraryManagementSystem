from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
key="DJANGO_KEY="+get_random_string(50, chars)
outF = open(".env", "w")
outF.write(key)
outF.close()