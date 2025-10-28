#!/usr/bin/env python3
"""
Test script to verify data retrieval from ChromaDB
"""

import sys
from chromadb_store import ChromaDBStore
from finops_chatbot import FinOpsChatbot

print("=" * 80)
print("Testing Data Retrieval from ChromaDB")
print("=" * 80)

# Test 1: Check ChromaDB stats
print("\n1. Checking ChromaDB Collection Stats...")
store = ChromaDBStore()
stats = store.get_collection_stats()
print(f"   Cost records: {stats.get('cost_records', 0)}")
print(f"   Resource records: {stats.get('resource_records', 0)}")
print(f"   Optimization records: {stats.get('optimization_records', 0)}")

if stats.get('cost_records', 0) == 0:
    print("\n   ⚠️  WARNING: No data in ChromaDB!")
    print("   You need to sync AWS data first:")
    print("   curl -X POST http://localhost:5000/api/sync -H 'Content-Type: application/json' -d '{\"days\": 30}'")
    sys.exit(1)

# Test 2: Search for resources
print("\n2. Searching for Resources...")
resources = store.search_resources("running", limit=5)
print(f"   Found {len(resources)} resources")
if resources:
    for i, resource in enumerate(resources[:3], 1):
        print(f"   {i}. {resource.get('instance_id')} ({resource.get('instance_type')}) - {resource.get('state')}")

# Test 3: Search for costs
print("\n3. Searching for Costs...")
costs = store.search_costs("EC2", limit=5)
print(f"   Found {len(costs)} cost entries")
if costs:
    for i, cost in enumerate(costs[:3], 1):
        print(f"   {i}. {cost.get('service')}: ${cost.get('cost'):.2f}")

# Test 4: Search for optimizations
print("\n4. Searching for Optimizations...")
optimizations = store.search_optimizations("savings", limit=3)
print(f"   Found {len(optimizations)} optimization insights")
if optimizations:
    for i, opt in enumerate(optimizations[:3], 1):
        print(f"   {i}. {opt.get('title')} - ${opt.get('savings'):.2f}")

# Test 5: Test chatbot query
print("\n5. Testing Chatbot Query...")
chatbot = FinOpsChatbot()
result = chatbot.query("What resources do I have?")
print(f"   Response: {result.get('response', 'No response')[:200]}...")
print(f"   Relevant resources found: {len(result.get('relevant_resources', []))}")
print(f"   Relevant costs found: {len(result.get('relevant_costs', []))}")

print("\n" + "=" * 80)
print("Test Complete!")
print("=" * 80)
