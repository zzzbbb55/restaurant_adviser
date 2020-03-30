import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'restaurant_adviser.settings')

import django
django.setup()

from rest_adv.models import Restaurant
def test1():
    rest1={'name':'rest test1'}
    add_rest(rest1['name'])

def add_rest(name):
    r = Restaurant.objects.get_or_create(name=name)[0]
    r.rate = 0
    r.save()
    return r

if __name__ == '__main__':
    print('Starting rest population script...')
    test1()