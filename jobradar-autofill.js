(function () {
  const profile = {
    firstName: "Ahmad",
    lastName: "Naggayev",
    fullName: "Ahmad Naggayev",
    email: "ahmadavar956@gmail.com",
    phone: "(415) 812-1535",
    city: "Berkeley",
    state: "CA",
    stateAbbr: "California",
    zip: "94710",
    country: "United States",
    linkedin: "https://linkedin.com/in/ahmadnaggayev",
    github: "https://github.com/ahmadavar",
    website: "https://www.loanmatchai.app",
    // EEO
    veteran: "I am not a protected veteran",
    disability: "No, I don't have a disability",
    gender: "Male",
    ethnicity: "White (Not Hispanic or Latino)",
    authorized: "Yes",
    sponsorship: "No",
  };

  let filled = 0;

  // ── Helpers ──────────────────────────────────────────────
  function fill(el, value) {
    if (!el || el.value === value) return;
    try {
      const setter = Object.getOwnPropertyDescriptor(
        el.tagName === "TEXTAREA"
          ? window.HTMLTextAreaElement.prototype
          : window.HTMLInputElement.prototype,
        "value"
      ).set;
      setter.call(el, value);
      el.dispatchEvent(new Event("input", { bubbles: true }));
      el.dispatchEvent(new Event("change", { bubbles: true }));
      el.dispatchEvent(new Event("blur", { bubbles: true }));
      filled++;
    } catch (e) {}
  }

  function selectOption(el, value) {
    if (!el) return;
    const option = Array.from(el.options).find(
      (o) => o.text.toLowerCase().includes(value.toLowerCase()) ||
             o.value.toLowerCase().includes(value.toLowerCase())
    );
    if (option) {
      el.value = option.value;
      el.dispatchEvent(new Event("change", { bubbles: true }));
      filled++;
    }
  }

  function tryFill(selectors, value) {
    for (const sel of selectors) {
      try {
        const el = document.querySelector(sel);
        if (el) { fill(el, value); return; }
      } catch (e) {}
    }
  }

  function pasteFromClipboard(selectors) {
    navigator.clipboard.readText().then((text) => {
      if (!text) return;
      for (const sel of selectors) {
        try {
          const el = document.querySelector(sel);
          if (el) { fill(el, text); return; }
        } catch (e) {}
      }
    }).catch(() => {});
  }

  // ── Detect ATS ───────────────────────────────────────────
  const url = window.location.href;
  const isWorkday = url.includes("myworkday") || !!document.querySelector("[data-automation-id]");
  const isGreenhouse = url.includes("greenhouse.io") || !!document.querySelector("#application_form");
  const isLever = url.includes("jobs.lever.co");
  const isAshby = url.includes("ashbyhq.com");
  const isUber = url.includes("uber.com/careers");

  // ── Workday ──────────────────────────────────────────────
  if (isWorkday) {
    const wd = [
      ["legalNameSection_firstName", profile.firstName],
      ["legalNameSection_lastName", profile.lastName],
      ["email", profile.email],
      ["phone", profile.phone],
      ["addressSection_city", profile.city],
      ["addressSection_postalCode", profile.zip],
    ];
    for (const [id, val] of wd) {
      const el = document.querySelector(`[data-automation-id="${id}"] input`) ||
                 document.querySelector(`[data-automation-id="${id}"]`);
      if (el) fill(el, val);
    }
    // Workday dropdowns
    selectOption(document.querySelector('[data-automation-id="country"] select'), "United States");
    selectOption(document.querySelector('[data-automation-id="state"] select'), "California");
    // Cover letter from clipboard
    pasteFromClipboard(['[data-automation-id="coverLetter"] textarea', 'textarea[data-automation-id*="cover"]']);
  }

  // ── Greenhouse ───────────────────────────────────────────
  if (isGreenhouse) {
    fill(document.querySelector("#first_name"), profile.firstName);
    fill(document.querySelector("#last_name"), profile.lastName);
    fill(document.querySelector("#email"), profile.email);
    fill(document.querySelector("#phone"), profile.phone);
    tryFill(['input[name*="linkedin"]', 'input[placeholder*="LinkedIn"]', 'input[id*="linkedin"]'], profile.linkedin);
    tryFill(['input[name*="github"]', 'input[placeholder*="GitHub"]'], profile.github);
    tryFill(['input[name*="website"]', 'input[placeholder*="Website"]', 'input[placeholder*="Portfolio"]'], profile.website);
    pasteFromClipboard(["#cover_letter", 'textarea[name*="cover"]']);
    // EEO
    selectOption(document.querySelector('select[name*="gender"]'), "Male");
    selectOption(document.querySelector('select[name*="veteran"]'), "not a protected");
    selectOption(document.querySelector('select[name*="disability"]'), "No");
    selectOption(document.querySelector('select[name*="race"], select[name*="ethnicity"]'), "White");
  }

  // ── Lever ────────────────────────────────────────────────
  if (isLever) {
    fill(document.querySelector('input[name="name"]'), profile.fullName);
    fill(document.querySelector('input[name="email"]'), profile.email);
    fill(document.querySelector('input[name="phone"]'), profile.phone);
    tryFill(['input[name*="linkedin"]', 'input[placeholder*="LinkedIn"]'], profile.linkedin);
    tryFill(['input[name*="github"]', 'input[placeholder*="GitHub"]'], profile.github);
    pasteFromClipboard(['textarea[name="comments"]', 'textarea[name*="cover"]']);
  }

  // ── Ashby ────────────────────────────────────────────────
  if (isAshby) {
    tryFill(['input[name="firstName"]', 'input[placeholder*="First"]'], profile.firstName);
    tryFill(['input[name="lastName"]', 'input[placeholder*="Last"]'], profile.lastName);
    fill(document.querySelector('input[name="email"], input[type="email"]'), profile.email);
    fill(document.querySelector('input[name="phone"]'), profile.phone);
    tryFill(['input[name*="linkedin"]', 'input[placeholder*="LinkedIn"]'], profile.linkedin);
    pasteFromClipboard(['textarea[name*="cover"]', 'textarea[placeholder*="cover"]']);
  }

  // ── Uber ─────────────────────────────────────────────────
  if (isUber) {
    fill(document.querySelector('input[name="firstName"]'), profile.firstName);
    fill(document.querySelector('input[name="lastName"]'), profile.lastName);
    fill(document.querySelector('input[name="email"]'), profile.email);
    fill(document.querySelector('input[name="mobileNumber"]'), profile.phone);
    fill(document.querySelector('input[name="linkedInURL"]'), profile.linkedin);
    fill(document.querySelector('input[name="githubURL"]'), profile.github);
    fill(document.querySelector('input[name="otherURL"]'), profile.website);
    // Work authorization: legalRightToWork = Yes
    const authYes = document.querySelector('input[name="legalRightToWork"][value="true"], input[name="legalRightToWork"]');
    if (authYes) { authYes.click(); filled++; }
    // Visa sponsorship: requireVisaSponsorship = No
    const visaNo = document.querySelector('input[name="requireVisaSponsorship"][value="false"]');
    if (visaNo) { visaNo.click(); filled++; }
    // EEO — gender: Male
    const genderMale = Array.from(document.querySelectorAll('input[name="gender"]')).find(el => el.value === "male" || el.value === "Male" || el.value === "1");
    if (genderMale) { genderMale.click(); filled++; }
    // EEO — race: White
    const raceWhite = Array.from(document.querySelectorAll('input[name="race"]')).find(el => el.value.toLowerCase().includes("white"));
    if (raceWhite) { raceWhite.click(); filled++; }
    // EEO — disability: No
    const disabilityNo = Array.from(document.querySelectorAll('input[name="disability"]')).find(el => el.value === "2" || el.value.toLowerCase().includes("no") || el.value.toLowerCase().includes("don"));
    if (disabilityNo) { disabilityNo.click(); filled++; }
    // EEO — veteran: not protected
    const vetNo = Array.from(document.querySelectorAll('input[name="veteran"]')).find(el => el.value.toLowerCase().includes("not") || el.value === "4");
    if (vetNo) { vetNo.click(); filled++; }
    // inUSA: Yes
    const inUSA = document.querySelector('input[name="inUSA"][value="true"], input[name="inUSA"]');
    if (inUSA) { inUSA.click(); filled++; }
  }

  // ── Generic fallback (any ATS) ───────────────────────────
  const generic = [
    [['input[autocomplete="given-name"]', 'input[name="first_name"]', 'input[id="first_name"]'], profile.firstName],
    [['input[autocomplete="family-name"]', 'input[name="last_name"]', 'input[id="last_name"]'], profile.lastName],
    [['input[autocomplete="email"]', 'input[type="email"]'], profile.email],
    [['input[autocomplete="tel"]', 'input[name="phone"]', 'input[id="phone"]'], profile.phone],
    [['input[name*="linkedin"]', 'input[placeholder*="LinkedIn"]'], profile.linkedin],
    [['input[name*="city"]', 'input[placeholder*="City"]'], profile.city],
  ];

  for (const [selectors, value] of generic) {
    for (const sel of selectors) {
      try {
        const el = document.querySelector(sel);
        if (el && !el.value) { fill(el, value); break; }
      } catch (e) {}
    }
  }

  // ── Done ─────────────────────────────────────────────────
  const ats = isWorkday ? "Workday" : isGreenhouse ? "Greenhouse" : isLever ? "Lever" : isAshby ? "Ashby" : isUber ? "Uber" : "Generic";
  alert(`✅ JobRadar filled ${filled} fields on ${ats}.\n\n📋 Cover letter: copied from your clipboard.\nMake sure you copied it from your email first!\n\n📎 Resume: upload manually (browser security restriction).`);
})();
