// ---------------------------------------------------------------------------
// Members page – minimal list/create UI (placeholder).
// ---------------------------------------------------------------------------

import { useEffect, useState } from "react";

import { listUsers, createUser } from "../api/users";

// TODO: replace with Material-UI DataGrid once design system is plugged in.

export default function MembersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [email, setEmail] = useState("");

  useEffect(() => {
    listUsers().then(setUsers).catch(console.error);
  }, []);

  async function handleAdd() {
    const newUser = await createUser({ email, password: "secret" } as any);
    setUsers([...users, newUser]);
    setEmail("");
  }

  return (
    <div>
      <h1>Members</h1>

      <div>
        <input
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button onClick={handleAdd}>Add</button>
      </div>

      <ul>
        {users.map((u) => (
          <li key={u.id}>{u.email}</li>
        ))}
      </ul>
    </div>
  );
}
