#!/usr/bin/env python3
"""
Diagnostic script to identify why AWS data is not being retrieved
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("DIAGNOSTIC: AWS Data Retrieval Issue")
print("=" * 80)

# Step 1: Check AWS credentials
print("\n1. Checking AWS Credentials...")
aws_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION', 'us-east-1')

if aws_key and aws_secret:
    print(f"   ✓ AWS_ACCESS_KEY_ID: Found")
    print(f"   ✓ AWS_SECRET_ACCESS_KEY: Found")
    print(f"   ✓ AWS_REGION: {aws_region}")
else:
    print(f"   ✗ AWS credentials missing!")
    print(f"   AWS_ACCESS_KEY_ID: {aws_key}")
    print(f"   AWS_SECRET_ACCESS_KEY: {aws_secret}")
    sys.exit(1)

# Step 2: Test AWS connection
print("\n2. Testing AWS Connection...")
try:
    from aws_cost_extractor import AWSCostExtractor
    extractor = AWSCostExtractor(region=aws_region)
    print("   ✓ AWS Cost Extractor initialized")
    
    # Try to fetch data
    print("   Fetching EC2 instances...")
    instances = extractor.get_ec2_instances()
    print(f"   ✓ Found {len(instances)} EC2 instances")
    
    if instances:
        print(f"   Sample instance: {instances[0]}")
    else:
        print("   ⚠ No EC2 instances found in your AWS account")
    
    print("   Fetching cost data...")
    costs = extractor.get_service_breakdown(days=30)
    print(f"   ✓ Found {len(costs)} cost entries")
    
    if costs:
        print(f"   Sample cost: {costs[0]}")
    else:
        print("   ⚠ No cost data found")
        
except Exception as e:
    print(f"   ✗ Error: {str(e)}")
    sys.exit(1)

# Step 3: Check ChromaDB
print("\n3. Checking ChromaDB Storage...")
try:
    from chromadb_store import ChromaDBStore
    store = ChromaDBStore()
    stats = store.get_collection_stats()
    
    print(f"   Cost records: {stats.get('cost_records', 0)}")
    print(f"   Resource records: {stats.get('resource_records', 0)}")
    print(f"   Optimization records: {stats.get('optimization_records', 0)}")
    
    if stats.get('cost_records', 0) == 0:
        print("\n   ⚠ WARNING: No data in ChromaDB!")
        print("   This means data was never synced or was cleared.")
        print("\n   ACTION REQUIRED:")
        print("   1. Call POST /api/sync to sync AWS data")
        print("   2. Wait for sync to complete")
        print("   3. Then query the chatbot")
    
except Exception as e:
    print(f"   ✗ Error: {str(e)}")
    sys.exit(1)

# Step 4: Test data retrieval
print("\n4. Testing Data Retrieval from ChromaDB...")
try:
    resources = store.search_resources("running", limit=5)
    print(f"   Resources found: {len(resources)}")
    if resources:
        print(f"   Sample: {resources[0]}")
    
    costs = store.search_costs("EC2", limit=5)
    print(f"   Costs found: {len(costs)}")
    if costs:
        print(f"   Sample: {costs[0]}")
    
    optimizations = store.search_optimizations("savings", limit=3)
    print(f"   Optimizations found: {len(optimizations)}")
    if optimizations:
        print(f"   Sample: {optimizations[0]}")
        
except Exception as e:
    print(f"   ✗ Error: {str(e)}")
    sys.exit(1)

# Step 5: Test chatbot query
print("\n5. Testing Chatbot Query...")
try:
    from finops_chatbot import FinOpsChatbot
    chatbot = FinOpsChatbot()
    
    result = chatbot.query("What resources do I have?")
    print(f"   Response: {result.get('response', 'No response')[:150]}...")
    print(f"   Relevant resources: {len(result.get('relevant_resources', []))}")
    print(f"   Relevant costs: {len(result.get('relevant_costs', []))}")
    
except Exception as e:
    print(f"   ✗ Error: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)

print("\nNEXT STEPS:")
print("1. If AWS data is found but ChromaDB is empty:")
print("   → Call POST /api/sync to sync data")
print("\n2. If AWS data is not found:")
print("   → Check AWS credentials in .env")
print("   → Verify AWS account has resources")
print("   → Check IAM permissions")
print("\n3. If ChromaDB has data but queries return nothing:")
print("   → Restart Flask app: python app.py")
print("   → Check search query keywords")
