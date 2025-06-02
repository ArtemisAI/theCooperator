// ---------------------------------------------------------------------------
// Ad-hoc TypeScript interfaces mirroring backend *User* schema.
// Will be auto-generated from OpenAPI once codegen pipeline is configured.
// ---------------------------------------------------------------------------

export interface UserRead {
  id: string;
  email: string;
  full_name?: string | null;
  role: "resident" | "admin" | "observer";
}

export interface UserCreate {
  email: string;
  password: string;
  full_name?: string | null;
  role?: "resident" | "admin" | "observer";
}

// ---------------------------------------------------------------------------
// TypeScript interfaces mirroring backend *Task* schema.
// ---------------------------------------------------------------------------

export type TaskStatus = "todo" | "in_progress" | "done"; // Matches backend Enum

export interface Task {
  id: string;
  title: string;
  description?: string | null;
  status: TaskStatus;
  assignee_id?: string | null;
  due_date?: string | null; // Assuming ISO date string for due_date
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface TaskCreate {
  title: string;
  description?: string | null;
  status?: TaskStatus;
  assignee_id?: string | null;
  due_date?: string | null;
}

// ---------------------------------------------------------------------------
// TypeScript interfaces mirroring backend *Unit* schema.
// ---------------------------------------------------------------------------

export interface Unit {
  id: string;
  name: string;
  address: string;
  description?: string | null;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
  // Add other relevant fields if returned by API (e.g., manager_id)
}

export interface UnitCreate {
  name: string;
  address: string;
  description?: string | null;
}

export interface UnitUpdate {
  name?: string;
  address?: string;
  description?: string | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  status?: TaskStatus;
  assignee_id?: string | null; // Important for assignment/unassignment
  due_date?: string | null;
}
