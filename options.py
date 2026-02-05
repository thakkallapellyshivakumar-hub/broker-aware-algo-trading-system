def get_atm_strike(spot):
    return round(spot / 50) * 50

def option_symbol(index, strike, opt_type):
    return f"{index}{strike}{opt_type}"
