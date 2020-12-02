# -*- coding: utf-8 -*-
from __future__ import division


from prepare_dataset import prepare_dataset
from define_tax_incidence_data import *


def compute_gains_losses(df_hh):
    """ load dataset """
    
    initial_variables = df_hh.columns.tolist()      
    for element in ['gasoline', 'diesel', 'domestic_fuel', 'natural_gas_variable']:
    
        """ Fix parameters : """
        
        i = 0.8
        current_carbon_price = 44.6 # Carbon tax in 2018
        adjusted_carbon_price = 44.6 + 50 # Carbon tax that we simulate
            
        if element == 'gasoline':
            current_price = 1.441 # This is the value of gasoline prices
            e = -0.4
            carbon_intensity = 0.002286
            initial_excise_tax = 0.6069 - 0.026 # This is the value of the TICPE without carbon tax
        elif element == 'diesel':
            current_price = 1.399 # This is the value of diesel prices
            e = -0.4
            carbon_intensity = 0.002651
            initial_excise_tax = 0.4284 + 2*0.026 # This is the value of the TICPE without carbon tax
        elif element == 'domestic_fuel':
            current_price = 0.859 # This is the value of domestic fuel prices
            e = -0.2
            carbon_intensity = 0.00265
            initial_excise_tax = 0.038 # This is the value of the TICPE without carbon tax
        else:
            current_price = 0.0651 # This is the unitary price of natural gas
            e = -0.2
            carbon_intensity = 0.000182
            initial_excise_tax = 0.0003 # This is the level of the TICGN if the carbon price was null
        
        """ Compute remaining parameters : """
        adjusted_carbon_tax = carbon_tax(adjusted_carbon_price, carbon_intensity)
        current_carbon_tax = carbon_tax(current_carbon_price, carbon_intensity)
        
        adjusted_excise_tax = excise_tax(adjusted_carbon_tax, initial_excise_tax)
        current_excise_tax = excise_tax(current_carbon_tax, initial_excise_tax)
        
        new_final_price = final_price_adjusted(current_price, i, adjusted_excise_tax, current_excise_tax)
        growth_final_price = variation_final_price(i, current_price, adjusted_excise_tax, current_excise_tax)
        
        current_price_without_tax = price_without_tax(current_price, current_excise_tax)
        new_price_without_tax = price_without_tax(new_final_price, adjusted_excise_tax)
    
    
        """ Compute tax incidence : """
        df_hh['{}_quantity'.format(element)] = df_hh['{}_expenditures'.format(element)] / current_price
        df_hh = adjusted_quantity_data(e, growth_final_price, df_hh, element)
    
        df_hh = adjusted_expenditures_data(e, growth_final_price, df_hh, element)
        df_hh['{}_expenditures_increase'.format(element)] = df_hh['{}_adjusted_expenditures'.format(element)] - df_hh['{}_expenditures'.format(element)]
    
        df_hh = taxes_data(current_price_without_tax, current_excise_tax, df_hh, element)
        df_hh = taxes_data(new_price_without_tax, adjusted_excise_tax, df_hh, '{}_adjusted'.format(element))
        df_hh['{}_tax_increase'.format(element)] = df_hh['{}_adjusted_taxes'.format(element)] - df_hh['{}_taxes'.format(element)]
    
    
    df_hh['transport_expenditures_increase'] = (
        df_hh['gasoline_expenditures_increase'] + df_hh['diesel_expenditures_increase']
        )
    df_hh['housing_expenditures_increase'] = (
        df_hh['domestic_fuel_expenditures_increase'] + df_hh['natural_gas_variable_expenditures_increase']
        )
    df_hh['total_expenditures_increase'] = (
        df_hh['transport_expenditures_increase'] + df_hh['housing_expenditures_increase']
        )
    df_hh['transport_tax_increase'] = (
        df_hh['gasoline_tax_increase'] + df_hh['diesel_tax_increase']
        )
    df_hh['housing_tax_increase'] = (
        df_hh['domestic_fuel_tax_increase'] + df_hh['natural_gas_variable_tax_increase']
        )
    df_hh['total_tax_increase'] = (
        df_hh['transport_tax_increase'] + df_hh['housing_tax_increase']
        )
    
    try:
        df_hh['nb_adults'] = df_hh['nb_persons'] - df_hh['nb_children']
    except:
        df_hh['nb_adults'] = df_hh['plus_18']
    df_hh['nb_beneficiaries'] = 2 - 1 * (df_hh['nb_adults'] == 1)
    
    return df_hh[initial_variables + ['housing_expenditures_increase'] + ['housing_tax_increase'] +
        ['transport_expenditures_increase'] + ['transport_tax_increase'] +
        ['total_expenditures_increase'] + ['total_tax_increase'] + ['nb_beneficiaries']]


if __name__ == "__main__":
    df_hh = prepare_dataset()
    df_hh = compute_gains_losses(df_hh)
    revenue_from_tax_transports = (df_hh['hh_weight'] * df_hh['transport_tax_increase']).sum()
    revenue_from_tax_housing = (df_hh['hh_weight'] * df_hh['housing_tax_increase']).sum()
    revenue_from_tax_total = (df_hh['hh_weight'] * df_hh['total_tax_increase']).sum()

    print "Revenue from trannsport fuels tax policy in billions euros :", revenue_from_tax_transports / 1e09
    print "Revenue from housing energies tax policy in billions euros :", revenue_from_tax_housing / 1e09
    print "Revenue from the total policy in billions euros :", revenue_from_tax_total / 1e09
    print "Dividend to be redistributed per adult :", revenue_from_tax_total / 50891106 # number of adults in metropolitan France in 2018
