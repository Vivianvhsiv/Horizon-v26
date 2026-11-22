# Privacy Surface Review — v25.9

## Scope
A static inspection of `app.py` and the bundled configuration. This is a preliminary privacy-surface review, not a penetration test, legal review, platform data-processing assessment, or certification.

## Findings from the code inspected
- The application gathers exploration choices (selected majors, interests, and current school subjects) and keeps them in Streamlit session state.
- The inspected `app.py` does not expose obvious form fields for names, email addresses, phone numbers, home addresses, or student IDs.
- Static pattern checks did not find obvious local file-write calls, outbound write requests, or database-client references in `app.py`.
- The app has a summary-download feature. Students should be told that downloaded summaries are saved to their own device and should avoid including identifying details in free-text reflections.

## Not established by this review
- Streamlit hosting, Railway, reverse-proxy, and infrastructure logs may process technical metadata such as IP addresses and request logs.
- This package does not inspect Railway settings, account permissions, backups, retention, third-party telemetry, dependency vulnerabilities, or actual network traffic.
- This package does not prove that no personal data is processed anywhere in the deployment.

## Before public release
1. Publish a plain-language privacy notice describing what is collected, why, where it is processed, retention, and contact route.
2. Do not collect names, contact details, student IDs, or identifiable survey responses unless there is a documented need and appropriate adult/school approval.
3. Review Streamlit/Railway logging, access controls, secrets, backups, and retention with the account owner and school.
4. Keep survey source data private; publish only aggregated, non-identifying results after disclosure-risk review.
5. Obtain parent/guardian and school approval where required before inviting minors to submit data.
