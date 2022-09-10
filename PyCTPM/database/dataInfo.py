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
