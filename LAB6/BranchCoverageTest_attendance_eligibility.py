import pytest

from attendance_eligibility import (
    attendance_percent,
    exam_eligibility,
    attendance_warning,
)


# ATTENDANCE PERCENTAGE - BRANCH TESTS

def test_total_classes_invalid_zero():
    with pytest.raises(ValueError):
        attendance_percent(10, 0, 0)


def test_total_classes_invalid_negative():
    with pytest.raises(ValueError):
        attendance_percent(10, -1, 0)


def test_attendance_below_zero():
    with pytest.raises(ValueError):
        attendance_percent(-1, 40, 0)


def test_attendance_above_total():
    with pytest.raises(ValueError):
        attendance_percent(41, 40, 0)


def test_attendance_valid_boundary():
    assert attendance_percent(40, 40, 0) == 100


def test_medical_leave_above_five():
    assert attendance_percent(30, 40, 6) == 87


def test_medical_leave_at_five():
    assert attendance_percent(30, 40, 5) == 87


def test_credited_attendance_above_total():
    assert attendance_percent(39, 40, 5) == 100


def test_credited_attendance_not_above_total():
    assert attendance_percent(30, 40, 0) == 75


# EXAM ELIGIBILITY - BRANCH TESTS

def test_fees_not_paid():
    assert exam_eligibility(90, True, False) == "fees pending"


def test_fees_paid():
    assert exam_eligibility(90, True, True) == "eligible"


def test_exactly_75_percent():
    assert exam_eligibility(75, False, True) == "eligible"


def test_above_75_percent():
    assert exam_eligibility(80, False, True) == "eligible"


def test_between_65_and_75_with_condonation():
    assert exam_eligibility(70, True, True) == "eligible"


def test_between_65_and_75_without_condonation():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_exactly_65_without_condonation():
    assert exam_eligibility(65, False, True) == "condonation required"


def test_below_65():
    assert exam_eligibility(64, True, True) == "detained"


# ATTENDANCE WARNING - BRANCH TESTS

def test_warning_at_85():
    assert attendance_warning(85, 2) is None


def test_warning_above_85():
    assert attendance_warning(90, 2) is None


def test_warning_below_85():
    assert attendance_warning(84, 2) == "reminder"


def test_warning_at_75():
    assert attendance_warning(75, 2) == "reminder"


def test_warning_below_75():
    assert attendance_warning(74, 5) == "critical"


def test_critical_when_more_than_four_weeks():
    assert attendance_warning(70, 5) == "critical"


def test_final_notice_at_four_weeks():
    assert attendance_warning(70, 4) == "final notice"


def test_final_notice_below_four_weeks():
    assert attendance_warning(70, 2) == "final notice"