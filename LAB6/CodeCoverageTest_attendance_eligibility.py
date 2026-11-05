import pytest

from attendance_eligibility import (
    attendance_percent,
    exam_eligibility,
    attendance_warning,
)


# ATTENDANCE PERCENTAGE TESTS

def test_plain_percent():
    assert attendance_percent(30, 40, 0) == 75


def test_medical_leave():
    assert attendance_percent(30, 40, 5) == 87


def test_medical_leave_above_limit():
    assert attendance_percent(30, 40, 10) == 87


def test_credited_attendance_capped():
    assert attendance_percent(38, 40, 5) == 100


def test_zero_attended_classes():
    assert attendance_percent(0, 40, 0) == 0


def test_invalid_total_zero():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, 0, 0)


def test_invalid_total_negative():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, -5, 0)


def test_negative_attendance():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 40, 0)


def test_attendance_greater_than_total():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(45, 40, 0)


# EXAM ELIGIBILITY TESTS

def test_exam_eligible():
    assert exam_eligibility(80, False, True) == "eligible"


def test_fees_pending():
    assert exam_eligibility(90, True, False) == "fees pending"


def test_condonation_required():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_condonation_approved():
    assert exam_eligibility(70, True, True) == "eligible"


def test_detained():
    assert exam_eligibility(60, True, True) == "detained"


# ATTENDANCE WARNING TESTS

def test_no_warning():
    assert attendance_warning(90, 2) is None


def test_reminder():
    assert attendance_warning(80, 2) == "reminder"


def test_final_notice():
    assert attendance_warning(70, 3) == "final notice"


def test_critical_warning():
    assert attendance_warning(70, 5) == "critical"