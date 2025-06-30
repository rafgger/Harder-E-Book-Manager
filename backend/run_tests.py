#!/usr/bin/env python3
"""
Test Runner for E-Book Manager Backend

This script provides convenient access to all test files moved to the tests/ directory.
Run this from the backend directory to execute tests.
"""
import os
import sys
import subprocess

def run_test(test_name):
    """Run a specific test file"""
    test_path = os.path.join("tests", f"{test_name}.py")
    if os.path.exists(test_path):
        print(f"\n=== Running {test_name} ===")
        try:
            result = subprocess.run([sys.executable, test_path], check=True)
            print(f"✅ {test_name} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {test_name} failed with exit code {e.returncode}")
            return False
    else:
        print(f"❌ Test file {test_path} not found")
        return False

def list_available_tests():
    """List all available test files"""
    tests_dir = "tests"
    if not os.path.exists(tests_dir):
        print("❌ Tests directory not found")
        return []
    
    test_files = []
    for file in os.listdir(tests_dir):
        if file.endswith('.py') and file != '__init__.py':
            test_name = file[:-3]  # Remove .py extension
            test_files.append(test_name)
    
    return sorted(test_files)

def main():
    print("=== E-Book Manager Backend Test Runner ===")
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python run_tests.py <test_name>     # Run specific test")
        print("  python run_tests.py list           # List all available tests")
        print("  python run_tests.py all            # Run key tests")
        print("\nAvailable tests:")
        tests = list_available_tests()
        for test in tests:
            print(f"  - {test}")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        tests = list_available_tests()
        print(f"\nFound {len(tests)} test files:")
        for test in tests:
            print(f"  - {test}")
    
    elif command == "all":
        # Run the most important tests
        key_tests = [
            "test_new_fields",
            "comprehensive_test", 
            "test_auth_flow",
            "test_database",
            "diagnose_500_error"
        ]
        
        print("\n🧪 Running key backend tests...")
        passed = 0
        total = len(key_tests)
        
        for test in key_tests:
            if run_test(test):
                passed += 1
        
        print(f"\n📊 Test Results: {passed}/{total} tests passed")
        if passed == total:
            print("🎉 All key tests passed!")
        else:
            print("💥 Some tests failed. Check the output above.")
    
    else:
        # Run specific test
        test_name = command
        if not run_test(test_name):
            sys.exit(1)

if __name__ == "__main__":
    main()
