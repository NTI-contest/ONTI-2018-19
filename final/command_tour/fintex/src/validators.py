from argparse import Action

from checkers import check_pin_code, check_phone_number, check_date, check_ticket

from blockchain import pin_code_to_private_key, phone_to_address


# Substitutes pin with private_key
class PINPhoneValidate(Action):
    def __call__(self, parser, args, values, option_string=None):
        pin_code, phone_number = values
        res = [pin_code_to_private_key(pin_code), check_phone_number(phone_number)]
        setattr(args, self.dest, res)


# Substitutes pin with private_key
class PINTicketValidate(Action):
    def __call__(self, parser, args, values, option_string=None):
        pin_code, ticket = values
        res = [pin_code_to_private_key(pin_code), check_ticket(ticket)]
        setattr(args, self.dest, res)


# Substitutes pin with private_key
# Substitutes phone with address
class PersonValidate(Action):
    def __call__(self, parser, args, values, option_string=None):
        name, phone_number, pin_code = values
        res = [pin_code_to_private_key(name),
               phone_to_address(check_phone_number(phone_number)),
               check_pin_code(pin_code)]
        setattr(args, self.dest, res)


# Substitutes pin with private_key
class TransactValidate(Action):
    def __call__(self, parser, args, values, option_string=None):
        pin_code, phone_number, amount = values
        res = [pin_code_to_private_key(pin_code),
               check_phone_number(phone_number),
               int(amount)]
        setattr(args, self.dest, res)


# Substitutes pin with private_key
class ApproveValidate(Action):
    def __call__(self, parser, args, values, option_string=None):
        pin_code, value, date_to_expire = values
        res = [pin_code_to_private_key(pin_code), int(value), check_date(date_to_expire)]
        setattr(args, self.dest, res)
