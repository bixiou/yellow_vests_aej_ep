# -*- coding: utf-8 -*-

# Here we construct a very standard exemple to study the tax incidence on one consumer
# consuming 1000€ of domestic fuel per year, and not driving a car.

from __future__ import division


from define_tax_incidence import *


def domestic_fuel_example(expenditures):

    dict_fuel = dict()
    vat = 0.2
    e_housing = -0.2
    i = 0.8
    
    current_price = 0.859 # This is the value of domestic fuel prices
        
    old_carbon_tax = 44.6 # Carbon tax in 2018
    new_carbon_tax = 44.6 + 50 # Carbon tax that we simulate
    carbon_intensity = 0.002651 # Carbon content of gasoline (deduced from art 265 code des douanes)
    
    initial_excise_tax = 0.038
    
    # Compute tax rates :
    new_carbon_tax = carbon_tax(new_carbon_tax, carbon_intensity)
    old_carbon_tax = carbon_tax(old_carbon_tax, carbon_intensity)
    
    new_excise_tax = excise_tax(new_carbon_tax, initial_excise_tax)
    old_excise_tax = excise_tax(old_carbon_tax, initial_excise_tax)    #print "Excise tax (before/after)", old_excise_tax, "/", new_excise_tax
    
    
    # Compute prices :
    new_final_price = final_price_adjusted(current_price, i, new_excise_tax, old_excise_tax)
    final_price_variation = variation_final_price(i, current_price, new_excise_tax, old_excise_tax)
    
    current_price_without_tax = price_without_tax(current_price, old_excise_tax)
    new_price_without_tax = price_without_tax(new_final_price, new_excise_tax)
    
    
    # Compute quantities :
    current_quantity = quantity(current_price, expenditures)
    new_quantity = adjusted_quantity(current_quantity, e_housing, final_price_variation)
    
    
    # Compute expenditures :
    new_expenditures = adjusted_expenditures(expenditures, e_housing, final_price_variation)
    variation_expenditures = new_expenditures - expenditures
    
    
    # Compute taxes paid :
    current_taxes = taxes(current_price_without_tax, current_quantity, old_excise_tax)
    new_taxes = taxes(new_price_without_tax, new_quantity, new_excise_tax)

    dict_fuel['new_expenditures'] = new_expenditures
    dict_fuel['variation_expenditures'] = variation_expenditures
    dict_fuel['new_quantity'] = new_quantity
    dict_fuel['current_quantity'] = current_quantity
    dict_fuel['current_taxes'] = current_taxes
    dict_fuel['new_taxes'] = new_taxes

    return dict_fuel


if __name__ == "__main__":
    expenditures = 1000
    example = domestic_fuel_example(expenditures)
