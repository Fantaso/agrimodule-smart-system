'''CALCULATION OF ROP WATER REQUIREMENTS'''
why_methods = 'Primarily the choice of method must be based on the type of climatic data available and on the accuracy required in determining water needs.'
procedure = {   'first': 'The effect of climate on crop water requirement',
                'second': 'The effect of the crop characteristics on crop water requirements',
                'third': 'The effect of local conditions and agricultural practices on crop water requirements',
}
methods = [ 'Blaney-Criddle': {
                                'temperature': 'measured',
                                'humidity': 'estimated',
                                'wind': 'estimated',
                                'sunshine': 'estimated',
                                'radiation': None,
                                'evaporation': None,
                                'environment': 'estimated',
                                'environment': 'estimated',
                                'error tolerance': {'for longer periods of a month': '+-25%',
                                                    },
                                },
            'Radiation': {
                                'temperature': 'measured',
                                'humidity': 'estimated',
                                'wind': 'estimated',
                                'sunshine': 'measured',
                                'radiation': 'not essential',
                                'evaporation': None,
                                'environment': 'estimated',
                                'error tolerance': {'in extreme donditions': '+-20%',
                                                    },
                                },
            'Penman': {
                                'temperature': 'measured',
                                'humidity': 'measured',
                                'wind': 'measured',
                                'sunshine': 'measured',
                                'radiation': 'not essential',
                                'evaporation': None,
                                'environment': 'estimated',
                                'error tolerance': {'summer donditions': '+-10%',
                                                    'low evaporative conditions': '+-20%'
                                                    },
                                },
            'Pan Evaporation': {
                                'temperature': None,,
                                'humidity': 'estimated',
                                'wind': 'estimated',
                                'sunshine': None,
                                'radiation': None,
                                'evaporation': 'measured',
                                'environment': 'measured',
                                'error tolerance': {'depends on location': '+-15%',
                                                    },
                                },
            ]

eff
