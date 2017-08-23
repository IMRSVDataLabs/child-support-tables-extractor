PROVINCES = {'ONTARIO': 'ontario',
             'QUEBEC/QUÉBEC': 'quebec',
             'NOVA SCOTIA/NOUVELLE-ÉCOSSE': 'nova_scotia',
             'NEW BRUNSWICK/NOUVEAU-BRUNSWICK': 'new_brunswick',
             'MANITOBA': 'manitoba',
             'BRITISH COLUMBIA/COLOMBIE-BRITANNIQUE': 'british_columbia',
             'PRINCE EDWARD ISLAND/ÎLE-DU-PRINCE-ÉDOUARD': 'prince_edward_island',
             'SASKATCHEWAN': 'saskatchewan',
             'ALBERTA': 'alberta',
             'NEWFOUNDLAND AND LABRADOR/TERRE-NEUVE-ET-LABRADOR': 'newfoundland_and_labrador',
             'YUKON': 'yukon',
             'NORTHWEST TERRITORIES/TERRITOIRES DU NORD-OUEST': 'northwest_territories',
             'NUNAVUT': 'nunavut'}


def _isfloat(s):
    try:
        float(s)
    except:
        return False
    else:
        return True
