from output_util import print_error
from datetime import datetime as dt


def check_pin_code(pin_code):
    if len(pin_code) != 4 or not pin_code.isdecimal():
        print_error('Pin code should have length 4 and contain only digits')
    return pin_code


def check_name(name):
    if len(name) > 128 or not name.isalpha():
        print_error('Name should have length at most 128 and contain only letters')
    return name


def check_phone_number(phone_number):
    if len(phone_number) != 12 or not phone_number[1:].isdecimal() or phone_number[0] != '+':
        print_error('Incorrect phone number')
    return phone_number[1:]


def check_date(date_str):
    try:
        date = dt.strptime(date_str, '%H:%M %d.%m.%Y')
    except ValueError:
        print_error('Expiration date is invalid')

    delta = int((date - dt.now()).total_seconds())
    if delta <= 0:
        print_error('Expiration date is invalid')
    return delta


def check_ticket(ticket):
    return ticket


def check_message(message):
    if len(message) != 140:
        print_error('Message should have length 140')
    return message
