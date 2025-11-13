thonfrom src.parsers.job_parser import parse_jobs_page

HTML = """
<html>
  <body>
    <div class="job-card" data-jobkey="job123">
      <h2 class="job-title">Data Center Technician</h2>
      <div class="job-location">Boydton, VA</div>
      <div class="job-salary">$26.39 - $60.96 an hour</div>
      <div class="job-description">
        As a Data Center Technician, you will maintain servers and networking equipment.
      </div>
    </div>
  </body>
</html>
"""

def test_parse_jobs_page_extracts_job_data():
    records = parse_jobs_page(HTML, base_url="https://www.indeed.com/cmp/Example/jobs")
    assert len(records) == 1
    job = records[0]
    assert job["jobKey"] == "job123"
    assert job["title"] == "Data Center Technician"
    assert job["formattedSalary"] == "$26.39 - $60.96 an hour"
    assert job["location"]["city"] == "Boydton, VA"
    assert "Data Center Technician" in job["jobDescriptionText"]
    assert job["sectionType"] == "jobs"