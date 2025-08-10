#!/usr/bin/env python3
"""
Debug script to test the all-in-one workflow and identify issues
"""

import pandas as pd
import tempfile
import os
from student_data_comparator import StudentDataComparator

def create_sample_ai_data():
    """Create sample AI-extracted data"""
    sample_data = [
        {'Student Name': 'John Smith', 'Grade': '5', 'Address': '123 Main St'},
        {'Student Name': 'Jane Doe', 'Grade': '4', 'Address': '456 Oak Ave'},
        {'Student Name': 'Mike Johnson', 'Grade': '6', 'Address': '789 Pine Rd'}
    ]
    return pd.DataFrame(sample_data)

def create_sample_comparison_data():
    """Create sample comparison data with slightly different format"""
    sample_data = [
        {'Student Name': 'Smith, John', 'Grade Level': '5', 'Home Address': '123 Main Street'},
        {'Student Name': 'Doe, Jane', 'Grade Level': '4', 'Home Address': '456 Oak Avenue'},
        {'Student Name': 'Williams, Sarah', 'Grade Level': '3', 'Home Address': '321 Elm St'}
    ]
    return pd.DataFrame(sample_data)

def test_comparison():
    """Test the comparison logic"""
    print("🔍 Testing student data comparison...")
    
    # Create sample data
    ai_data = create_sample_ai_data()
    comparison_data = create_sample_comparison_data()
    
    print(f"📊 AI data shape: {ai_data.shape}")
    print(f"📊 AI columns: {list(ai_data.columns)}")
    print(f"📊 AI sample names: {ai_data['Student Name'].tolist()}")
    
    print(f"📊 Comparison data shape: {comparison_data.shape}")
    print(f"📊 Comparison columns: {list(comparison_data.columns)}")
    print(f"📊 Comparison sample names: {comparison_data['Student Name'].tolist()}")
    
    # Save to temporary files
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as ai_temp:
        ai_data.to_excel(ai_temp.name, index=False)
        ai_path = ai_temp.name
    
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as comp_temp:
        comparison_data.to_excel(comp_temp.name, index=False)
        comp_path = comp_temp.name
    
    try:
        # Test comparison
        comparator = StudentDataComparator()
        
        print("📥 Loading AI data...")
        ai_loaded = comparator.load_ai_extractor_data(ai_path)
        print(f"✅ AI data loaded: {ai_loaded.shape if ai_loaded is not None else 'None'}")
        
        print("📥 Loading comparison data...")
        comp_loaded = comparator.load_comparison_data(comp_path)
        print(f"✅ Comparison data loaded: {comp_loaded.shape if comp_loaded is not None else 'None'}")
        
        print("🔄 Running comparison with fuzzy threshold 80...")
        results = comparator.compare_data(fuzzy_threshold=80)
        
        if results:
            print(f"✅ Results: {results}")
            matches = results.get('matches_found', 0)  # Use matches_found instead of matches
            print(f"🎯 Matches found: {matches}")
            
            if matches == 0:
                print("⚠️ Testing with lower threshold (70)...")
                results_70 = comparator.compare_data(fuzzy_threshold=70)
                matches_70 = results_70.get('matches_found', 0) if results_70 else 0
                print(f"🎯 Matches with 70% threshold: {matches_70}")
                
                if matches_70 == 0:
                    print("⚠️ Testing with very low threshold (50)...")
                    results_50 = comparator.compare_data(fuzzy_threshold=50)
                    matches_50 = results_50.get('matches_found', 0) if results_50 else 0
                    print(f"🎯 Matches with 50% threshold: {matches_50}")
            else:
                print(f"🎉 SUCCESS! Found {matches} matches with 80% threshold")
        else:
            print("❌ No results returned from comparison")
            
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        try:
            os.unlink(ai_path)
            os.unlink(comp_path)
        except:
            pass

def test_existing_files():
    """Test with existing files in the workspace"""
    print("\n🔍 Testing with existing files...")
    
    # Check for existing test files
    test_files = [
        'streamlit_test.xlsx',
        'test_transportation_export.xlsx',
        'traversa_test_fix.xlsx',
        'traversa_test_output.xlsx'
    ]
    
    for file in test_files:
        if os.path.exists(file):
            print(f"📁 Found test file: {file}")
            try:
                df = pd.read_excel(file)
                print(f"   📊 Shape: {df.shape}")
                print(f"   📊 Columns: {list(df.columns)[:5]}...")  # First 5 columns
                
                # Look for name-like columns
                name_cols = [col for col in df.columns if 'name' in str(col).lower()]
                if name_cols:
                    print(f"   📛 Name columns: {name_cols}")
                    for col in name_cols[:2]:  # First 2 name columns
                        sample_names = df[col].dropna().head(3).tolist()
                        print(f"   📝 Sample {col}: {sample_names}")
                
            except Exception as e:
                print(f"   ❌ Error reading {file}: {e}")

if __name__ == "__main__":
    print("🚀 Starting workflow debugging...")
    test_comparison()
    test_existing_files()
    print("✅ Debugging complete!")
