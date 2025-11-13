# Indeed Reviews, Interviews, Salaries & Jobs Scraper

> A full-funnel Indeed company intelligence scraper that collects reviews, interviews, salaries, jobs, FAQs, and company profile data from a single configuration.
> Designed for analysts, HR teams, and data engineers who need reliable Indeed workforce insights at scale, this scraper turns scattered company pages into a clean, unified dataset.

> With support for multiple international Indeed domains and advanced controls like temporal filtering, monitoring mode, and geo-targeted proxies, it helps you keep an always-fresh view of employer reputation, compensation, and hiring activity.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Indeed | Reviews | Interviews | Location | Salary | Job | $1/1K</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project extracts structured workforce intelligence from company pages across Indeed, including company reviews, job listings, salary ranges, interview experiences, FAQs, and rich company metadata. It takes standard company URLs and converts them into analytics-ready JSON suitable for dashboards, research, or downstream machine learning.

It solves the problem of manually navigating multiple Indeed sections, inconsistent layouts, and pagination limits by automating discovery, navigation, and field mapping into a unified schema.

It is built for:

- Data analysts and HR teams running recurring employer-branding and salary benchmarking reports.
- Talent analytics and workforce intelligence platforms that need fresh Indeed data at scale.
- Agencies and consultants monitoring employer sentiment, hiring velocity, and compensation competitiveness.

### Unified Indeed Company Intelligence

- Supports company overview, reviews, jobs, salaries, interviews, FAQs, and snapshot analytics from a single configuration.
- Handles international Indeed domains (e.g., indeed.com, indeed.fr, indeed.de, indeed.ca, indeed.co.uk) with automatic localization.
- Includes monitoring mode for reviews to fetch only new reviews since the last run and avoid duplicates.
- Provides temporal filters (e.g., `targetDate`) to restrict reviews and other content to a specific date window.
- Integrates performance, proxy, and concurrency controls for stable, large-scale workloads.

## Features

| Feature | Description |
|--------|-------------|
| Multi-entity company scraping | Collects reviews, jobs, salaries, interviews, FAQs, and company details from company profile URLs and their subpaths. |
| International domain support | Works across all major Indeed domains with automatic locale detection and localized content extraction. |
| Monitoring mode for reviews | `monitoringModeForReviews` collects only new reviews that were not returned in previous runs, ideal for scheduled monitoring. |
| Temporal filtering | `targetDate` allows you to restrict review scraping up to a certain date for time-bounded analyses. |
| Intelligent URL routing | Automatically detects whether a URL is for reviews, jobs, interviews, salaries, FAQs, or the about page and routes it to the right extractor. |
| Robust pagination handling | Navigates through long paginated result sets for reviews, jobs, and salary entries while avoiding duplicates. |
| Geo-targeted proxy support | Uses residential proxies with country selection to reduce blocking and get localized results. |
| Snapshot analytics extraction | Captures 360° company profiles including historical rating trends, CEO approval, happiness metrics, and department-level benchmarks where available. |
| Performance & reliability controls | Tunable `maxConcurrency`, `minConcurrency`, and `maxRequestRetries` for stable scraping on large input sets. |
| Flexible output formats | Output is structured JSON with clear typing and field explanations, ready for conversion to CSV, Excel, or data warehouses. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-----------|------------------|
| `companyName` | Normalized company name as shown on the company profile. |
| `companyUrl` | Canonical company profile URL (e.g., `/cmp/Microsoft`). |
| `domain` | The Indeed domain from which the data was scraped (e.g., `indeed.com`, `uk.indeed.com`). |
| `sectionType` | The type of page: `reviews`, `jobs`, `salaries`, `interviews`, `faq`, `about`, or `snapshot`. |
| `aggregateRating` | Overall employer rating (e.g., 4.2) plus total review count. |
| `ratingDistribution` | Distribution of 1–5 star ratings as counts or ratios. |
| `reviewTitle` | Title of an individual employee review. |
| `reviewBody` | Full text of the employee review, including pros, cons, and narrative feedback. |
| `reviewRatingOverall` | Overall rating for that review (1–5). |
| `reviewCategoryRatings` | Category-specific ratings (e.g., management, work–life balance, culture, pay & benefits). |
| `reviewAuthorJobTitle` | Job title of the reviewer (e.g., “Team Lead”). |
| `reviewAuthorStatus` | Employment status and type (e.g., “Current employee”, “Former employee”, “Full-time”). |
| `reviewLocation` | Location associated with the review (city, region, country). |
| `reviewSubmissionDate` | Human-readable or normalized date when the review was posted. |
| `reviewHelpfulVotes` | Count of “helpful” votes received by a review. |
| `companyResponse` | Official company responses to reviews, if available. |
| `interviewQuestions.answers` | Array of interview question answers with text, job title, location, and submission date. |
| `interviewQuestionURL` | Relative URL to the full question page for interview Q&A. |
| `interviewExperienceScore` | Normalized candidate sentiment metrics for interview experience (0–1 scale). |
| `hiringDurations` | Breakdown of time-to-hire categories (e.g., “About two weeks”) with ratios. |
| `jobKey` | Unique identifier of a job posting on Indeed. |
| `title` | Job title (e.g., “Data Center Technician”). |
| `formattedSalary` | Human-readable salary range string combining currency, min, max, and frequency. |
| `compensation` | Encoded or parsed compensation object, including pay range and currency where available. |
| `location.countryCode` | ISO country code for the job location (e.g., `US`). |
| `location.city` | City for the job posting, when available (e.g., “Boydton”). |
| `location.fullAddress` | Full formatted address string for the job location. |
| `jobDescriptionHtml` | Full HTML job description from the job details page. |
| `jobDescriptionText` | Plain-text version of the job description for natural language analysis. |
| `jobTypes` | Employment types (e.g., `Full-time`, `Part-time`, `Contract`). |
| `shiftAndSchedule` | Schedule attributes (e.g., `Weekends as needed`, `Evenings as needed`, `Holidays`). |
| `benefits` | Benefits and perks attributes (e.g., `On-the-job training`, `Background check` requirement). |
| `attributes` | Normalized list of tagged attributes (skills, requirements, context) associated with the job. |
| `datePublished` | Timestamp when the job was originally published. |
| `dateOnIndeed` | Timestamp when the job was indexed or updated on Indeed. |
| `expired` | Boolean indicating whether the job posting is expired. |
| `salarySnippet` | Short salary snippet from salary listings pages, including ranges and type. |
| `salaryMetadata` | Metadata for salary pages, including last update date, counts, and category groupings. |
| `salaryCategories` | Grouped salary statistics by role categories (e.g., “Popular Roles”, “Software Development”, “Marketing”). |
| `categoryTitle` | Name of a salary category (e.g., “Popular Roles”). |
| `roleTitle` | Job title within a salary category (e.g., “Software Engineer”). |
| `roleSalary` | Salary value for a role (e.g., `$141,020` yearly). |
| `reportedSalaryCount` | Number of salary reports used to calculate the displayed salary. |
| `faqQuestions` | Frequently asked questions extracted from the company FAQ section. |
| `faqAnswers` | Official answers to FAQ items, including policy and process explanations. |
| `snapshot.ceoApprovalRating` | CEO approval rating as a percentage where available. |
| `snapshot.happinessMetrics` | Multi-category breakdown of employee happiness across up to 15 dimensions (e.g., work–life balance, compensation, culture). |
| `snapshot.ratingTrends` | Historical rating trends over a multi-year window. |
| `snapshot.jobDistributionByLocation` | Metrics showing job counts and density by geography. |
| `scrapedAt` | ISO timestamp when the record was scraped. |
| `_raw` | Optional raw payload or reference field when full source data needs to be preserved. |

---

## Example Output


    [
        {
            "sectionType": "interviews",
            "companyName": "Microsoft",
            "interviewQuestions": {
                "answers": [
                    {
                        "answerText": {
                            "languageTag": "en",
                            "text": "Describe your previous job."
                        },
                        "jobTitle": "Team Lead",
                        "location": "Lagos, Nigeria",
                        "submissionDate": "November 5, 2022"
                    }
                ],
                "interviewQuestionURL": "/cmp/Microsoft/faq/what-questions-did-they-ask-during-your-interview-at-microsoft..."
            },
            "interviewProcessStory": {
                "hiringDurations": {
                    "items": [
                        {
                            "labelText": "About two weeks",
                            "ratio": 0.23017408
                        }
                    ]
                },
                "overviewExperience": {
                    "sliders": [
                        {
                            "highestText": "Excellent",
                            "lowestText": "Poor",
                            "ratio": 0.8289624
                        }
                    ]
                }
            },
            "scrapedAt": "2025-10-26T19:12:31.461Z"
        },
        {
            "sectionType": "jobs",
            "jobKey": "8255932cdf7977a4",
            "companyName": "Microsoft",
            "title": "Critical Environment Technician",
            "formattedSalary": "$26.39 - $60.96 an hour",
            "location": {
                "countryCode": "US",
                "city": "Boydton",
                "fullAddress": "Boydton, VA"
            },
            "url": "https://www.indeed.com/rc/clk?jk=8255932cdf7977a4...",
            "descriptionText": "As a Senior Data Center Technician (DCT), you will demonstrate expertise in standard processes and procedures for preparing, installing, performing diagnostics, troubleshooting, replacing, and/or decommissioning equipment...",
            "jobTypes": [
                "Full-time"
            ],
            "shiftAndSchedule": [
                "Weekends as needed",
                "Evenings as needed",
                "Holidays"
            ],
            "attributes": [
                "Background check",
                "Data center experience",
                "Computer hardware",
                "Ability to lift 50 pounds"
            ],
            "datePublished": 1751432400000,
            "dateOnIndeed": 1751521523208,
            "expired": false
        },
        {
            "sectionType": "salaries",
            "companyName": "Microsoft",
            "title": "Data Center Technician",
            "formattedSalary": "$23.17 - $52.79 an hour",
            "subtitle": "United States",
            "jobKey": "a7f35508dc2ad979",
            "snippet": "As a Microsoft Data Center Technician (DCT), you will develop an understanding of standard processes and procedures for preparing, installing, performing…",
            "sponsored": false,
            "urgentHire": false,
            "scrapedAt": "2025-10-26T19:12:31.461Z",
            "_metadata": {
                "salaryHeader": {
                    "headerText": "Microsoft salaries: How much does Microsoft pay?",
                    "formattedLastUpdateDate": "October 13, 2025",
                    "totalSalaryCount": 28615
                },
                "salaryFooter": {
                    "footerTitleText": "How much does Microsoft in the United States pay?",
                    "salaryCount": 28615
                },
                "categorySalarySection": {
                    "categories": [
                        {
                            "categoryTitle": "Popular Roles",
                            "salaries": [
                                {
                                    "title": "Software Engineer",
                                    "salary": "$141,020",
                                    "salaryType": "YEARLY",
                                    "reportedSalaryCount": 653
                                },
                                {
                                    "title": "Senior Software Engineer",
                                    "salary": "$166,029",
                                    "salaryType": "YEARLY",
                                    "reportedSalaryCount": 474
                                }
                            ]
                        }
                    ]
                }
            }
        }
    ]

---

## Directory Structure Tree


    Indeed | Reviews | Interviews | Location | Salary | Job | $1/1K /
    ├── src/
    │   ├── main.py
    │   ├── config/
    │   │   ├── settings.example.json
    │   │   └── proxies.example.json
    │   ├── crawlers/
    │   │   ├── company_reviews_crawler.py
    │   │   ├── jobs_crawler.py
    │   │   ├── salaries_crawler.py
    │   │   ├── interviews_crawler.py
    │   │   └── faq_crawler.py
    │   ├── parsers/
    │   │   ├── company_parser.py
    │   │   ├── review_parser.py
    │   │   ├── job_parser.py
    │   │   ├── salary_parser.py
    │   │   └── interview_parser.py
    │   ├── pipelines/
    │   │   ├── storage_pipeline.py
    │   │   └── monitoring_pipeline.py
    │   └── utils/
    │       ├── http_client.py
    │       ├── pagination.py
    │       ├── date_utils.py
    │       └── logging_utils.py
    ├── data/
    │   ├── sample_input.json
    │   └── sample_output.json
    ├── tests/
    │   ├── test_review_parser.py
    │   ├── test_job_parser.py
    │   ├── test_salary_parser.py
    │   └── test_interview_parser.py
    ├── docker/
    │   └── Dockerfile
    ├── requirements.txt
    ├── pyproject.toml
    └── README.md

---

## Use Cases

- **People analytics teams** use it to centralize reviews, salaries, and interview feedback across multiple companies, so they can track employer reputation trends over time.
- **Compensation analysts** use it to extract salary ranges and category-level benchmarks, so they can compare pay bands against the market for specific locations and roles.
- **Recruitment agencies** use it to monitor job listings and interview experiences for key clients, so they can advise on candidate experience and hiring competitiveness.
- **HR and employer branding teams** use it to aggregate reviews, FAQs, and snapshot metrics, so they can identify pain points and improve culture and communication.
- **Data product teams** use it to feed normalized Indeed datasets into dashboards and ML models, so they can power workforce intelligence products with fresh, structured data.

---

## FAQs

**Q1: Which Indeed pages and domains are supported?**
This scraper supports company profile URLs and their subpages such as `/about`, `/reviews`, `/jobs`, `/interviews`, `/salaries`, and `/faq` across major Indeed country domains (for example `indeed.com`, `uk.indeed.com`, `ca.indeed.com`, `de.indeed.com`, `fr.indeed.com`). The scraper automatically detects the section type from each URL and routes it to the appropriate extractor.

**Q2: How does monitoring mode for reviews work in practice?**
When `monitoringModeForReviews` is set to `true`, the scraper operates in an incremental mode. It compares reviews discovered in the current run with previously stored reviews (by ID, URL, or timestamp) and only returns newly detected reviews. This is ideal for scheduled daily or weekly jobs where you want to track new reviews without reprocessing the entire review history.

**Q3: How can I control performance and avoid timeouts on large inputs?**
You can tune `maxConcurrency`, `minConcurrency`, and `maxRequestRetries` to match your environment and proxy resources. Higher concurrency accelerates scraping but also increases the load on your network and the target website. For large lists of company URLs, start with moderate concurrency (e.g., 5–10), enable retries, and use residential proxies for stability, then scale up gradually.

**Q4: Do I need proxies, and which type should I use?**
While the scraper can work without proxies on small workloads, using rotating residential proxies significantly improves reliability, especially for cross-country scraping or continuous monitoring. You can configure proxy groups and a preferred country (e.g., `FR`, `US`) to localize content and reduce the chance of being blocked.

---

## Performance Benchmarks and Results

- **Primary Metric – Throughput:** On a typical configuration with `maxConcurrency: 5` and residential proxies, the scraper can process 80–150 company sections (e.g., reviews, jobs, salaries pages) per hour while preserving high success rates.
- **Reliability Metric – Success Rate:** With retries enabled (`maxRequestRetries: 8`) and robust pagination logic, successful page-resolution rates of 95–99% are realistic for stable proxy pools.
- **Efficiency Metric – Resource Usage:** The crawler batches requests, de-duplicates URLs, and reuses HTTP sessions, keeping memory usage moderate and allowing long-running jobs without excessive overhead.
- **Quality Metric – Data Completeness:** For companies with extensive public data, the scraper typically captures >90% of exposed reviews, job listings, and salary entries per run, along with rich metadata (attributes, schedules, rating distributions, and salary categories) suitable for advanced analytics.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
