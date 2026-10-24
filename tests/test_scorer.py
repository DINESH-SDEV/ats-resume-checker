
from app.scorer import score_resume


def test_perfect_match():
    result = score_resume("Python SQL", "Python SQL")
    assert result["score"] == 100


def test_missing_keyword():
    result = score_resume("Python SQL", "Python SQL Java")
    assert result["score"] < 100
    assert "java" in result["missing_keywords"]


def test_empty_job_description():
    result = score_resume("Python SQL", "")
    assert result["score"] == 0


def test_no_match():
    result = score_resume("HTML CSS", "Python Java")
    assert result["score"] == 0


def test_synonym_match():
    result = score_resume("I know JS", "JavaScript")
    assert result["score"] == 100
