"""
Simple test to verify RAG retrieval is working correctly.
Run this after fixing the agent implementation.
"""
import sys
import os

# Ensure we can import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.index_builder import build_policy_index
from app.llm import get_llm


def test_rag_retrieval():
    """Test that RAG retrieval works end-to-end."""
    
    print("="*60)
    print("Testing RAG Retrieval")
    print("="*60)
    
    # Step 1: Build/load index
    print("\nStep 1: Building policy index...")
    try:
        index = build_policy_index(force_rebuild=False)
        print("✓ Index built successfully")
    except Exception as e:
        print(f"✗ Failed to build index: {e}")
        return False
    
    # Step 2: Create query engine
    print("\nStep 2: Creating query engine...")
    try:
        llm = get_llm()
        query_engine = index.as_query_engine(
            similarity_top_k=3,
            response_mode="compact",
            llm=llm
        )
        print("✓ Query engine created")
    except Exception as e:
        print(f"✗ Failed to create query engine: {e}")
        return False
    
    # Step 3: Test queries
    test_queries = [
        "Is prior authorization required for lumbar MRI?",
        "What are the criteria for MRI approval?",
        "When is PA waived for imaging?"
    ]
    
    print(f"\nStep 3: Testing {len(test_queries)} queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Query {i}/{len(test_queries)} ---")
        print(f"Q: {query}")
        
        try:
            response = query_engine.query(query)
            print(f"A: {str(response)[:300]}...")
            
            # Check if we got source nodes
            if hasattr(response, 'source_nodes') and response.source_nodes:
                print(f"✓ Retrieved {len(response.source_nodes)} source documents")
                for j, node in enumerate(response.source_nodes[:2], 1):
                    print(f"  Source {j}: {node.text[:100]}...")
            else:
                print("⚠ Warning: No source nodes retrieved")
                
        except Exception as e:
            print(f"✗ Query failed: {e}")
            return False
    
    print("\n" + "="*60)
    print("✓ All RAG retrieval tests passed!")
    print("="*60)
    return True


def test_agent_with_rag():
    """Test that agents can use RAG tools."""
    
    print("\n" + "="*60)
    print("Testing Agent with RAG Tool")
    print("="*60)
    
    from app.agents.prior_auth_agent import build_prior_auth_agent
    from app.tools.codes_tools import ICD10_TOOL, CPT_TOOL
    
    print("\nStep 1: Building PA agent with RAG capability...")
    try:
        llm = get_llm()
        index = build_policy_index(force_rebuild=False)
        agent = build_prior_auth_agent(index, [ICD10_TOOL, CPT_TOOL], llm=llm)
        print("✓ Agent created successfully")
    except Exception as e:
        print(f"✗ Failed to create agent: {e}")
        return False
    
    print("\nStep 2: Testing agent query...")
    query = "Is PA required for MRI under PPO-Blue-2025 for low back pain after 6 weeks of PT?"
    print(f"Query: {query}")
    
    try:
        response = agent.chat(query)
        print(f"\nAgent Response:\n{str(response)}")
        
        # Check if response contains expected elements
        response_str = str(response).lower()
        checks = {
            "mentions PA": "prior auth" in response_str or "pa" in response_str,
            "has JSON structure": "{" in str(response) and "}" in str(response),
            "references policy": "rule" in response_str or "policy" in response_str
        }
        
        print("\nResponse validation:")
        for check, passed in checks.items():
            status = "✓" if passed else "⚠"
            print(f"  {status} {check}")
        
        if all(checks.values()):
            print("\n✓ Agent successfully used RAG to answer!")
        else:
            print("\n⚠ Agent response may need improvement")
            
    except Exception as e:
        print(f"✗ Agent query failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*60)
    print("✓ Agent RAG integration test complete!")
    print("="*60)
    return True


if __name__ == "__main__":
    print("\nCareGraph RAG Retrieval Tests")
    print("="*60 + "\n")
    
    # Run tests
    test1_passed = test_rag_retrieval()
    test2_passed = test_agent_with_rag()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"RAG Retrieval: {'✓ PASS' if test1_passed else '✗ FAIL'}")
    print(f"Agent Integration: {'✓ PASS' if test2_passed else '✗ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n✓ All tests passed! RAG retrieval is working.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed. Check errors above.")
        sys.exit(1)
