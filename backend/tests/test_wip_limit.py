import pytest
from app.services.wip import can_move_to_in_progress


class TestWIPLimit:
    """Test WIP limit enforcement logic"""
    
    def test_allow_when_count_less_than_limit(self):
        """Should allow moving to in-progress when count < limit"""
        # Arrange
        in_progress_count = 0
        wip_limit = 1
        
        # Act
        result = can_move_to_in_progress(in_progress_count, wip_limit)
        
        # Assert
        assert result is True, "Should allow when count (0) < limit (1)"
    
    def test_allow_when_count_just_below_limit(self):
        """Should allow moving to in-progress when count is just below limit"""
        # Arrange
        in_progress_count = 2
        wip_limit = 3
        
        # Act
        result = can_move_to_in_progress(in_progress_count, wip_limit)
        
        # Assert
        assert result is True, "Should allow when count (2) < limit (3)"
    
    def test_block_when_count_equals_limit(self):
        """Should block moving to in-progress when count == limit"""
        # Arrange
        in_progress_count = 1
        wip_limit = 1
        
        # Act
        result = can_move_to_in_progress(in_progress_count, wip_limit)
        
        # Assert
        assert result is False, "Should block when count (1) == limit (1)"
    
    def test_block_when_count_exceeds_limit(self):
        """Should block moving to in-progress when count > limit"""
        # Arrange
        in_progress_count = 3
        wip_limit = 2
        
        # Act
        result = can_move_to_in_progress(in_progress_count, wip_limit)
        
        # Assert
        assert result is False, "Should block when count (3) > limit (2)"
    
    def test_block_when_limit_is_zero(self):
        """Should block everything when limit is 0"""
        # Arrange
        in_progress_count = 0
        wip_limit = 0
        
        # Act
        result = can_move_to_in_progress(in_progress_count, wip_limit)
        
        # Assert
        assert result is False, "Should block when limit is 0"
    
    def test_block_when_limit_is_zero_and_count_positive(self):
        """Should block when limit is 0 regardless of count"""
        # Arrange
        in_progress_count = 5
        wip_limit = 0
        
        # Act
        result = can_move_to_in_progress(in_progress_count, wip_limit)
        
        # Assert
        assert result is False, "Should block when limit is 0, even with positive count"

