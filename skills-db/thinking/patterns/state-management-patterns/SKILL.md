---
name: state-management-patterns
description: Systematically manage application state across components using patterns like centralized stores, observable state, atomic updates, and unidirectional data flow
---

# State Management Patterns

## Overview

State management patterns provide systematic approaches to handling application state - the data that changes over time and drives UI rendering. As applications grow beyond simple forms, ad-hoc state management (scattered useState hooks, prop drilling, uncontrolled mutations) becomes unmaintainable - developers lose track of what updates what, race conditions emerge, and debugging becomes archaeology. Modern state management patterns emerged from Facebook's Flux architecture (2014) in response to React's scaling challenges, evolving into Redux (2015), MobX (2015), and newer solutions like Zustand (2019) and Jotai (2020).

These patterns share core principles: predictable state updates, centralized or coordinated state storage, and clear data flow between components. The spectrum ranges from immutable centralized stores (Redux) requiring explicit actions and reducers, to reactive observable state (MobX) with automatic dependency tracking, to minimalist atomic state (Zustand, Jotai) balancing simplicity and power. The right choice depends on application complexity, team size, and performance requirements.

## When to Use

- Applications with complex state shared across multiple components
- When prop drilling becomes unwieldy (passing state through 4+ component levels)
- Forms with intricate validation and cross-field dependencies
- Real-time applications requiring state synchronization (chat, collaboration tools)
- Applications needing time-travel debugging or state persistence
- When multiple developers need clear state update conventions
- Performance-critical apps requiring selective component re-renders

## The Process

### Step 1: Identify State Domains and Scope

Categorize application state by domain (user, products, UI) and scope (global, route-specific, component-local).

**Ask:** "What state is truly global? What's local to specific features or components?"

**State Categories:**
- **Server/Remote State:** Data from APIs (user profiles, product catalogs) - consider React Query, SWR instead of state management
- **Global Client State:** Authentication status, user preferences, shopping cart - candidates for centralized store
- **Local Component State:** Form inputs, accordion open/closed, hover states - keep in component with useState
- **URL State:** Filters, pagination, search queries - store in URL params for shareability

**Example:** E-commerce app - cart items (global state), product filters (URL state), hover effects (local state), product data (server state with React Query)

### Step 2: Choose State Management Approach

Select pattern based on complexity, team preferences, and performance needs.

**Ask:** "What level of structure and predictability do I need?"

**Options:**

**Redux (Centralized Immutable Store):**
- Single store with immutable state tree
- Updates via actions dispatched to reducers
- Predictable, debuggable, boilerplate-heavy
- **Best for:** Large teams, complex state, time-travel debugging needs

**MobX (Observable Mutable State):**
- Observable state objects with automatic reactivity
- Direct mutations trigger re-renders
- Less boilerplate, less predictable
- **Best for:** Rapid development, smaller teams, complex nested state

**Zustand (Minimalist Hook-Based Store):**
- Lightweight hooks-based stores with minimal API
- Direct state updates via setter functions
- No providers, no boilerplate
- **Best for:** Medium apps, teams wanting Redux benefits without Redux complexity

**Context + useReducer (React Built-In):**
- React's native state management
- Good for moderate complexity
- **Best for:** Avoiding external dependencies, simpler apps

**Example:** Choose Redux for enterprise dashboard with undo/redo, choose Zustand for startup MVP needing speed

### Step 3: Design State Structure

Organize state shape for clarity, efficiency, and scalability.

**Ask:** "How should I structure state to minimize updates and maximize clarity?"

**Best Practices:**
- **Normalize Data:** Store entities by ID in objects, not arrays - enables O(1) lookups
  - **Bad:** `{users: [{id: 1, name: "Alice"}, {id: 2, name: "Bob"}]}`
  - **Good:** `{users: {1: {id: 1, name: "Alice"}, 2: {id: 2, name: "Bob"}}, userIds: [1, 2]}`
- **Separate Domains:** Distinct slices for user, products, cart - easier debugging and code splitting
- **Avoid Duplication:** Single source of truth - don't store same data in multiple places
- **Flat Over Nested:** Deep nesting complicates updates and re-renders

**Example:**
```javascript
{
  users: { byId: {}, allIds: [] },
  products: { byId: {}, allIds: [], filters: {} },
  cart: { itemIds: [], total: 0 },
  ui: { isLoading: false, error: null }
}
```

### Step 4: Implement Unidirectional Data Flow

Enforce predictable update pattern: Action → State Update → View Re-render.

**Ask:** "Can I trace any state change back to a single action?"

**Flow:**
1. User interaction triggers action (button click → dispatch addToCart action)
2. Action updates state (reducer/setter modifies cart state)
3. State change triggers re-render (components reading cart state update automatically)
4. Never allow reverse flow (view directly mutating state)

**Implementation (Redux):**
- Components dispatch actions: `dispatch({type: 'ADD_TO_CART', productId})`
- Reducers handle actions: `case 'ADD_TO_CART': return {...state, items: [...state.items, action.productId]}`
- Components subscribe to state: `const cart = useSelector(state => state.cart)`

**Implementation (Zustand):**
```javascript
const useStore = create((set) => ({
  items: [],
  addItem: (item) => set((state) => ({items: [...state.items, item]}))
}))
// Component: const addItem = useStore(state => state.addItem)
```

### Step 5: Optimize Re-Renders with Selective Subscriptions

Prevent unnecessary re-renders by subscribing components only to state slices they need.

**Ask:** "Does this component re-render when unrelated state changes?"

**Techniques:**
- **Selector Functions:** Subscribe to derived/filtered state, not entire store
  - Redux: `useSelector(state => state.products.byId[productId])`
  - Zustand: `const userName = useStore(state => state.users[userId].name)`
- **Memoization:** Use `useMemo` for expensive derived state calculations
- **Split Stores:** Multiple small stores instead of monolithic store (Zustand, Jotai approach)
- **Shallow Equality:** Configure selector equality checks to prevent re-renders on deep equality

**Example:** Product list component subscribes only to `products.allIds`, not entire products object - cart updates don't trigger product list re-render

### Step 6: Handle Async Operations and Side Effects

Manage async actions (API calls, timers) with middleware or built-in async support.

**Ask:** "Where do I put API calls and async logic?"

**Approaches:**

**Redux Toolkit (recommended):**
- `createAsyncThunk` for async actions - handles loading/success/error states automatically
```javascript
const fetchUser = createAsyncThunk('users/fetch', async (userId) => {
  const response = await api.getUser(userId)
  return response.data
})
```

**MobX:**
- Direct async actions in observable classes
```javascript
class UserStore {
  @observable user = null
  @observable loading = false

  @action async fetchUser(id) {
    this.loading = true
    this.user = await api.getUser(id)
    this.loading = false
  }
}
```

**Zustand:**
- Async functions in store actions
```javascript
const useStore = create((set) => ({
  user: null,
  fetchUser: async (id) => {
    const user = await api.getUser(id)
    set({user})
  }
}))
```

**Separate Concern:** Consider React Query/SWR for server state instead of putting API data in state management - they handle caching, revalidation, optimistic updates better

## Example Application

**Situation:** Building a collaborative task management app (Trello clone) where multiple users edit boards simultaneously - need real-time updates, optimistic UI, undo/redo, and offline support.

**Application of State Management Patterns:**

**Chosen Approach:** Redux Toolkit + Redux Toolkit Query (RTK Query) for server state

**State Structure:**
```javascript
{
  boards: { byId: {}, allIds: [], activeId: null },
  tasks: { byId: {}, byBoardId: {} },
  users: { byId: {}, currentUserId: null },
  ui: { selectedTaskId: null, isDragging: false },
  optimistic: { pendingActions: [] }
}
```

**Key Patterns:**

1. **Normalized State:** Tasks stored by ID - when task #42 updates via WebSocket, single O(1) update to `tasks.byId[42]` instead of searching arrays

2. **Optimistic Updates:**
   - User moves task → immediately update local state + dispatch server action
   - If server rejects → rollback using optimistic actions queue
   - Smooth UX while maintaining data integrity

3. **Real-Time Sync:**
   - WebSocket messages dispatched as actions → reducers handle remote updates
   - Conflicts resolved by timestamp - server always wins on conflict

4. **Undo/Redo:**
   - Redux DevTools provides time-travel debugging
   - Custom middleware records action history for undo stack

5. **Selective Re-Renders:**
   - TaskCard component: `useSelector(state => state.tasks.byId[taskId])` - only re-renders when specific task changes
   - BoardList component: `useSelector(state => state.boards.allIds)` - only re-renders when board list changes, not task edits

6. **Offline Support:**
   - RTK Query with offline-first configuration
   - Mutations queued when offline, replayed on reconnection

**Outcome:** 60fps drag-and-drop despite hundreds of tasks. Debugging via Redux DevTools shows exact action sequence. Optimistic updates feel instant. Real-time collaboration without UI flickering. Codebase maintainable by 6 developers with clear action conventions.

## Common Pitfalls

**Over-Centralization:** Putting all state in global store including trivial local state (button hover) - creates unnecessary complexity. **Fix:** Global for truly shared state only, useState for local.

**State Duplication:** Storing server data in state management AND React Query/SWR - causes sync issues. **Fix:** Use server state libraries for API data, state management for client-only state.

**Mutating State Directly (Redux/Zustand):** `state.items.push(item)` instead of `[...state.items, item]` - breaks immutability and re-rendering. **Fix:** Use Immer (Redux Toolkit includes) or spread operators.

**Too Many Selectors:** Creating new selector functions on every render - defeats memoization. **Fix:** Define selectors outside components or use `useCallback`.

**Prop Drilling Avoidance Obsession:** Using global state to avoid passing props 2 levels - premature optimization. **Fix:** Props are fine for 2-3 levels, global state for truly distant components.

**Ignoring Performance Tools:** Not profiling re-renders, optimizing blindly. **Fix:** Use React DevTools Profiler to identify actual bottlenecks before optimizing.

## Key Insights

**No Silver Bullet:** Redux, MobX, Zustand each excel in different contexts - Redux for predictability and debugging, MobX for rapid development, Zustand for simplicity. Evaluate based on team needs, not trends.

**Server State ≠ Client State:** Most "state management" problems are actually server state problems - React Query/SWR solve caching, revalidation, synchronization better than Redux. Use state management for client-only concerns.

**Start Simple, Grow Strategically:** Begin with Context + useReducer or Zustand, migrate to Redux when complexity demands it - don't prematurely adopt Redux boilerplate for simple apps.

**Re-Render Performance:** Most apps don't have performance issues. Profile first - 90% of "slow" apps are slow API calls or N+1 queries, not state management. Optimize selectors only when profiler shows problems.

**DevTools Matter:** Redux DevTools' time-travel debugging is a game-changer for complex state - replaying 50 actions to reproduce bug is worth the boilerplate.

**Colocation Principle:** Keep state as close to where it's used as possible - global only when actually global. Most state should be local or route-scoped.

## Related Patterns

- **Flux Architecture:** Original Facebook pattern inspiring Redux - unidirectional data flow with actions/stores
- **Observer Pattern:** Foundation of MobX and reactive state - observers subscribe to observable state changes
- **Command Pattern:** Redux actions are commands - encapsulated state change requests
- **CQRS:** Command-Query Responsibility Segregation - Redux separates reads (selectors) from writes (actions/reducers)
- **Event Sourcing:** Redux's action log is event sourcing - rebuild state by replaying actions
- **Atomic State (Recoil/Jotai):** Alternative approach - state as independent atoms instead of monolithic store
