def compute_team_depth_score(doc: dict)-> float:
    score=0.0
    e= doc.get("founder_exits",0)
    d= doc.get("founder_domain_exp_yrs",0)
    score+= e*10
    score+= min(d,10)
    if score>100: score=100
    return round(score,2)

def compute_moat_score(doc: dict)-> float:
    pat= doc.get("patent_count",0)
    brand= doc.get("brand_presence_score",50.0)
    val= pat*2 + brand*0.3
    if val>100: val=100
    return round(val,2)