# DATABASE INFO
# --------------


# database folder
DATABASE_FOLDER_NAME = "database"

# database info
DATABASE_INFO = [
    {
        "name": "GENERAL",
        "file": "data_general.csv"
    },
    {
        "name": "HEAT_CAPACITY_PRESSURE",
        "file": "data_heat_capacity_constant_pressure.csv"
    },
    {
        "name": "THERMAL_CONDUCTIVITY",
        "file": "data_thermal_conductivity.csv"
    },
    {
        "name": "VISCOSITY",
        "file": "data_viscosity.csv"
    },
    {
        "name": "VAPOR_PRESSURE",
        "file": "data_vapor_pressure.csv"
    },
    {
        "name": "ENTHALPY_AND_GIBBS_ENERGY_OF_FORMATION",
        "file": "data_enthalpy_and_gibbs_energy_of_formation.csv"
    },
    {
        "name": "GENERAL_CONSTANTS",
        "file": "CRITICAL CONSTANTS AND ACENTRIC FACTORS OF INORGANIC AND ORGANIC COMPOUNDS.csv"
    },
]


DB_GENERAL = [
    {
        "name": "GENERAL",
        "file": "data_general.csv"
    },
    {
        "name": "GENERAL",
        "file": "CRITICAL CONSTANTS AND ACENTRIC FACTORS OF INORGANIC AND ORGANIC COMPOUNDS.csv"
    },
]

DB_HEAT = [
    {
        "name": "ENTHALPY_AND_GIBBS_ENERGY_OF_FORMATION",
        "file": "data_enthalpy_and_gibbs_energy_of_formation.csv"
    },
]

DB_VAPOR_PRESSURE = [
    {
        "name": "VAPOR_PRESSURE",
        "file": "data_vapor_pressure.csv"
    },
    {
        "name": "VAPOR_PRESSURE",
        "file": "Vapor Pressure of Inorganic and Organic Liquids.csv"
    }
]

# general database info
DATABASE_GENERAL_ITEMS = ["MW", "Tc", "Pc", "w", "dHf25", "dGf25"]
DATABASE_GENERAL_ITEMS_FULL = [
    ["molecular weight", "MW", "g/mol"], ["critical temperature", "Tc", "K"], [
        "critical pressure", "Pc", "bar"],
    ["acentric factor", "w", "-"], ["standard enthalpy of formation", "dHf25", "kJ/mol"], [
        "Standard Gibbs free energy of formation", "dGf25", "kJ/mol"]
]
