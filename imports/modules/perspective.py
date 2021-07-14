from googleapiclient import discovery
import json,os

client=discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=os.environ["P_API_KEY"],
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

def istoxic(txt:str,per:int=95):
    perc=getscore(txt)
    if perc>per:
        return True
    else:
        return False
    
def getscore(text:str):
    analyze_request={
        "comment": {"text": text},
        "requestedAttributes": {"PROFANITY": {}}
    }
    try:
        res=json.loads(json.dumps(client.comments().analyze(body=analyze_request).execute()))
        perc=float(res["attributeScores"]["PROFANITY"]["summaryScore"]["value"])*100
    except:
        perc=50
    print(perc)
    return perc
