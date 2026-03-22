# Affirmative Defenses - Reference Guide

**Version**: 1.0.0
**Last Updated**: 2026-01-01
**Maintained By**: MISJustice Alliance Legal Team

---

## Purpose

This reference provides comprehensive analysis of affirmative defenses commonly asserted in civil rights and tort litigation. Understanding these defenses is critical for:
- Case assessment and viability analysis
- Discovery planning
- Motion practice strategy
- Trial preparation

---

## Qualified Immunity (§ 1983 Individual Defendants)

### Overview

**Most Important Defense** in § 1983 litigation against individual officers

**Purpose**: Shields government officials from civil liability unless they violated "clearly established" constitutional rights

**Policy Rationale**:
- Protect officials making split-second decisions
- Avoid overdeterrence of vigorous enforcement
- Reduce frivolous litigation

**Criticism**: Effectively impossible to overcome in many cases (see "Qualified Immunity Problem")

---

### Two-Prong Test

#### Prong 1: Constitutional Violation?

**Question**: Taking facts in light most favorable to plaintiff, did defendant violate constitutional right?

**Analysis**: Standard constitutional analysis (Fourth Amendment, etc.)

**Court May Skip**: Court may skip to Prong 2 even if violation found (*Pearson v. Callahan*, 555 U.S. 223 (2009))

---

#### Prong 2: Clearly Established Right?

**Standard**: Was right "sufficiently clear that every reasonable official would have understood that what he is doing violates that right" (*Mullenix v. Luna*, 577 U.S. 7 (2015))

**Critical Question**: Was there controlling case law with materially similar facts?

---

### "Clearly Established" Analysis

#### High Specificity Requirement

**General Principles Insufficient**: Broad constitutional statements don't clearly establish rights

**Examples - NOT Clearly Established**:
- ❌ "Excessive force violates Fourth Amendment" (too general)
- ❌ "Shooting unarmed person may be excessive" (too general)

**Examples - Clearly Established**:
- ✅ *Tennessee v. Garner* (1985): Cannot shoot **fleeing**, **unarmed**, **non-dangerous** suspect
- ✅ Circuit precedent with nearly identical facts

**Troubling Trend**: Courts demand ever-more specific precedent
- "Was there a case involving three taser applications?"
- "Was suspect wearing a red shirt or blue shirt?"
- Extreme specificity denies QI protection

---

#### Sources of Clearly Established Law

**Hierarchy**:
1. **Supreme Court precedent** (strongest)
2. **Controlling circuit precedent** (Court of Appeals for your circuit)
3. **Weight of authority** from other circuits (weaker)
4. **District court cases** (not binding, but persuasive)

**Circuit Split**: If circuits split, right likely NOT clearly established

**Temporal Requirement**: Precedent must exist at time of violation

---

#### "Obvious Case" Exception

**Rule**: Right can be clearly established even without prior case if violation is obvious

**Standard**: Constitutional violation so obvious that cited case law unnecessary

**In Practice**: Rarely succeeds
- Courts say it applies in theory
- But almost never find it satisfied

**Example - Potential Obvious Case**:
```
Officer shoots handcuffed suspect lying on ground, posing no threat

Analysis:
  - No need for specific precedent
  - Obviously excessive force
  - "Every reasonable officer" would know this violates Fourth Amendment

Likely Result: Still denied (courts find ways to grant QI)
```

---

### Overcoming Qualified Immunity

#### Strategy 1: Find Circuit Precedent

**Goal**: Locate case in your circuit with materially similar facts

**Resources**:
- Circuit case law databases (Westlaw, Lexis)
- Civil rights practice guides
- Prior briefs in similar cases

**Example**:
```
Your Case: Officer tased handcuffed suspect
Circuit Precedent: Smith v. City (9th Cir. 2018) - taser on handcuffed suspect = excessive force
Result: Qualified immunity DENIED (clearly established)
```

---

#### Strategy 2: Argue "Obvious Case"

**Approach**: Even without specific precedent, violation was so clear that no reasonable officer could believe lawful

**Supporting Arguments**:
- Officer's training clearly prohibited conduct
- Department policy explicitly forbade action
- Common sense dictates unreasonableness

**Likelihood**: Low success rate, but worth asserting

---

#### Strategy 3: Factual Disputes Preclude Summary Judgment

**Key Principle**: Qualified immunity is legal question, but based on facts

**Strategy**: Create genuine disputes of material fact
- Officer says suspect lunged; plaintiff says compliant
- Dispute precludes summary judgment on QI
- Case survives to trial or settlement

**Discovery Focus**:
- Video evidence (bodycam, surveillance)
- Witness testimony
- Physical evidence contradicting officer's account

---

#### Strategy 4: Sue Municipality (No Qualified Immunity)

**Monell Liability**: Municipalities have NO qualified immunity

**Elements**:
1. Constitutional violation (by employee)
2. Municipal policy/custom caused violation
3. Deliberate indifference

**Advantage**: Avoids qualified immunity entirely

**Disadvantage**: Higher burden of proof (must show policy/custom)

---

### The Qualified Immunity Problem

#### Catch-22 Paradox

**Problem**:
1. To overcome QI, need prior case with materially similar facts
2. But if prior case dismissed on QI (no similar precedent), no precedent created
3. Next case also dismissed (still no precedent)
4. Rights never become "clearly established"

**Result**: Impossible to establish new rights

---

#### Reform Proposals

**Legislative**:
- **Ending Qualified Immunity Act** (proposed federal legislation)
- State-level reforms (Colorado, New Mexico, Connecticut)

**Judicial**:
- Justice Sotomayor's dissents calling for reconsideration
- Academic criticism from across political spectrum

**Practical Impact**: Until reformed, QI remains major obstacle

---

## Governmental Immunity

### Federal Level: Federal Tort Claims Act (FTCA)

#### Sovereign Immunity Waiver

**General Rule**: United States has sovereign immunity (cannot be sued)

**FTCA Waiver**: 28 U.S.C. §§ 2671-2680 waives immunity for certain torts

**Scope**: Federal employees acting within scope of employment

---

#### Key FTCA Exceptions (Immunity NOT Waived)

**1. Discretionary Function Exception** (28 U.S.C. § 2680(a))
- **Rule**: No liability for discretionary acts (policy decisions)
- **Test** (*Berkovitz v. United States*, 486 U.S. 531 (1988)):
  1. Does statute/regulation mandate specific conduct? (If yes, not discretionary)
  2. Does judgment involve policy considerations? (If yes, discretionary)
- **Examples**:
  - ✅ Immune: Decision to deploy troops
  - ❌ Not Immune: Negligent driving by postal worker

**2. Law Enforcement Exception** (28 U.S.C. § 2680(h))
- **Rule**: No liability for claims arising from:
  - Assault, battery, false imprisonment, false arrest, abuse of process, malicious prosecution
  - **BY LAW ENFORCEMENT OFFICER**
- **Effect**: Bars most claims against federal law enforcement (FBI, DEA, etc.)

**3. Intentional Tort Exception** (28 U.S.C. § 2680(h))
- **Rule**: No liability for intentional torts (with exceptions)
- **Exception to Exception**: Assault, battery, false imprisonment, false arrest, abuse of process, malicious prosecution by law enforcement (see above)

---

#### FTCA Procedural Requirements

**Administrative Exhaustion**:
1. File SF-95 claim with federal agency
2. Wait 6 months for decision (or denial)
3. Then may file lawsuit

**Exclusive Remedy**: FTCA is exclusive remedy (bars § 1983 against federal officials)

**No Jury Trial**: FTCA cases tried to judge only

---

### Bivens Actions (Federal Officers)

**Alternative to FTCA**: Constitutional tort claims against federal officers (*Bivens v. Six Unknown Named Agents*, 403 U.S. 388 (1971))

**Scope**: Very narrow, limited to:
1. Fourth Amendment unreasonable search/seizure
2. Fifth Amendment due process
3. Eighth Amendment cruel and unusual punishment

**Modern Trend**: Supreme Court has refused to expand Bivens (*Ziglar v. Abbasi*, 137 S. Ct. 1843 (2017))

**Qualified Immunity**: Federal officers entitled to QI in Bivens actions

---

### State Level: Sovereign Immunity

#### Eleventh Amendment

**Rule**: States immune from private damages suits in federal court

**Exceptions**:
1. **Prospective injunctive relief** (*Ex parte Young*)
   - Can sue state official for injunction
   - Cannot sue for retroactive monetary relief
2. **State waiver**: Express consent to suit
3. **Congressional abrogation**: Valid exercise of Section 5 power (14th Amendment)

**ADA Abrogation**:
- Title II: Partial (access to courts) (*Tennessee v. Lane*)
- Title I: NO (*Board of Trustees v. Garrett*)

---

#### State Tort Claims Acts

**Waiver of Sovereign Immunity**: Most states have enacted tort claims acts waiving immunity with limitations

**Common Features**:
1. **Notice Requirements**: File claim with state within 30-180 days
2. **Damage Caps**: $250K-$1M typical
3. **Discretionary Function Exception**: Similar to federal FTCA
4. **Intentional Tort Exceptions**: Many states retain immunity for intentional torts

**State Variations**: Check specific state statute

---

### Municipal Immunity

#### No Qualified Immunity

**Key Point**: **Municipalities do NOT receive qualified immunity** (*Owen v. City of Independence*, 445 U.S. 622 (1980))

**Rationale**: Municipality not "person" entitled to good faith defense

**Impact**: If Monell liability proven, municipality liable (no QI shield)

---

#### Discretionary vs. Ministerial Acts

**Many States Distinguish**:
- **Discretionary Acts**: Policy decisions (immune)
- **Ministerial Acts**: Routine implementation (not immune)

**Examples**:
- **Discretionary (Immune)**: Decision on number of police officers to hire
- **Ministerial (Not Immune)**: Negligent driving by police officer

---

## Absolute Immunity

### Prosecutors

#### Absolute Immunity for Advocacy (*Imbler v. Pachtman*, 424 U.S. 409 (1976))

**Rule**: Prosecutors absolutely immune for acts "intimately associated with judicial phase of criminal process"

**Protected Activities**:
- Initiating prosecution
- Presenting case at trial
- Making legal arguments
- Examining witnesses

**Not Protected** (Qualified Immunity Only):
- Investigative functions
- Administrative acts
- Advice to police

---

#### Brady Violations

**Problem**: Prosecutors have absolute immunity for withholding exculpatory evidence (*Brady v. Maryland*)

**Result**: Even deliberate suppression often unremedied in civil suit

**Limited Remedy**: Criminal conviction reversal, but no § 1983 damages

---

### Judges

#### Absolute Immunity for Judicial Acts (*Stump v. Sparkman*, 435 U.S. 349 (1978))

**Rule**: Judges absolutely immune for acts performed in judicial capacity

**Test**:
1. Did judge act in judicial capacity?
2. Did judge have subject matter jurisdiction?

**Protected Even If**:
- Act was error
- Act was malicious
- Act violated law

**Examples**:
- ✅ Immune: Judge sentences defendant
- ✅ Immune: Judge holds plaintiff in contempt (even maliciously)
- ❌ Not Immune: Judge physically assaults litigant in chambers

---

#### Exception: Non-Judicial Acts

**Not Protected**:
- Administrative acts (hiring court staff)
- Ministerial acts (signing form)
- Acts in absence of jurisdiction

**Practical Reality**: Extremely difficult to sue judges

---

### Witnesses

**Absolute Immunity**: Witnesses (including police who testify) absolutely immune for testimony

**Rationale**: Encourage truthful testimony without fear of retaliation

**Scope**: Covers perjury (even deliberate false testimony)

---

### Legislators

**Speech or Debate Clause** (U.S. Const. art. I, § 6): Federal legislators absolutely immune for legislative acts

**State Equivalent**: Most states provide similar protection

---

## Consent

### Express Consent

**Definition**: Plaintiff explicitly agreed to conduct

**Examples**:
- Signed consent form for medical procedure
- Contractual agreement to participate in activity
- Verbal agreement to contact

**Burden**: Defendant must prove consent

**Limits**:
- Consent to one act ≠ consent to different act
- Consent obtained by fraud/duress invalid

---

### Implied Consent

**Definition**: Consent inferred from circumstances

**Examples**:
- Plaintiff's conduct implied consent (held out hand for handshake)
- Emergency medical treatment (unconscious patient)
- Custom/practice (sports, social interactions)

**Standard**: Would reasonable person believe plaintiff consented?

---

### Scope of Consent

**Limited to What Plaintiff Consented To**:
- Consent to X-ray ≠ consent to surgery
- Consent to pat-down ≠ consent to strip search

**Exceeding Scope = Battery/Trespass**

---

## Self-Defense and Defense of Others

### Self-Defense

#### Elements

1. **Reasonable Belief**: Defendant reasonably believed force necessary
2. **Imminent Harm**: Threat was imminent (not future)
3. **Proportional Force**: Force used was proportional to threat

**Objective Standard**: Would reasonable person believe force necessary?

---

#### Duty to Retreat

**Traditional Rule**: Duty to retreat before using force (if safe to do so)

**Castle Doctrine**: No duty to retreat in one's home (most states)

**Stand Your Ground**: No duty to retreat anywhere (many states)

---

#### Deadly Force

**Allowed Only If**: Reasonable belief of imminent death or serious bodily injury

**Not Allowed**: To prevent minor assault, property crime (generally)

**Police Exception**: *Tennessee v. Garner* - police may use deadly force to prevent escape of dangerous fleeing felon

---

### Defense of Others

**Elements**: Same as self-defense, but defending third party

**Relationship**: No relationship required (can defend stranger)

**Reasonable Belief**: Defendant must reasonably believe third party has right to self-defense

---

### Imperfect Self-Defense

**Some Jurisdictions Recognize**: Defendant honestly but unreasonably believed force necessary

**Effect**:
- Not complete defense
- May reduce damages
- May reduce criminal charges (murder → manslaughter)

---

## Comparative/Contributory Negligence

### Contributory Negligence (5 States)

**Rule**: ANY negligence by plaintiff bars recovery

**States**: Alabama, Maryland, North Carolina, Virginia, Washington D.C.

**Harsh Result**: Even 1% fault = no recovery

**Exception**: Last Clear Chance doctrine (defendant had last opportunity to avoid harm)

---

### Comparative Negligence (Most States)

#### Pure Comparative Negligence (13 States)

**Rule**: Plaintiff's recovery reduced by percentage of fault

**Can Recover Even If Mostly at Fault**: Even 99% fault = 1% recovery

**States**: Alaska, Arizona, California, Florida, Kentucky, Louisiana, Mississippi, Missouri, New Mexico, New York, Rhode Island, South Dakota, Washington

---

#### Modified Comparative Negligence (33 States)

**50% Bar Rule** (12 states): Can recover if 50% or less at fault
- Arkansas, Colorado, Georgia, Idaho, Kansas, Maine, Nebraska, North Dakota, Oklahoma, Tennessee, Utah, West Virginia

**51% Bar Rule** (21 states): Can recover if less than 51% at fault
- Connecticut, Delaware, Hawaii, Illinois, Indiana, Iowa, Massachusetts, Michigan, Minnesota, Montana, Nevada, New Hampshire, New Jersey, Ohio, Oregon, Pennsylvania, South Carolina, Texas, Vermont, Wisconsin, Wyoming

---

#### Apportionment

**Jury Determines**:
1. Total damages
2. Percentage fault for each party
3. Reduce damages by plaintiff's percentage

**Example**:
```
Total damages: $100,000
Plaintiff's fault: 30%
Defendant's fault: 70%

Recovery: $70,000 (100,000 × 70%)
```

---

### Strategic Considerations

**Defendant's Burden**: Prove plaintiff's comparative negligence

**Discovery**: Look for plaintiff's conduct contributing to injury
- Failure to follow instructions
- Voluntary intoxication
- Ignoring warnings
- Unreasonable behavior

---

## Assumption of Risk

### Express Assumption of Risk

**Definition**: Plaintiff contractually agreed to assume risk (waiver)

**Examples**:
- Ski resort liability waiver
- Gym membership waiver
- Extreme sports waiver

**Enforceability**:
- ✅ Generally enforceable for negligence
- ❌ NOT enforceable for gross negligence, recklessness, intentional torts

**Public Policy Limits**:
- Some states void waivers for essential services
- Cannot waive liability for willful/wanton conduct

---

### Implied Assumption of Risk

**Definition**: Plaintiff voluntarily encountered known risk

**Elements**:
1. **Knowledge**: Plaintiff knew of risk
2. **Voluntariness**: Plaintiff voluntarily encountered risk
3. **Appreciation**: Plaintiff appreciated magnitude of risk

**Examples**:
- Attending baseball game (risk of foul ball)
- Playing contact sports (risk of injury)

---

### Primary vs. Secondary Assumption of Risk

**Primary**: Risk inherent in activity
- Complete defense (no duty to protect against inherent risks)
- Example: Getting hit by hockey puck at game

**Secondary**: Defendant negligent, but plaintiff assumed risk anyway
- Merged with comparative negligence in most states
- Reduces recovery rather than barring it

---

## Statute of Limitations

### Function as Defense

**Affirmative Defense**: Defendant must plead and prove

**Effect**: Bars claim if filed after limitations period expired

**Calculation**: From date of accrual (injury occurred or discovered)

---

### Accrual Rules

**General Rule**: Accrues when injury occurs

**Discovery Rule**: Some claims accrue when plaintiff discovers (or should have discovered) injury
- Medical malpractice (many states)
- Fraud (most states)
- **NOT** § 1983 (generally) - accrues at injury

---

### Tolling

**Minority**: Statute tolled (paused) until plaintiff reaches age 18

**Disability**: Tolled if plaintiff legally incompetent

**Fraudulent Concealment**: Defendant's fraud may toll statute

**Continuing Violation**: Some claims treated as ongoing (each day new accrual)

---

### State-Specific SOL for § 1983

**Federal Borrowing Rule**: § 1983 borrows state's personal injury statute of limitations

**Typical Periods**:
- 2 years: California, Illinois, Tennessee, Texas, Wisconsin
- 3 years: Florida, New York, Pennsylvania
- 4 years: Maine
- 6 years: Michigan (outlier)

**Check Your State**: Always verify current SOL

---

## Mitigation of Damages

### Duty to Mitigate

**Rule**: Plaintiff must take reasonable steps to minimize damages

**Not Affirmative Defense**: Failure to mitigate reduces damages, not complete bar

**Examples**:
- Seek medical treatment for injuries
- Seek comparable employment after wrongful termination
- Repair property damage to prevent further loss

**Reasonableness Standard**: What would reasonable person do?

---

### Defendant's Burden

**Prove**:
1. Plaintiff failed to mitigate
2. Damages could have been avoided
3. Amount of avoidable damages

---

### Limits

**Not Required**:
- Dangerous or risky mitigation
- Unreasonable expense
- Degrading or humiliating conduct

**Medical Treatment**: Not required to undergo surgery (generally)

---

## Collateral Source Rule

### Rule

**General**: Plaintiff's damages not reduced by compensation from collateral sources (insurance, benefits)

**Rationale**: Defendant should not benefit from plaintiff's insurance

**Examples**:
- Health insurance paid medical bills → Defendant still liable for full medical expenses
- Disability benefits compensate lost wages → Defendant still liable for lost wages

---

### State Variations

**Traditional Rule**: Collateral sources inadmissible (jury never hears about insurance)

**Modified Rules**: Some states allow:
- Evidence of collateral sources
- Reduction of damages by collateral source amounts
- Subrogation by collateral source provider

**Tort Reform**: Many states modified rule to reduce damages

---

## Justification and Privilege

### Necessity

**Public Necessity**: Defendant acted to prevent greater harm to public
- Complete defense
- Example: Firefighter breaks down door to save life

**Private Necessity**: Defendant acted to prevent greater harm to self
- Incomplete defense (must pay for actual harm, but no punitive damages)
- Example: Trespassing on property to escape danger

---

### Arrest and Detention Privileges

**Lawful Arrest**: Officer not liable for proper execution of arrest

**Requirements**:
- Valid warrant OR
- Probable cause (warrantless arrest)

**Excessive Force**: Privilege does not extend to excessive force

---

### Shopkeeper's Privilege

**Rule**: Store may detain suspected shoplifter if:
1. Reasonable suspicion of theft
2. Detention in reasonable manner
3. For reasonable time
4. On premises or immediate vicinity

**State Variations**: Check specific state statute

---

## Preemption

### Federal Preemption of State Claims

**Rule**: Federal law may preempt state law claims

**Types**:
1. **Express Preemption**: Statute explicitly preempts state law
2. **Field Preemption**: Federal law occupies entire field
3. **Conflict Preemption**: Impossible to comply with both federal and state law

**Examples**:
- Federal Aviation Act preempts state tort claims (some circuits)
- ERISA preempts state claims related to employee benefits

---

## Release and Settlement

### Valid Release

**Elements**:
1. Offer and acceptance
2. Consideration
3. Mutual intent to settle

**Effect**: Bars further claims covered by release

**Scope**: Limited to claims specifically released
- General release: All known and unknown claims
- Specific release: Only enumerated claims

---

### Joint Tortfeasors

**Release of One**:
- **Traditional Rule**: Release of one releases all
- **Modern Rule**: Release of one reduces others' liability by released party's share

**Settlement Credits**: Settling defendant gets credit for settlement amount

---

## Strategic Considerations: Overcoming Defenses

### Discovery Strategy

**Qualified Immunity**:
- Find circuit precedent with similar facts
- Develop factual disputes (video evidence crucial)
- Depose officer on knowledge of law/training

**Governmental Immunity**:
- Plead individual defendants (avoid entity immunity)
- Identify ministerial acts (not discretionary)
- Research state tort claims act exceptions

**Comparative Negligence**:
- Emphasize defendant's superior knowledge/power
- Highlight plaintiff's compliance with instructions
- Show defendant's conduct was sole cause

---

### Motion Practice

**Summary Judgment on QI**: Most critical motion
- File opposition with detailed factual record
- Attach video evidence, expert declarations
- Argue factual disputes preclude summary judgment

**Notice Requirements**: Strictly comply with governmental notice requirements
- File administrative claim timely
- Include all required information
- Preserve claim for litigation

---

## Related Resources

- **Federal Civil Rights**: See `federal-civil-rights.md` for qualified immunity deep dive
- **State Torts**: See `state-tort-law.md` for comparative negligence by state
- **Elements Checklists**: See `elements-checklists/` for affirmative defense analysis

---

**Last Updated**: 2026-01-01
**Disclaimer**: Affirmative defense law varies by jurisdiction. Always research controlling law in specific state and circuit.
