thonfrom src.parsers.review_parser import parse_reviews_page

HTML = """
<html>
  <body>
    <div class="review">
      <h2 class="review-title">Great culture and team</h2>
      <div class="review-body">
        I enjoyed working here. The team was supportive and the benefits were solid.
      </div>
      <span class="review-rating">4.0 out of 5</span>
      <span class="review-author-title">Software Engineer</span>
      <span class="review-author-status">Current employee</span>
      <span class="review-location">Remote</span>
      <span class="review-date">January 10, 2025</span>
    </div>
  </body>
</html>
"""

def test_parse_reviews_page_extracts_basic_fields():
    records = parse_reviews_page(HTML, base_url="https://www.indeed.com/cmp/Example/reviews")
    assert len(records) == 1
    review = records[0]
    assert review["reviewTitle"] == "Great culture and team"
    assert "enjoyed working here" in review["reviewBody"]
    assert review["reviewRatingOverall"] == 4.0
    assert review["reviewAuthorJobTitle"] == "Software Engineer"
    assert review["reviewAuthorStatus"] == "Current employee"
    assert review["reviewLocation"] == "Remote"
    assert review["reviewSubmissionDate"] == "January 10, 2025"
    assert review["sectionType"] == "reviews"