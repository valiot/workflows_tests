# Summary 📝

Please include a short summary of the change and which issue will be fixed.

## **Fixes** #SDLQU-
<!-- It has to include an issue so that this PR can be accepted. It can be a Jira or Linear issue. -->

## Type of change 🦺

- [ ] 💥**MAJOR CHANGE**: Fix or feature that can change the behaviour of a component or project. These changes also contain all the *breaking changes*.
- [ ] ✨**MINOR CHANGE**: Add new features or deprecate existing ones, all without breaking changes.
- [ ] 🩹**PATCH CHANGE**: Can be a refactor of an existing component, a bug fix or the improvement of a new library, optimising existing features, adding notifications or stuff like that. It's not a big requirement or an algorithm required by the client, something that doesn't require a breaking change.

<!-- If this is a critical hotfix, uncomment the below option and delete the other ones. -->
<!--
## HOT FIX
- [ ] 🚑️**HOT FIX**: It's a critical fix that needs to be reviewed ASAP. It can be to improve the CI/CD tools, repair some error in an algorithm or make any change that is urgent or critical. It'd be counted as a **PATCH CHANGE**.
-->


----------
## How has this been tested? ⚗️
How were these changes tested, and what changed?

| Automatic tests | Manual tests |
| ------------- | ------------- | 
| <ul><li>[ ] With a CI tool</li></ul> <!-- Pytest or Cypress --> | <ul><li>[ ] With an implementation </li></ul>| <!-- Here, describe each component that is needed to run the tests or check the results. -->
| <ul><li> **command_line**</li><li> (...)</li></ul> <!-- For the back-end, it's 'pytest', and for the front-end, it's 'yarn test' --> | <!-- Describe each step to test these changes manually --> <ul><li> Using *SOME_IMPLEMENTATION*</li><li> **Step**</li><li> (...)</li></ul> |

### Visual demo <!-- delete if it didn't have any visual demo to show. -->

<!-- If you have to add something visible in front, uncomment this -->
<!-- 
#### Scenario Path: [Go to XXXX page](https://localhost:3000/your_demo_page)
-->
| Before  (What happened before?) | After (What happens now?) |
| ------------- | ------------- | 
| <img width="674" alt="Screen Shot 2022-02-23 at 9 43 23" src="https://user-images.githubusercontent.com/16729556/155354025-3aab7f55-c4a5-40c4-84ea-52a7849880a6.png">  | <img width="664" alt="Screen Shot 2022-02-23 at 9 43 33" src="https://user-images.githubusercontent.com/16729556/155354011-bc8a7864-4e78-49b8-ae69-d4e47bb599d1.png"> |
| Explanation of the previous behaviour. | Explanation of the new behaviour. |

----------
## Documentation 📖 <!-- delete if it didn't have any corresponding change -->
If these changes require a documentation update, please report it on the corresponding channel of the [Valiot official handbook](https://handbook.valiot.io/en/home).


## Checklist 📋
Ensure all the below points are satisfied before opening a **Pull Request** for review. If they are not satisfied, you can always open it as **draft**. <!-- To open it as a draft, you can do it by clicking the display green button below. -->

- [ ] 💻 My code follows the [style guidelines](https://docs.google.com/presentation/d/1wD-14NLWMlQtrB4nKt2zipyquOQFbrfSksIMUNuA6nQ/edit#slide=id.g3c63aa8b17_0_133) of this project. <!-- Use 'yarn format:changed' for the front. -->
- [ ] :octocat: I have performed a self-review of my code.
- [ ] ⚠️ My code doesn't generate new warnings or alerts (deprecate code or incompatible libraries).
- [ ] 🧪 New and existing tests pass successfully. <!-- Use 'yarn test:all' for front-end and 'pytest' for back-end -->
- [ ] ✅ The checks pass successfully on my local machine.
- [ ] 💯 My code is covered by tests.
- [ ] 📓 Documentation and comments are added where needed. <!-- Use your 'docs' folder for the documentation -->

<!--
If you open your PR to review without fulfilling the checklist, it will automatically be rejected.
-->
