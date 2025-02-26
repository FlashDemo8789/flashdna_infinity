PATTERNS= [
  {
    "name": "Strong Founder Experience",
    "criteria": [
      {"metric":"founder_domain_exp_yrs","op":">","value":4},
      {"metric":"founder_exits","op":">","value":0}
    ]
  },
  {
    "name":"High Referral",
    "criteria": [
      {"metric":"referral_rate","op":">","value":0.08}
    ]
  }
]

def meets_criterion(value, operator, threshold):
    if operator==">": return value>threshold
    elif operator==">=": return value>=threshold
    elif operator=="<": return value<threshold
    elif operator=="<=": return value<=threshold
    elif operator=="==": return value==threshold
    return False

def detect_patterns(doc: dict):
    matched=[]
    for pat in PATTERNS:
        ok= True
        for crit in pat["criteria"]:
            m= crit["metric"]
            op= crit["op"]
            tv= crit["value"]
            val= doc.get(m,0)
            if not meets_criterion(val, op, tv):
                ok= False
                break
        if ok:
            matched.append(pat["name"])
    return matched