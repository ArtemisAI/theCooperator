# Data Model Guidance: The Cooperator

This document outlines the proposed data model for "The Cooperator" application, focusing on Units, Members, Committees, and Tasks. It serves as a guide for development and will be updated as the project evolves.

## 1. Core Entities and Relationships

The primary entities are:

*   **Unit:** Represents a physical housing unit within the cooperative.
*   **Member:** Represents an individual residing in a unit and/or participating in the cooperative's activities.
*   **Committee:** Represents a formal group of members established for specific functions.
*   **CommitteeMemberRole:** An association entity defining a member's role within a specific committee.
*   **Task:** Represents a piece of work or responsibility that can be assigned and tracked.

## 2. Entity Definitions

### 2.1. Unit

*   **Purpose:** Manages information about each housing unit.
*   **Attributes:**
    *   `id` (UUID, Primary Key): Unique identifier for the unit.
    *   `unit_number` (String, Unique, Not Nullable): The official number or identifier for the unit (e.g., "Apartment 101", "House 5B").
    *   `status` (Enum, Not Nullable, Default: "active"): Current status of the unit.
        *   Values: `"active"`, `"vacant"`, `"under_maintenance"`
    *   `created_at` (DateTime, Not Nullable, Auto-generated): Timestamp of creation.
    *   `updated_at` (DateTime, Nullable, Auto-generated on update): Timestamp of last update.
*   **Relationships:**
    *   `members` (One-to-Many with Member): A unit can have multiple members. Each member belongs to one unit.

### 2.2. Member

*   **Purpose:** Stores information about individuals associated with the cooperative. This model replaces the initial generic `User` model for data directly related to cooperative membership and unit residency. A separate `SystemUser` or `Account` model might be introduced later for application login/authentication if needed.
*   **Constraints:**
    *   Each `Unit` (unless marked as "vacant") should have at least one `Member` with `member_type` = "primary".
*   **Attributes:**
    *   `id` (UUID, Primary Key): Unique identifier for the member.
    *   `first_name` (String, Not Nullable): Member's first name.
    *   `last_name` (String, Not Nullable): Member's last name.
    *   `dob` (Date, Nullable): Date of Birth. Used to calculate age.
    *   `email` (String, Unique, Not Nullable): Member's email address.
    *   `phone_number` (String, Nullable): Member's phone number.
    *   `occupation` (String, Nullable): Member's occupation.
    *   `sex` (Enum, Nullable): Member's sex/gender.
        *   Values: `"male"`, `"female"`, `"other"`, `"prefer_not_to_say"`
    *   `skills` (JSON/Array of Strings, Nullable): List of skills the member possesses (e.g., `["plumbing", "gardening", "accounting"]`).
    *   `education_level` (String, Nullable): Highest level of education completed.
    *   `member_type` (Enum, Not Nullable): Defines the member's status within their unit.
        *   Values: `"primary"`, `"secondary"`
    *   `unit_id` (UUID, ForeignKey to Unit.id, Nullable): The unit this member is associated with. Nullable if a member can exist before being assigned to a unit.
    *   `created_at` (DateTime, Not Nullable, Auto-generated): Timestamp of creation.
    *   `updated_at` (DateTime, Nullable, Auto-generated on update): Timestamp of last update.
*   **Relationships:**
    *   `unit` (Many-to-One with Unit): The unit this member resides in or is associated with.
    *   `committee_assignments` (One-to-Many with CommitteeMemberRole): Roles held by the member in various committees.
    *   `created_tasks` (One-to-Many with Task): Tasks created by this member.
    *   `assigned_tasks` (One-to-Many with Task): Tasks assigned to this member.

### 2.3. Committee

*   **Purpose:** Organizes members into groups for specific governance or operational functions.
*   **Attributes:**
    *   `id` (UUID, Primary Key): Unique identifier for the committee.
    *   `name` (String, Unique, Not Nullable): Official name of the committee (e.g., "Finance Committee", "Maintenance Committee").
    *   `description` (Text, Nullable): A brief description of the committee's purpose and responsibilities.
    *   `created_at` (DateTime, Not Nullable, Auto-generated): Timestamp of creation.
    *   `updated_at` (DateTime, Nullable, Auto-generated on update): Timestamp of last update.
*   **Relationships:**
    *   `member_roles` (One-to-Many with CommitteeMemberRole): The members and their roles within this committee.

### 2.4. CommitteeMemberRole (Association Table)

*   **Purpose:** Defines the specific role a member plays within a committee. Facilitates a many-to-many relationship between Member and Committee, with an added role attribute.
*   **Attributes:**
    *   `id` (UUID, Primary Key): Unique identifier for the role assignment.
    *   `member_id` (UUID, ForeignKey to Member.id, Not Nullable): The member assigned.
    *   `committee_id` (UUID, ForeignKey to Committee.id, Not Nullable): The committee involved.
    *   `role` (Enum, Not Nullable): The function or title of the member within the committee.
        *   Values: `"leader"`, `"secretary"`, `"treasurer"`, `"member"`, `"coordinator"` (extensible)
    *   `start_date` (Date, Nullable): Date when the member assumed this role.
    *   `end_date` (Date, Nullable): Date when the member ceased this role.
    *   `created_at` (DateTime, Not Nullable, Auto-generated): Timestamp of creation.
    *   `updated_at` (DateTime, Nullable, Auto-generated on update): Timestamp of last update.
*   **Relationships:**
    *   `member` (Many-to-One with Member): The member.
    *   `committee` (Many-to-One with Committee): The committee.

### 2.5. Task

*   **Purpose:** Tracks tasks, responsibilities, or projects within the cooperative.
*   **Attributes:**
    *   `id` (UUID, Primary Key): Unique identifier for the task.
    *   `title` (String, Not Nullable): A brief title for the task.
    *   `description` (Text, Nullable): Detailed description of the task.
    *   `status` (Enum, Not Nullable, Default: "open"): Current status of the task.
        *   Values: `"open"`, `"in_progress"`, `"assigned"`, `"completed"`, `"cancelled"`, `"on_hold"`
    *   `priority` (Enum, Nullable, Default: "medium"): Priority of the task.
        *   Values: `"low"`, `"medium"`, `"high"`, `"urgent"`
    *   `created_by_member_id` (UUID, ForeignKey to Member.id, Nullable): The member who created or posted the task.
    *   `assigned_to_member_id` (UUID, ForeignKey to Member.id, Nullable): The member to whom the task is currently assigned.
    *   `committee_id` (UUID, ForeignKey to Committee.id, Nullable): If the task is associated with a specific committee.
    *   `due_date` (DateTime, Nullable): Deadline for task completion.
    *   `budget_allocated` (Float, Nullable): Any budget allocated for this task.
    *   `budget_spent` (Float, Nullable): Actual amount spent on this task.
    *   `created_at` (DateTime, Not Nullable, Auto-generated): Timestamp of creation.
    *   `updated_at` (DateTime, Nullable, Auto-generated on update): Timestamp of last update.
*   **Relationships:**
    *   `creator` (Many-to-One with Member): The member who created the task.
    *   `assignee` (Many-to-One with Member): The member assigned to the task.
    *   `committee` (Many-to-One with Committee): The committee associated with the task.
    *   `votes` (One-to-Many, if tasks can be voted on - to be detailed in Voting module).
    *   `comments` (One-to-Many, for task discussions - consider a separate Comment entity).

## 3. Future Development Steps (Backend)

Based on this data model, the following backend development steps are envisioned:

1.  **Implement Model Changes:**
    *   Update `unit.py` and `user.py` (rename to `member.py`).
    *   Create `committee.py` and `task.py` for the new models.
    *   Establish all defined relationships (SQLAlchemy `relationship()` attributes).
2.  **Update/Create Pydantic Schemas:**
    *   Align schemas in `schemas/unit.py` and `schemas/user.py` (rename to `member.py`) with model changes.
    *   Create `schemas/committee.py` and `schemas/task.py`.
    *   Ensure schemas handle relational data appropriately (e.g., nested schemas for reads, IDs for creates/updates).
3.  **Update/Create CRUD Operations:**
    *   Modify existing CRUD logic for units and members.
    *   Implement new CRUD functions for committees, committee member roles, and tasks.
4.  **Update/Create API Endpoints:**
    *   Adjust existing API endpoints for units and members.
    *   Develop new API endpoints for committees and tasks, including managing memberships and assignments.
5.  **Database Migrations:**
    *   Generate and apply Alembic migrations to update the database schema. This will include table creation, column additions/modifications, and table renames (e.g., `users` to `members`).
6.  **Business Logic Implementation:**
    *   Implement validation logic (e.g., at least one primary member per active unit).
    *   Develop services for more complex operations if needed.
7.  **Testing:**
    *   Update existing tests for units and members.
    *   Write new unit and integration tests for committees and tasks.
8.  **Authentication & Authorization (Potentially Separate):**
    *   If application access control is needed beyond member data, develop a separate `SystemUser` model and associated auth mechanisms (JWT, etc.). This current data model focuses on the cooperative's internal structure.

## 4. Frontend Considerations (High-Level)

*   **Unit Management:** Update UI to reflect new Unit fields (status, unit number) and display associated members.
*   **Member Management:**
    *   Rename "Users" sections to "Members".
    *   Update forms and displays to include all new Member fields (DoB, occupation, sex, skills, etc.).
    *   Implement logic for assigning members to units and setting primary/secondary status.
*   **Committee Management:**
    *   New UI sections for creating committees, viewing committees, and managing committee memberships (adding/removing members, assigning roles).
*   **Task Management:**
    *   New UI sections for creating tasks, viewing tasks (e.g., Kanban, list), assigning tasks, and updating task status, deadlines, budget.
*   **API Integration:** Update frontend API services to interact with the modified and new backend endpoints.

This document provides the initial framework. Further details and refinements will be added as development progresses on each module.
