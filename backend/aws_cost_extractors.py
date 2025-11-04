import boto3
import json
from datetime import datetime, timedelta
from typing import List,Dict,Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class awsExtractor:
  def __init__(self,region:str="us-east-1"):
        self.ce_client = boto3.client("ce", region_name=region)
        self.ec2_client=boto3.client("ec2",region_name=region)
        logger.info("AWS Cost Extractor Initialized")
    

  def get_cost_and_uage(self,days:int=30,granularity:str="DAILY",metrics:List[str]=None)->Dict[str,Any]:
      if metrics is None:
          metrics = ["BlendedCost", "UsageQuantity"]
      endDate = datetime.now().date()
      startdate = endDate - timedelta(days=days)
      try:
          response = self.ce_client.get_cost_and_usage(
              TimePeriod={
                  'Start': startdate.strftime("%Y-%m-%d"),
                  'End': endDate.strftime("%Y-%m-%d")
              },
              Granularity=granularity,
              Metrics=metrics,
              GroupBy=[
                  {"Type": "DIMENSION", "Key": "SERVICE"},
                  {"Type": "DIMENSION", "Key": "REGION"}
              ],
              Filter={
                  "Dimensions": {
                      "Key": "PURCHASE_TYPE",
                      "Values": ["On Demand", "Reserved"]
                  }
              }
          )
          logger.info("Cost and Usage Data Extracted")
          return response
      except Exception as e:
          logger.info(f"Error retrieving cost data: {str(e)}")
          raise
      
  def get_services_breakdown(self,days:int =30)-> List[Dict[str, Any]]:
      response=self.get_cost_and_uage(days=days)
      service_costs=[]

      for result in response.get("ResultsByTime",[]):
          for group in result.get("groups",[]):
              server_name=None
              region=None
              for key in group.get("keys",[]):
                  if key.startwith("Amazone"):
                    server_name=key
                  else:
                    region=key

            
              metrics=group.get("Metrics",{})
              service_costs.append({
                 "service":server_name,
                 "region":region,
                 "cost":float(metrics.get("BlendedCost",{}).get("Amount",0)),
                 
                 
           





              })



         
           
if __name__ == "__main__":
    ce = awsExtractor()
    cost_and_usage = ce.get_cost_and_uage(days=30, granularity="DAILY", metrics=None)
    print(cost_and_usage)
