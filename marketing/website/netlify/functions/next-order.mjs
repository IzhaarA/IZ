// Hands out sequential order numbers: MWO-0001, MWO-0002, ...
// POST -> takes the next number. GET -> shows the last number used (does not take one).
import { getStore } from "@netlify/blobs";

const fmt = (n) => "MWO-" + String(n).padStart(4, "0");
// MWO-0001 to MWO-0004 were placed before the counter existed, so it starts at 0005
const ALREADY_USED = 4;

export default async (req) => {
  const store = getStore({ name: "order-numbers", consistency: "strong" });
  if (req.method === "GET") {
    const cur = await store.get("counter", { type: "json" });
    return Response.json({ last: fmt(cur ? cur.n : ALREADY_USED) });
  }
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  for (let attempt = 0; attempt < 10; attempt++) {
    const cur = await store.getWithMetadata("counter", { type: "json" });
    const n = (cur && cur.data ? cur.data.n : ALREADY_USED) + 1;
    const res = await store.setJSON("counter", { n }, cur ? { onlyIfMatch: cur.etag } : { onlyIfNew: true });
    if (res.modified) return Response.json({ no: fmt(n) });
  }
  return new Response("Busy, try again", { status: 503 });
};

export const config = { path: "/api/next-order" };
