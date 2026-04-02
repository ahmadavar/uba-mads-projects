# JobRadar Autofill — Usage Guide

## Daily Workflow (20 applications in ~1 hour)

1. Open Gmail — find today's JobRadar digest
2. Open all "Apply Now" links in new tabs
3. On each job page, follow the steps below

---

## Step-by-Step Per Application

### CRITICAL ORDER — do not reverse this

1. **Upload resume first** — drag AN_Resume.pdf onto the upload area
2. **Wait 2-3 seconds** — let the company's auto-parse finish (watch the form settle)
3. **Open console** — Cmd+Option+I
4. **Run autofill script** — Up arrow (reuses last command) → Enter
5. **Review filled fields** — check name, email, phone, LinkedIn are correct
6. **Upload resume again if needed** — some forms reset after autofill
7. **Submit**

### Why this order matters
If you run the script BEFORE uploading the resume, the company's auto-parser fires after and overwrites your clean data with its (often wrong) interpretation of the PDF. Always let the parser go first, then our script corrects anything it got wrong.

---

## First Time Setup (per Safari session)

Safari console history clears when you quit Safari. Each new session:

1. Open any job application page
2. Cmd+Option+I to open console
3. Go to: `https://raw.githubusercontent.com/ahmadavar/uba-mads-projects/master/bookmarklet.txt`
4. Select all (Cmd+A), copy (Cmd+C)
5. Paste into console → Enter
6. For every other tab after that: Up arrow → Enter

---

## Supported ATS Platforms

| Platform | Fields Filled |
|----------|--------------|
| Uber (uber.com/careers) | Name, email, phone, LinkedIn, GitHub, portfolio, experience, education, all radio buttons, EEO |
| Greenhouse (greenhouse.io) | Name, email, phone, LinkedIn, GitHub, website, EEO dropdowns |
| Lever (jobs.lever.co) | Name, email, phone, LinkedIn, GitHub |
| Ashby (ashbyhq.com) | Name, email, phone, LinkedIn |
| Workday (myworkday.com) | Name, email, phone, city, zip, country, state |
| Generic | Name, email, phone, LinkedIn, city (autocomplete fields) |

---

## Adding a New Company

When you hit "0 fields filled" on an unknown ATS:

1. Run in console:
```javascript
document.querySelectorAll('input, textarea, select').forEach(el => console.log(el.tagName + ' | name=' + el.name + ' | id=' + el.id + ' | placeholder=' + el.placeholder))
```
2. Paste output to Claude
3. Script updated and pushed in ~5 minutes
4. Get new bookmarklet.txt from GitHub

---

## Profile Data Stored in Script

- Name: Ahmad Naggayev
- Email: ahmadavar956@gmail.com
- Phone: (415) 812-1535
- Location: Berkeley, CA 94710
- LinkedIn: linkedin.com/in/ahmadnaggayev
- GitHub: github.com/ahmadavar
- Website: loanmatchai.app
- EEO: Male, White (Not Hispanic or Latino), No disability, Not a protected veteran, No sponsorship required

---

## Cover Letter

The script reads your clipboard. Before running autofill:
- Copy the cover letter from the JobRadar email (Cmd+C)
- The script pastes it into the cover letter field automatically (where supported)
