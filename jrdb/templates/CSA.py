from jrdb.templates.CZA import CZA


class CSA(CZA):
    """
    JRDB調教師データ（CSA）
    差分(今週出走分,先週成績更新分)

    http://www.jrdb.com/program/Cs/Cs_doc1.txt
    """
    name = 'JRDB調教師データ（CSA）'
