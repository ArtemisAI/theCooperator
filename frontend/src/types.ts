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
