# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- Response to both prompts
-   - The inital UML diagram will consits of four classes: Owner, Pet, Task, and Scheduler. Each class will be responsible of holding crucial information respectively and all of them except for scheduler will have methods that will help in application. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- Response to both prompts: N/A

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- Response to both prompts
    - The scheduler considers the following constraints: Time conflicts, a task's due date, and overdue. The constraint that i believe mattered the most was the time conflict one because an issue may arise in the use of the application where an user schedulues a task at the same time as another schedulued task

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- Response to both prompts
    - A tradeoff that the scheduler makes has to do with the 15-minute conflict window. The benefit in this implementation comes from the assumption that it takes at most 15 minutes to prepare for a task. It gives employess time to prepare and avoid tasks being cramped in a time frame. Although a case may be presented where two tasks can be done back-to-back on paper, it is not realistic. In other words, i am tradding off more tasks being done for organization and for a cleanre schedule structure.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- Response to both prompts
    - I used Claude for the purposes of design, debugging, implementation, and refactorization. The prompts and questions i used that were useful in the project process were more on the side of design. I asked claude what should be in a object like Task and i was provided with useful details that would help in the application.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- Response to both prompts
    - For my case, i did not stumble at a point where i rejected an AI suggestion as-is. I think what helped was the context i provided it and what needed to be done. The way i evaulate an AI suggestion is by asking wether or not it wil make the project both efficient and directly adrressing the need. I also made sure that it did break the exisitng code implementation.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- Response to both prompts
    - I tested the basic functionality of the code like the scheduling because this is the "main point" of the application

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

- Response to both prompts
    - I am pretty confident it works. The edge case i would test and attempt to solve if i had more time would be canceling a task on a ID that does not exist.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

- I am satisfied with the overall project. I liked how we had to begin from scratch and work our way up

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

- Definetly the filter_tasks

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- I learned how to become more familiar with UML class diagram design and proeptly prompt enginerring
