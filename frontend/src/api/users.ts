// ----------------------------------------------------------------------------
// Type-safe React hooks for `/api/v1/users` endpoints (auto-generated later).
// ----------------------------------------------------------------------------

// TODO:
// 1. Once the backend OpenAPI schema is exposed, feed it into *openapi-typescript*
//    + *react-query* codegen to create fully-typed hooks.
// 2. Replace the temporary fetch helpers below.

import { UserRead, UserCreate } from "../types"; // will be generated later

export async function listUsers(): Promise<UserRead[]> {
  const res = await fetch("/api/v1/users");
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

export async function createUser(payload: UserCreate): Promise<UserRead> {
  const res = await fetch("/api/v1/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create user");
  return res.json();
}
