thonfrom src.parsers.interview_parser import parse_interviews_page

HTML = """
<html>
  <body>
    <div class="interview-question">
      <a href="/cmp/Example/faq/interview-question-1">View details</a>
      <div class="interview-answer">
        <p class="answer-text">Describe your previous job.</p>
        <span class="answer-job-title">Team Lead</span>
        <span class="answer-location">Lagos, Nigeria</span>
        <span class="answer-date">November 5, 2022</span>
      </div>
    </div>
  </body>
</html>
"""

def test_parse_interviews_page_extracts_answers():
    records = parse_interviews_page(HTML, base_url="https://www.indeed.com/cmp/Example/interviews")
    assert len(records) == 1
    record = records[0]
    answers = record["interviewQuestions"]["answers"]
    assert len(answers) == 1
    answer = answers[0]
    assert answer["answerText"]["text"] == "Describe your previous job."
    assert answer["jobTitle"] == "Team Lead"
    assert answer["location"] == "Lagos, Nigeria"
    assert answer["submissionDate"] == "November 5, 2022"
    assert record["sectionType"] == "interviews"

indeed-reviews-interviews-location-salary-job-1k/docker/Dockerfile
dockerfileFROM python:3.11-slim

WORKDIR /app