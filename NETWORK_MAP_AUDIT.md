# Network Map interest-mapping audit

Date: 2026-11-24
Scope: all 20 major profiles in `majors.json`, the corresponding records in `academic_sources.json`, and `emasi_mapping_protocol.json`.

## Audit rule

The mapping protocol requires a specific, source-backed relationship and states: “No evidence, no confirmed connection.” It also requires institution/programme-specific evidence and prohibits promoting pending relationships into the interactive network.

A major profile's `interests` array is a taxonomy/tag list. It does not contain a claim-level source, institution, programme, explanation, or verification status for each interest-to-major pair. The shared tags therefore cannot establish that a student's selected interest is academically connected to a particular major.

The current EMASI subject guidance is explicitly exploratory. No populated, verified EMASI subject-to-major connection records were found in the audited profiles. Programme-availability records and general disciplinary claims are not treated as evidence for a specific interest match or an EMASI subject connection.

## Profile-by-profile result

| Major | Existing interest tags | Audit result | Network behavior |
|---|---|---|---|
| Cognitive Science | Psychology; Technology; Human behavior; Research; Cognitive processes; Brain and neuroscience; Mental processes and learning; Education and learning; Language and communication; Decision making; Research and analysis | Shared taxonomy tags; no claim-level evidence per interest | Tag matches disabled |
| Psychology | Psychology; Human behavior; Social science; Helping others; Research; Cognitive processes; Brain and neuroscience; Mental processes and learning; Education and learning; Sports and human movement; Health and human biology; Decision making; Research and analysis | Shared taxonomy tags; no claim-level evidence per interest | Tag matches disabled |
| Computer Science | Technology; Problem solving; Innovation; Mathematics; Artificial intelligence; Coding and software; Robotics and automation; Data and patterns; Engineering and invention | Shared taxonomy tags; no claim-level evidence per interest | Tag matches disabled |
| Data Science | Technology; Mathematics; Research; Problem solving; Data and patterns; Climate and geography; Maps and places; Scientific research; Research and analysis; Decision making | Shared taxonomy tags; broad geographic tags are not sufficient evidence | Tag matches disabled |
| Economics | Business; Society; Mathematics; Policy; Politics and public policy; Economics and markets; Business and entrepreneurship; Finance and investment; Leadership and management; Social issues; Culture and society; Climate and geography; Cities and urban spaces | Shared taxonomy tags; broad societal/geographic tags are not sufficient evidence | Tag matches disabled |
| Biology | Life sciences; Environment; Health; Research; Nature and wildlife; Environment and sustainability; Climate and geography; Animals and living systems; Health and human biology; Experiments and discovery | Shared taxonomy tags; no claim-level evidence per interest | Tag matches disabled |
| Mechanical Engineering | Technology; Design; Problem solving; Innovation; Robotics and automation; Engineering and invention; Product design; Architecture and buildings | Shared taxonomy tags; no claim-level evidence per interest | Tag matches disabled |
| Finance | Business; Mathematics; Decision making; Economics and markets; Business and entrepreneurship; Finance and investment; Leadership and management; Data and patterns | Shared taxonomy tags; no claim-level evidence per interest | Tag matches disabled |
| Chemistry | No interest tags | No interest mapping to audit | No inferred match |
| Physics | No interest tags | No interest mapping to audit | No inferred match |
| Environmental Science | No interest tags | No interest mapping to audit | No inferred match |
| Architecture | No interest tags | No interest mapping to audit | No inferred match |
| Electrical Engineering | No interest tags | No interest mapping to audit | No inferred match |
| Civil Engineering | No interest tags | No interest mapping to audit | No inferred match |
| Political Science | No interest tags | No interest mapping to audit | No inferred match |
| Sociology | No interest tags | No interest mapping to audit | No inferred match |
| Linguistics | No interest tags | No interest mapping to audit | No inferred match |
| Education | No interest tags | No interest mapping to audit | No inferred match |
| Accounting | No interest tags | No interest mapping to audit | No inferred match |
| Communication & Media Studies | No interest tags | No interest mapping to audit | No inferred match |

## Implemented safeguards

- The Network Map no longer creates major matches from shared interest tags.
- It no longer creates major matches from exploratory EMASI subject guidance.
- It shows selected interests and current subjects as separate student inputs.
- It shows a major only when the student explicitly selects that major; the UI labels it as the student's stated intention, not a recommendation or suitability assessment.
- Unrelated majors are not inserted into the student's personalized map.
- Existing source records and major profile content are preserved; this change does not delete the broader Explore Majors content.
- The standalone Reflection page and navigation item are removed. The homepage workflow now has four steps.

## Evidence required to restore a connection

A future interest-to-major edge must have a claim-level record with the exact interest, named major, relationship type, explanation, institution/programme scope, source URL, source section/page, verification status, and review date. An EMASI subject edge must additionally identify the relevant EMASI learning outcome/topic and the corresponding university course, programme outcome, or explicitly documented prerequisite. Until then, the edge remains absent from the personalized network.
