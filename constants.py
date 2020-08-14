frequency_bands = {
	'900E': {
			'downlink': {
				'start': 925.2,
				'end': 958.8
			},
			'uplink': {
				'start': 880.2,
				'end':914.8 
			}
		},
	'1800DCS': {
			'downlink': {
				'start': 1805.2,
				'end': 1879.8
			},
			'uplink': {
				'start': 1710.2,
				'end':1784.8 
			}
		},	
	
	'1':
		{
			'downlink': {
				'start': 2110,
				'end': 2170
			},
			'uplink': {
				'start': 1920,
				'end':1980 
			}
		},
	'2':
		{
			'downlink': {
				'start': 1930,
				'end': 1990
			},
			'uplink': {
				'start': 1850,
				'end':1910 
			}
		},
	'3':
		{
			'downlink': {
				'start': 1805,
				'end': 1880
			},
			'uplink': {
				'start': 1710,
				'end':1785 
			}
		}

}

LTE_arfcn_table = {
    'Band1':{'FDL_low':2110, 'NDL_low': 0, 'FDL_high': 2170, 'NDL_high': 599, 'NOffs-DL':0, 'FUL_low': 1920, 'NUL_low': 18000, 'FUL_high': 1980, 'NUL_high': 18599, 'NOffs-UL':18000, 'spacing': 190},
    'Band2':{'FDL_low':1930, 'NDL_low': 600, 'FDL_high': 1990, 'NDL_high': 1199, 'NOffs-DL':600, 'FUL_low': 1850, 'NUL_low': 18600, 'FUL_high': 1910, 'NUL_high': 19199, 'NOffs-UL':18600, 'spacing': 80},
    'Band3':{'FDL_low':1805, 'NDL_low': 1200, 'FDL_high': 1880, 'NDL_high': 1949, 'NOffs-DL':1200, 'FUL_low': 1710, 'NUL_low': 19200, 'FUL_high': 1785, 'NUL_high': 19949, 'NOffs-UL':19200, 'spacing': 95},
	'Band8':{'FDL_low':925, 'NDL_low': 3450, 'FDL_high': 960, 'NDL_high': 3799, 'NOffs-DL':3450, 'FUL_low': 880, 'NUL_low': 21450, 'FUL_high': 915, 'NUL_high': 21799, 'NOffs-UL':21450, 'spacing': 45},
    'Band20':{'FDL_low':791, 'NDL_low': 6150, 'FDL_high': 821, 'NDL_high': 6449, 'NOffs-DL':6150, 'FUL_low': 832, 'NUL_low': 24150, 'FUL_high': 862, 'NUL_high': 24449, 'NOffs-UL':24150, 'spacing': -41 },
	'Band38':{'FDL_low':2570, 'NDL_low': 37750, 'FDL_high': 2610, 'NDL_high': 38249, 'NOffs-DL':37750}
}

GSM_arfcn_table = {
    '900E':{'FDL_low': 925.2, 'FDL_high': 959.8, 'FUL_low': 880.2, 'FUL_high': 914.8, 'spacing': 45},
    '900R':{'FDL_low': 921.2, 'FDL_high': 959.8, 'FUL_low': 876.2, 'FUL_high': 914.8, 'spacing': 45},
    '900P':{'FDL_low': 935.2, 'FDL_high': 959.8, 'FUL_low': 890.2, 'FUL_high': 914.8, 'spacing': 45}
}

UMTS_arfcn_table = {
    'Band1':{'NDL_low':10562, 'NDL_high': 10838, 'NOffs-DL': 0, 'NUL_low':9612, 'NUL_high':9888, 'NOffs-UL': 0},
    'Band8':{'NDL_low':2937, 'NDL_high': 3088, 'NOffs-DL': 340, 'NUL_low':2712, 'NUL_high':2863, 'NOffs-UL': 340}
}

