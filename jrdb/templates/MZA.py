from jrdb.templates.template import Template


class MZA(Template):
    """
    http://www.jrdb.com/program/Msa/msa_doc.txt
    """
    name = '抹消馬'
    items = [
        ['pedigree_registration_number', '血統登録番号', None, '8', 'X', '1', None],
        ['reserved', '予備', None, '11', 'X', '292', 'スペース'],
        ['newline', '改行', None, '2', 'X', '303', 'ＣＲ・ＬＦ']
    ]
