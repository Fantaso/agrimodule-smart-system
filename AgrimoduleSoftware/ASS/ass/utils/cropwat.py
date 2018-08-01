# Variables

# factors affecrting eto are only climatic factors, so it can be calculated based on only weather data
# evaporating power of atmosphere in a specific location and time
ETo = 'reference crop evapotranspiration [mm / day]'

# factor considered:
# disease-free, well-fertilized crops, grown in large fields under optimun water conditions and achive full production under given climatic condiitions
# etc will be aprox. 1-9 mm/day from cool to warn average temparatures
ETc = 'crop evapotranspiration under standard conditions'

# weather
direct_solar_radiation = ''
air_temperature = ''
air_relative_humidity = ''
wind_speed = ''

# crop
crop_transpiration_resistance = ''
crop_roughness = ''
crop_height = ''
crop_reflection = ''
crop_ground_cover = ''
crop_root_characteristics = ''
crop_density = ''

# soil
soil_salinity = ''
soil_fertility = ''
soil_roughness = ''
soil_water_content = ''


# EQUATION FOR AN EVAPORATING SURFACE
	# Rn: net radiation at crop surface [MJ]/ pow(m, 2) * day]
	# H: sensible heat
	# G: soil heat flux [MJ / pow(m, 2) * day]
	# ƛ * ET: latent heat flux
Rn - G - ƛET - H = 0

# PENMAN-MONTEITH EQUATION
	# Rn = net radiation
	# (es - ea) = s the vapour pressure deficit of the air [kPa]
	# ∆ =  the slope of the saturation vapour pressure temperature relationship
	# γ = psychrometric constant
	# rs, ra = (bulk) surface and aerodynamic resistances
	# Pa = the mean air density at constant pressure
	# Cp = the specific heat of the air
ƛET = (∆ * (Rn - G) + Pa * Cp * ((Es - Ea) / ra)) / (∆ + γ * (1 + (rs / ra)))

# AREODYNAMIC RESISTANCE (ra)
	# ra = aerodynamic resistances [s pow(m, -1)]
	# Zm = height of wind measurements [m] meters
	# Zh = height of humidity measurements [m] meters
	# d = zero plane displacement height [m] meters
	# Zom = roughness length governing momentum transfer [m] meters
	# Zoh = roughness length governing transfer of heat and vapour [m] meters
	# k = von Karman's constant, 0.41 [None]
	# Uz = wind speed at height z [s pow(m, -1)]
from math import log, pow
ra = (log((Zm - d) / Zom) * log((Zh - d) / Zoh)) / (pow(K, 2) * Uz)

# (BULK) SURFACE RESISTANCE (rs)
	# rs = (bulk) surface resistances [s pow(m, -1)]
	# rl = bulk stomatal resistance of the well-illuminated leaf [s pow(m, -1)]
	# LAI_active = active (sunlit) leaf area index [pow(m, 2) (leaf area) pow(m, -2) (soil surface)] meters
		# The LAI values for various crops differ widely but values of 3-5 are common for many mature crops. For a given
		# crop, green LAI changes throughout the season and normally reaches its maximum before or at flowering
		# LAI further depends on the plant density and the crop variety.
		# A general equation for LAIactive is: LAI_active = 0.5 LAI
			# which takes into consideration the fact that generally only the upper half of dense clipped grass is actively
			# contributing to the surface heat and vapour transfer. For clipped grass a general equation for LAI is:
			# LAI = 24 * h
			# where h is the crop height [m] meter
			# The stomatal resistance, rl of a single leaf has a value of about 100 s m-1 under well-watered conditions
LAI = 24 * crop_height
LAI_active = 0.5 * LAI

rs = rl / LAI_active

# REFERENCE CROP EVAPOTRANSPIRATION
	# ETo = reference evapotranspiration [mm / day]
	# Rn = net radiation at the crop surface [MJ / (pow(m, 2) * day]
	# G = soil heat flux density [MJ / (pow(m, 2) * day)]
	# T = mean daily air temperature at 2 m height [°C]
	# Uz = wind speed at z or 2 m height [m / s] # calculations should be done at 2 m height
	# es = saturation vapour pressure [kPa]
	# ea = actual vapour pressure [kPa]
	# es - ea = saturation vapour pressure deficit [kPa]
	# ∆ = slope vapour pressure curve [kPa / °C]
	# γ = psychrometric constant [kPa / °C]

Eto = (0.408 * ∆ * (Rn - G) + γ * (900 / (T + 273)) * Uz * (es - ea)) / (∆ + γ * (1 + 0.34 * Uz))

# ATMOSPHERIC PRESSURE [kPa]
	# z = elevation above sea level [m] meters
from math import pow
atmospheric_pressure = 101.3 * pow(((293 - 0.0065 * z) / 293), 5.26)

# PSYCHROMETRICS CONSTANT
	# γ = psychrometric constant [kPa / °C]
	 # λ = latent heat of vaporization, 2.45 [MJ / kg]
	 # Cp = specific heat at constant pressure, 1.013 10-3 [MJ / kg * °C]
	 # ε = ratio molecular weight of water vapour/dry air = 0.622
γ = (Cp * atmospheric_pressure) / (ε * λ)
γ_alternative = 0.665e-3 * atmospheric_pressure

# AIR TEMPERATURE
	# temperature in KELVIN
kelvin = centigrades + 273.16
T_mean = (T_max - T_min) / 2

# RELATIVE HUMIDITY
	# The relative humidity (RH) expresses the degree of saturation of the air as a ratio of the actual (ea) to the
	# saturation (eo(T)) vapour pressure at the same temperature (T):
RH = 100 * (ea / eo)

# MEAN SATURATION VAPOUR PRESSURE (es)
	# As saturation vapour pressure is related to air temperature, it can be calculated from the air temperature. The relationship is expressed by
	# eo(T) saturation vapour pressure at the air temperature T [kPa]
	# air_temp = air temperature [°C]
	# exp[..] 2.7183 (base of natural logarithm) raised to the power [..].
# //TODO check if eo formula is the right way to calculate this formula
from math import expm1, exp
eo = pow(0.6108, ((17.27 * air_temp) / (air_temp + 237.3)) # function based on temperature
es = (eo * (T_max + T_min)) / 2

# ACTUAL VAPOUR PRESSURE (ea) DERIVED FROM DEWPOINT TEMPERATURE
    # T_dew = dewpoint temperature [°C]
ea = eo * pow(0.6108, ((17.27 * T_dew) / (T_dew + 237.3)) # function based on temperature

# ACTUAL VAPOUR PRESSURE (ea) DERIVED FROM PSYCHROMETRIC DATA
    # ea = actual vapour pressure [kPa]
    # eo(T_wet) = saturation vapour pressure at wet bulb temperature [kPa]
    # γ_psy = psychrometric constant of the instrument [kPa / °C]
    # T_dry - T_wet = wet bulb depression, with T_dry the dry bulb and T_wet the wet bulb temperature [°C]
    # for γ_psy
        # 0.000662 for ventilated (Asmann type) psychrometers, with an air movement of some 5 m/s,
        # 0.000800 for natural ventilated psychrometers (about 1 m/s),
        # 0.001200 for non-ventilated psychrometers installed indoors.
ea = eo * T_wet - γ_psy * (T_dry - T_wet)

# ACTUAL VAPOUR PRESSURE (ea) DERIVED FROM RELATIVE HUMIDITY DATA
    # ea = actual vapour pressure [kPa]
    # eo_T_min = saturation vapour pressure at daily minimum temperature [kPa]
    # eo_T_max = saturation vapour pressure at daily maximum temperature [kPa]
    # RH_max = maximum relative humidity [%]
    # RH_min = minimum relative humidity [%]
# --for RH_max and RH_min
ea = (eo_T_min * (RH_max / 100) + eo_T_max * (RH_min / 100)) / 2

# --for RH_max -- When using equipment where errors in estimating RH min can be large, or when RH data integrity are in doubt, then one should use only RH max
ea = eo_T_min * (RH_max / 100)

# --for RH_mean -- In the absence of RH max and RH min , another equation can be used to estimate e a
    # RH_mean = the mean relative humidity, defined as the average between RH max and RH min .
ea = (RH_mean / 100) * ((eo_T_max + eo_T_min) / 2)

# VAPOUR PRESSURE DEFICIT (es - ea)
    ∆ =

∆ =
