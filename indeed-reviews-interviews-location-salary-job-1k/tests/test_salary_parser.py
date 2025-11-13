thonfrom src.parsers.salary_parser import parse_salaries_page

HTML = """
<html>
  <body>
    <section class="salary-header">
      <h1>Example salaries: How much does Example pay?</h1>
      <div class="salary-last-updated">October 13, 2025</div>
      <div class="salary-count">28615 salaries</div>
    </section>
    <div class="salary-category">
      <h3 class="salary-category-title">Popular Roles</h3>
      <div class="salary-row">
        <span class="salary-role-title">Software Engineer</span>
        <span class="salary-role-value">$141,020</span>
        <span class="salary-role-count">653 salaries reported</span>
      </div>
    </div>
    <div class="salary-card">
      <div class="salary-title">Software Engineer</div>
      <div class="salary-snippet">$141,020 per year</div>
      <div class="salary-subtitle">United States</div>
    </div>
  </body>
</html>
"""

def test_parse_salaries_page_extracts_salary_data():
    records = parse_salaries_page(HTML, base_url="https://www.indeed.com/cmp/Example/salaries")
    assert len(records) == 1
    salary = records[0]
    assert salary["title"] == "Software Engineer"
    assert salary["formattedSalary"] == "$141,020 per year"
    metadata = salary["_metadata"]
    assert metadata["salaryHeader"]["totalSalaryCount"] == 28615
    categories = metadata["categorySalarySection"]["categories"]
    assert len(categories) == 1
    assert categories[0]["categoryTitle"] == "Popular Roles"
    assert categories[0]["salaries"][0]["salary"] == "$141,020"