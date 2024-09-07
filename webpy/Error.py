import json

def errorResult(code, reason):
    return json.dumps({'code': code, 'reason': reason})

