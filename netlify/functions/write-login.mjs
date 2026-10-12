/* Sign-in for the writers' desk. Kept apart from the rest so that a rate
   limit can be put on it without also throttling photograph uploads. */

import { Fail, body, guard, json, login } from '../lib/write.mjs';

export default (req) => guard(async () => {
  if (req.method !== 'POST') throw new Fail(405, 'bad_request', 'POST only');
  const { username, password } = await body(req);
  try {
    return json(login(username, password));
  } catch (e) {
    // A wrong guess costs the caller a moment.
    if (e.code === 'bad_login') await new Promise((r) => setTimeout(r, 600));
    throw e;
  }
});

export const config = { path: '/api/write/login' };
