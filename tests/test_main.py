"""
Unit tests for Social-Media-Dashboard
Auto-generated test scaffold — extend with project-specific tests
"""

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import dashboard
    HAS_DASHBOARD = True
except ImportError:
    HAS_DASHBOARD = False


class TestProjectStructure:
    """Test project structure and configuration."""
    
    def test_readme_exists(self):
        """Test that README.md exists."""
        readme = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
        assert os.path.isfile(readme), "README.md should exist"
    
    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        req = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "requirements.txt")
        assert os.path.isfile(req), "requirements.txt should exist"
    
    def test_license_exists(self):
        """Test that LICENSE exists."""
        lic = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "LICENSE")
        assert os.path.isfile(lic), "LICENSE should exist"

class TestDashboard:
    """Tests for dashboard module."""
    
    def test_module_imports(self):
        """Test that the module can be imported."""
        assert HAS_DASHBOARD, "Module dashboard should be importable"
    
    def test_module_has_attributes(self):
        """Test that the module has expected attributes."""
        if HAS_DASHBOARD:
            assert hasattr(dashboard, '__name__')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
