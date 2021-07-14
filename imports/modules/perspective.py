from googleapiclient import discovery
import json,os

client=discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=os.environ["P_API_KEY"],
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

def istoxic(text:str,per:int=95):
    analyze_request={
        "comment": {"text": text},
        "requestedAttributes": {"PROFANITY": {}}
    }
    res=json.dumps(client.comments().analyze(body=analyze_request).execute())
    perc=res["attributeScores"]["PROFANITY"]["summaryScore"]["value"]*100
    if perc>per:
        return True
    else:
        return False
