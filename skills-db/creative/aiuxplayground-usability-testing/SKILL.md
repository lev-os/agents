---
name: usability-testing
description: Help users conduct effective usability testing. Use when someone is planning user tests, designing prototype validation, preparing usability studies, or trying to understand why users struggle with their product.
---

# Usability Testing

Help the user conduct effective usability testing using frameworks and insights from 11 product leaders.

## How to Help

When the user asks for help with usability testing:

1. **Clarify the goal** - Determine if they're validating a concept, finding friction points, or optimizing conversion
2. **Choose the right fidelity** - Help them select between Wizard of Oz tests, fake doors, prototypes, or production testing
3. **Design the test** - Guide them on recruiting users, creating scenarios, and what to observe
4. **Plan for iteration** - Discuss how findings will flow back into the product development process

## Core Principles

### Fake it before you build it
Itamar Gilad: "Initially you fake it - fake door test, smoke test, Wizard of Oz tests. We showed the tabbed inbox working to people, but it wasn't really Gmail, it was just a facade." Validate core value propositions before writing production code using faked versions where humans perform the automated task behind the scenes.

### Small samples reveal big friction
Melanie Perkins: "It's amazing how you can find 10 random people on the internet and they can give such astute feedback that's so representative for such a large number of people." Run tests with as few as 10 random people to identify core product issues.

### Watch users, don't just ask them
Uri Levine: "Simply watch users and see what they're doing. If they're not doing what you expect, then ask them why." Direct observation reveals behaviors and needs that surveys miss. Ask 'why' when users deviate from the expected path.

### Test multiple options, not one
Kristen Berman: "We never do a UX study where we're just showing people one thing. We always present multiple options and relatively look for which one drives the intended behavior." Single-design testing is ineffective for predicting behavior.

### Overcome creator bias
Guillermo Rauch: "You tend to overrate how well your products work. It's very important to give your product to another person and watch them interact with it." Directly observing users helps overcome the tendency to think your product is more intuitive than it is.

### Micro-level testing drives millions
Judd Antin: "We changed seven characters and made Airbnb millions of dollars because we found out the button felt scary." Don't dismiss usability testing as junior work; finding scary or confusing CTAs can massively impact conversion.

### Progress through testing stages
Itamar Gilad: "Mid-level tests are about building a rough version - early adopter programs, alphas, longitudinal user studies, and fish food (testing on your own team)." Use a progression from fish fooding to dogfooding to alphas to increase confidence iteratively.

### Make testing a team sport
Noah Weiss: "We had PMs, engineers, designers, and the user researcher all in one Slack thread live, responding and reacting to the usability session." Increase engagement by having cross-functional teams live-react to sessions in shared chat threads.

## Questions to Help Users

- "What specific behavior are you trying to observe or validate?"
- "Do you need to validate the concept (use fake doors) or optimize the execution (use the real product)?"
- "How will you recruit users who have 'zero skin in the game' for honest feedback?"
- "Are you testing one option or multiple options to compare?"
- "What will you do with the findings - how will they flow back into development?"
- "Who else on the team should observe these sessions?"

## Common Mistakes to Flag

- **Testing only one design** - Present multiple options to measure relative performance
- **Building before validating** - Use Wizard of Oz or fake door tests before writing production code
- **Relying on internal intuition** - Employees are too familiar with the product to spot real user friction
- **Ignoring micro-level issues** - Small copy changes and button labels can have massive business impact
- **Testing in isolation** - Bring engineers and designers into sessions to build shared understanding

## Deep Dive

For all 14 insights from 11 guests, see `references/guest-insights.md`

## Related Skills

- Customer Research
- Writing PRDs
- Shipping Products
- Designing Growth Loops


---

# Guest Insights


# Usability Testing - All Guest Insights

*11 guests, 14 mentions*

---

## Amjad Masad
*Amjad Masad*

> "We've seen product managers build, like I said, like a v1 of an app and actually go out and test it with users. I can't name the company, but there's a public company that have used Replit to test a v1 of an app. And obviously after that sort of works, they take it to the engineers and they're like, 'Okay, we built this thing. We think it's a great thing. We test it with some users.'"

**Insight:** AI tools allow PMs to bypass engineering bottlenecks to create functional prototypes for real-world user testing.

**Tactical advice:**
- Build a functional v1 independently to validate ideas with users before putting them on the official engineering roadmap.

*Timestamp: 00:26:35*


## Bob Baxley
*Bob Baxley*

> "Go observe people going through self-checkout at Target... then go watch it at some other grocery store where it's not as great and really notice what happens with people... Just go watch somebody over 70 fumble with a chip card insert or watch somebody try to figure out Apple Pay."

**Insight:** Developing product intuition requires observing humans interacting with technology in the wild, outside of controlled lab environments.

**Tactical advice:**
- Conduct 'reality checks' by watching users interact with competitor products to see their unbiased behavior and needs.

*Timestamp: 00:50:11*


## Grant Lee
*Grant Lee*

> "We would have an idea in the morning, come up with some sort of functional prototype, recruit a bunch of people that are legitimately good prospective users, but have zero skin in the game, ship fast so people can start playing with it. In the afternoon, we're already running pretty full scale experiment. You start actually hearing other people describe their usage of the product. We can also watch them struggle. By the evening or by the next day. We can actually go through all of it together and say, okay, we're going back and we have to fix this."

**Insight:** Use rapid prototyping and unbiased user testing to identify friction points within a single day.

**Tactical advice:**
- Recruit prospective users with 'zero skin in the game' to ensure honest feedback.
- Watch users struggle and listen to them describe their thought process in real-time.
- Use platforms like Voicepanel or UserTesting to automate and scale the recruitment process.

*Timestamp: 00:01:08*


## Guillermo Rauch
*Guillermo Rauch*

> "Another aspect of exposure hours is that you tend to overrate how well your products work. It's very important to give your product to another person and watch them interact with it, expose yourself to the pain of reality. And the more you submerge yourself in the real deal, nitty-gritty of what happens when people use your interfaces and whatnot, I think you you'll come out stronger."

**Insight:** Directly observing users helps overcome the 'creator bias' where builders overrate the quality and ease of their own products.

**Tactical advice:**
- Invite customers to demo how they use the product live to the executive team or the whole company.
- Watch for 'pain points' or non-intuitive behaviors that aren't captured in automated metrics.

*Timestamp: 01:11:05*


## Itamar Gilad
*Itamar Gilad*

> "Initially you fake it, you do a fake door test, you do a smoke test, Wizard of Oz tests. We used a lot of those in the tabbed inbox by the way, one of the first early versions was actually we showed the tabbed inbox working to people. But it wasn't really Gmail, it was just a facade of HTML and behind the scenes... some of us moved just the subject and the sender into the right place."

**Insight:** Use 'faked' versions of a product (Wizard of Oz or smoke tests) to validate the core value proposition before writing production code.

**Tactical advice:**
- Run 'Wizard of Oz' tests where humans manually perform the automated task behind a facade
- Use 'Fake Door' tests to measure user intent and click-through rates on non-existent features

*Timestamp: 00:52:18*

---

> "Initially you fake it, mid-level tests are about building a rough version of it... those are early adopter programs, alphas, longitudinal user studies and fish food. Fish food is testing on your own team."

**Insight:** Utilize a progression of testing. From 'fish fooding' (team testing) to 'dogfooding' (company testing) to alphas, to increase confidence iteratively.

**Tactical advice:**
- Implement 'Fish Fooding' to catch immediate bugs and UX flaws within the core team
- Run longitudinal studies to see how user behavior changes over time before a full launch

*Timestamp: 00:53:21*


## Judd Antin
*Judd Antin*

> "The micro level, there's so much business value to be derived there... We changed the text on the button with help from our amazing content design... We basically changed seven characters and made Airbnb millions of dollars, because what we found out was really simple. It was just like, 'Hey, this button feels scary.'"

**Insight:** Micro-level evaluative research and usability testing can drive massive business value through small, tactical optimizations.

**Tactical advice:**
- Don't dismiss usability testing as 'junior' work; it is high-leverage for business metrics.
- Look for 'scary' or confusing CTAs that might be blocking the conversion funnel.

*Timestamp: 00:35:58*

---

> "Doing product walkthroughs to identify lists of potential issues is a great thing to do. Prioritizing that list, figuring out which ones are more or less a problem, and for whom is an area where you should be extremely wary of relying on your own opinion... Some things with a product... you need a pulse to recognize."

**Insight:** While dogfooding is useful for identifying potential issues, external user testing is required to prioritize them accurately because employees are not like the users.

**Tactical advice:**
- Use dogfooding to create a list of potential issues, but use research to prioritize them.
- Acknowledge that your internal intuition is biased by your knowledge of the product.

*Timestamp: 01:07:57*


## Kristen Berman
*Kristen Berman*

> "We never do a UX study where we're just showing people one thing because they could really like it or hate it, but they could really like or hate all the designs. We have no idea. So, when we're doing this, we always present multiple options, and then relatively look for which one is going to drive the behavior we're intending to change."

**Insight:** Testing a single design is ineffective for predicting behavior; you must present multiple options to measure relative performance.

**Tactical advice:**
- Always present multiple design variations in user tests to compare which one best drives the target behavior.

*Timestamp: 34:44*


## Melanie Perkins
*Melanie Perkins*

> "It's amazing to me how you can find 10 random people on the internet and they can give such astute feedback that then is so representative for such a large number of people."

**Insight:** Small-scale, frequent usability testing with random participants is highly representative of broader user friction.

**Tactical advice:**
- Run tests with as few as 10 random people to identify core product issues
- Use online platforms like UserTesting.com to get frank, unbiased feedback from users in their own environment

*Timestamp: 00:39:40*


## Noah Weiss
*Noah Weiss*

> "What we wound up doing, especially in the pandemic when we first went remote, is now you can dial into usability sessions and to make it really attractive for the team, what we would do is have people live in a thread, write their real time thoughts... Then you wind up having the PMs, the engineers, designers and the user researcher all in one Slack thread live, responding, reacting to usability session."

**Insight:** Increase team engagement with user research by having cross-functional teams live-react to usability sessions in a shared chat thread.

**Tactical advice:**
- Create a dedicated Slack thread for each live usability session.
- Encourage engineers and designers to share real-time observations and pain points during the session.

*Timestamp: 00:43:21*


## Upasna Gautam
*Upasna Gautam*

> "I had a big working session planned with my users to do research with them, or do user testing, and breaking news breaks, and it takes so much time and effort to gather a team of editors across the globe to do a user testing session. And when breaking news happens, they have to prioritize that over everything."

**Insight:** User testing in a high-pressure environment like news requires extreme flexibility as users will always prioritize breaking events over research sessions.

**Tactical advice:**
- Build in buffers and backups for research sessions involving busy stakeholders
- Be prepared to pivot or reschedule at a moment's notice

*Timestamp: 00:00:00*

---

> "We create a script and do a simulation of a breaking news scenario to stress test our platform, because all breaking news scenarios are definitely not the same either. This gives us a lot of great feedback in that short amount of time at the speed of breaking news."

**Insight:** Simulated 'dress rehearsals' are an effective way to test product performance and user workflows under high-stress, time-sensitive conditions.

**Tactical advice:**
- Script realistic scenarios for users to play out in the product
- Have engineers and support teams observe the simulation in real-time to identify friction points

*Timestamp: 13:44*


## Uri Levine
*Uri Levine*

> "Watch new users. Simply watch users and see what they're doing. And number two, if they're not doing what you expect them to do, then ask them why, because this why is the one that is going to make your product successful."

**Insight:** Direct observation of users reveals behaviors and needs that founders often miss because they aren't 'early majority' users.

**Tactical advice:**
- Observe users without intervening to see how they actually use the product.
- Ask 'why' when a user deviates from the expected path.

*Timestamp: 01:07:42*


