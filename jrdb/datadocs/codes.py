"""
脚質コード（競走馬が得意とする走り）
過去の競走実績よりその馬の脚質を判断したコード。

1 逃げ Front runner
2 先行 Stalker
3 差し Off the pace
4 追込 Off the pace stretch runner
5 好位差し Off the pace good position http://www.kei-bank.com/dic/205
6 自在 Versatile http://www.kei-bank.com/style/jizai
"""
RUNNING_STYLE = {
    1: 'FRONT_RUNNER',
    2: 'STALKER',
    3: 'OTP',
    4: 'OTP_STRETCH_RUNNER',
    5: 'OTP_GOOD_POS',
    6: 'VERSATILE'
}
