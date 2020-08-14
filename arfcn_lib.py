import constants

def ArfcnToFreq(tech, arfcn):

    if (tech == 'UMTS'):

        arfcn_table = constants.UMTS_arfcn_table
       
        # Find band containing arfcn
        # Search downlinks
        found_offset = False
        for key,value in arfcn_table.items():
            if int(arfcn) >= int(value['NDL_low']) and int(arfcn) <= int(value['NDL_high']):
                offset = value['NOffs-DL']
                found_offset = True

        if found_offset:
            freq_DL = int(arfcn)/5 + offset
            return freq_DL 
        else:
            print ('Cant find band (arfcn range) in UMTS')
            return 0
    if (tech == 'LTE'):
        arfcn_table = constants.LTE_arfcn_table
       
        # Find band containing arfcn
        # Search downlinks
        found_offset = False
        for key,value in arfcn_table.items():
            if int(arfcn) >= int(value['NDL_low']) and int(arfcn) <= int(value['NDL_high']):
                offset = value['NOffs-DL']
                freq_DL_low = value['FDL_low']
                found_offset = True

        if found_offset:
            print (offset, freq_DL_low, arfcn)
            freq_DL = int(freq_DL_low) + 0.1*(int(arfcn) - int(offset))
            return freq_DL 
        else:
            print ('Cant find band (arfcn range) in LTE')
            return 0

    else:
        print ('Cant find technology')
        return 0


