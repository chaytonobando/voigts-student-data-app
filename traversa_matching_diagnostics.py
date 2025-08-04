#!/usr/bin/env python3
"""
🔍 Traversa Matching Diagnostics Tool
Helps diagnose why student matching rates might be low between AI data and Traversa template.
"""

import pandas as pd
import logging
from datetime import datetime
import sys
from fuzzywuzzy import fuzz
import re

class MatchingDiagnostics:
    """Diagnostic tool for analyzing student matching issues"""
    
    def __init__(self):
        self.ai_data = None
        self.traversa_data = None
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)
    
    def load_files(self, ai_file_path: str, traversa_file_path: str):
        """Load both files and analyze their structure"""
        try:
            # Load AI data
            self.ai_data = pd.read_excel(ai_file_path)
            self.logger.info(f"✅ Loaded AI data: {len(self.ai_data)} students")
            self.logger.info(f"   Columns: {list(self.ai_data.columns)}")
            
            # Load Traversa data  
            self.traversa_data = pd.read_excel(traversa_file_path)
            self.logger.info(f"✅ Loaded Traversa data: {len(self.traversa_data)} students")
            self.logger.info(f"   Columns: {list(self.traversa_data.columns)}")
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Error loading files: {e}")
            return False
    
    def analyze_name_columns(self):
        """Analyze potential name columns in both datasets"""
        self.logger.info("\n🔍 ANALYZING NAME COLUMNS")
        self.logger.info("=" * 50)
        
        # Use the enhanced detect_name_columns from the comparator
        from student_data_comparator import StudentDataComparator
        comparator = StudentDataComparator()
        
        ai_name_cols = comparator.detect_name_columns(self.ai_data)
        traversa_name_cols = comparator.detect_name_columns(self.traversa_data)
        
        self.logger.info(f"\n📋 AI potential name columns: {ai_name_cols}")
        # Show sample data from each potential name column
        for col in ai_name_cols[:3]:  # Show first 3 potential columns
            sample_values = self.ai_data[col].dropna().head(5).tolist()
            self.logger.info(f"   {col} samples: {sample_values}")
        
        self.logger.info(f"\n📋 Traversa potential name columns: {traversa_name_cols}")
        # Show sample data from each potential name column
        for col in traversa_name_cols[:3]:  # Show first 3 potential columns
            sample_values = self.traversa_data[col].dropna().head(5).tolist()
            self.logger.info(f"   {col} samples: {sample_values}")
        
        return ai_name_cols, traversa_name_cols
    
    def _detect_name_columns(self, df, dataset_name):
        """Detect columns that likely contain names"""
        name_indicators = [
            'name', 'student', 'full_name', 'firstname', 'lastname', 
            'first_name', 'last_name', 'student_name', 'pupil', 'learner'
        ]
        
        potential_columns = []
        for col in df.columns:
            col_lower = str(col).lower()
            for indicator in name_indicators:
                if indicator in col_lower:
                    potential_columns.append(col)
                    break
        
        self.logger.info(f"\n📋 {dataset_name} potential name columns: {potential_columns}")
        
        # Show sample data from each potential name column
        for col in potential_columns[:3]:  # Show first 3 potential columns
            sample_values = df[col].dropna().head(5).tolist()
            self.logger.info(f"   {col} samples: {sample_values}")
        
        return potential_columns
    
    def test_matching_with_different_thresholds(self, ai_name_cols, traversa_name_cols):
        """Test matching with different fuzzy thresholds"""
        self.logger.info("\n🎯 TESTING MATCHING THRESHOLDS")
        self.logger.info("=" * 50)
        
        thresholds = [60, 70, 80, 85, 90, 95]
        
        # For AI data, prefer 'Student Name' if available, otherwise use first detected column
        ai_col = None
        for col in ai_name_cols:
            if 'student name' in str(col).lower() and 'student name' in str(col).lower() and '*' not in str(col):
                ai_col = col
                break
        if not ai_col and ai_name_cols:
            ai_col = ai_name_cols[0]
        
        # For Traversa data, check if we have first/last name columns to combine
        traversa_col = None
        first_name_col = None
        last_name_col = None
        
        for col in traversa_name_cols:
            col_lower = str(col).lower()
            if 'first' in col_lower and 'name' in col_lower:
                first_name_col = col
            elif 'last' in col_lower and 'name' in col_lower:
                last_name_col = col
        
        if first_name_col and last_name_col:
            traversa_col = [first_name_col, last_name_col]
            self.logger.info(f"Using combined Traversa name columns: {first_name_col} + {last_name_col}")
        elif traversa_name_cols:
            traversa_col = traversa_name_cols[0]
        
        if not ai_col or not traversa_col:
            self.logger.error("❌ Cannot find name columns for matching test")
            return
        
        self.logger.info(f"Testing with AI column: '{ai_col}' vs Traversa column: '{traversa_col}'")
        
        # Get clean name lists
        ai_names = self._get_clean_names(self.ai_data, ai_col)
        traversa_names = self._get_clean_names(self.traversa_data, traversa_col)
        
        self.logger.info(f"\n📊 Name samples:")
        self.logger.info(f"   AI names (first 5): {ai_names[:5]}")
        self.logger.info(f"   Traversa names (first 5): {traversa_names[:5]}")
        
        # Test different thresholds
        for threshold in thresholds:
            matches = self._count_matches(ai_names, traversa_names, threshold)
            match_rate = (matches / len(ai_names)) * 100 if ai_names else 0
            self.logger.info(f"   Threshold {threshold}%: {matches} matches ({match_rate:.1f}% of AI students)")
            
        return ai_col, traversa_col
    
    def _get_clean_names(self, df, name_col):
        """Get clean list of names from specified column"""
        if isinstance(name_col, list) and len(name_col) >= 2:
            # Handle combined first/last name columns
            combined_names = []
            for idx, row in df.iterrows():
                first_val = str(row.get(name_col[0], '')) if pd.notna(row.get(name_col[0])) else ''
                last_val = str(row.get(name_col[1], '')) if pd.notna(row.get(name_col[1])) else ''
                
                # Combine first and last names
                combined_name = ""
                if first_val.strip() and last_val.strip():
                    combined_name = f"{first_val.strip()} {last_val.strip()}"
                elif first_val.strip():
                    combined_name = first_val.strip()
                elif last_val.strip():
                    combined_name = last_val.strip()
                
                if combined_name.strip():
                    combined_names.append(combined_name)
            return combined_names
        else:
            # Single column
            if isinstance(name_col, list):
                name_col = name_col[0]
            return [str(name).strip() for name in df[name_col].dropna() if str(name).strip()]
    
    def _normalize_name(self, name):
        """Normalize name for matching"""
        if not name:
            return ""
        
        # Convert to string and clean
        name_str = str(name).strip()
        name_str = re.sub(r'\s+', ' ', name_str)
        name_str = name_str.title()
        
        # Remove common prefixes/suffixes
        prefixes = ['mr.', 'mrs.', 'ms.', 'dr.', 'prof.']
        suffixes = ['jr.', 'sr.', 'ii', 'iii', 'iv']
        
        words = name_str.split()
        words = [w for w in words if w.lower() not in prefixes + suffixes]
        
        return ' '.join(words)
    
    def _count_matches(self, ai_names, traversa_names, threshold):
        """Count matches at a given threshold"""
        matches = 0
        for ai_name in ai_names:
            best_score = 0
            for traversa_name in traversa_names:
                score = fuzz.ratio(ai_name.lower(), traversa_name.lower())
                if score > best_score:
                    best_score = score
            
            if best_score >= threshold:
                matches += 1
        
        return matches
    
    def analyze_specific_mismatches(self, ai_name_cols, traversa_name_cols, sample_size=10, ai_col=None, traversa_col=None):
        """Analyze specific examples of why names might not be matching"""
        self.logger.info("\n🔬 ANALYZING SPECIFIC MISMATCHES")
        self.logger.info("=" * 50)
        
        # Use passed columns or determine best columns
        if not ai_col:
            ai_col = None
            for col in ai_name_cols:
                if 'student name' in str(col).lower() and '*' not in str(col):
                    ai_col = col
                    break
            if not ai_col and ai_name_cols:
                ai_col = ai_name_cols[0]
        
        if not traversa_col:
            # Check for first/last name combination
            first_name_col = None
            last_name_col = None
            for col in traversa_name_cols:
                col_lower = str(col).lower()
                if 'first' in col_lower and 'name' in col_lower:
                    first_name_col = col
                elif 'last' in col_lower and 'name' in col_lower:
                    last_name_col = col
            
            if first_name_col and last_name_col:
                traversa_col = [first_name_col, last_name_col]
            elif traversa_name_cols:
                traversa_col = traversa_name_cols[0]
        
        if not ai_col or not traversa_col:
            return
        
        ai_names = self._get_clean_names(self.ai_data, ai_col)[:sample_size]
        traversa_names = self._get_clean_names(self.traversa_data, traversa_col)
        
        self.logger.info(f"Analyzing {len(ai_names)} AI student names against Traversa database...")
        
        for ai_name in ai_names:
            # Find best match in Traversa
            best_match = ""
            best_score = 0
            
            for traversa_name in traversa_names:
                score = fuzz.ratio(ai_name.lower(), traversa_name.lower())
                if score > best_score:
                    best_score = score
                    best_match = traversa_name
            
            status = "✅ MATCH" if best_score >= 80 else "❌ NO MATCH"
            self.logger.info(f"   {status} '{ai_name}' -> '{best_match}' (score: {best_score})")
    
    def suggest_improvements(self):
        """Suggest ways to improve matching"""
        self.logger.info("\n💡 SUGGESTIONS FOR IMPROVING MATCHING")
        self.logger.info("=" * 50)
        
        suggestions = [
            "1. 🎯 Lower the fuzzy threshold (try 70-75 instead of 80)",
            "2. 📝 Check if names are in different formats (Last, First vs First Last)",
            "3. 🔤 Verify if there are encoding issues (special characters, accents)",
            "4. 📋 Confirm you're using the correct name columns",
            "5. 🔍 Check if names include middle names/initials in one dataset but not the other",
            "6. 📊 Consider if student populations actually overlap (grade levels, time periods)",
            "7. 🧹 Clean data by removing prefixes/suffixes (Jr., Sr., etc.)",
            "8. 🔄 Try manual field mapping instead of auto-mapping"
        ]
        
        for suggestion in suggestions:
            self.logger.info(f"   {suggestion}")

def main():
    """Main diagnostic function"""
    print("🔍 Traversa Matching Diagnostics Tool")
    print("=" * 50)
    
    diagnostics = MatchingDiagnostics()
    
    # Get file paths
    ai_file = input("📁 Enter path to AI extracted data file: ").strip()
    if not ai_file:
        print("❌ AI file path required")
        return
    
    traversa_file = input("📁 Enter path to Traversa template file: ").strip()
    if not traversa_file:
        print("❌ Traversa file path required")
        return
    
    # Load and analyze
    if not diagnostics.load_files(ai_file, traversa_file):
        return
    
    # Analyze name columns
    ai_name_cols, traversa_name_cols = diagnostics.analyze_name_columns()
    
    if not ai_name_cols or not traversa_name_cols:
        print("❌ Could not detect name columns in one or both files")
        return
    
    # Test different thresholds
    diagnostics.test_matching_with_different_thresholds(ai_name_cols, traversa_name_cols)
    
    # Analyze specific mismatches
    diagnostics.analyze_specific_mismatches(ai_name_cols, traversa_name_cols)
    
    # Provide suggestions
    diagnostics.suggest_improvements()
    
    print("\n✅ Diagnostic analysis complete!")

if __name__ == "__main__":
    main()
