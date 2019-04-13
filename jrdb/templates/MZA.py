from jrdb.templates.template import Template
from jrdb.templates.item import StringItem


class MZA(Template):
    """
    http://www.jrdb.com/program/Msa/msa_doc.txt
    """
    name = '抹消馬'
    items = [
        StringItem('血統登録番号', 8, 0, 'jrdb.Horse.pedigree_reg_num'),
    ]
