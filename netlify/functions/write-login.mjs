/* Sign-in for the writers' desk. Its own function so that it can be rate
   limited without also throttling photograph uploads. */

import { Fail, body, guard, json, login } from '../lib/write.mjs';

export default (req) => guard(async () => {
  if (req.method !== 'POST') throw new Fail(405, 'bad_request', 'POST only');
  const { username, password } = await body(req);
  try {
    return json(login(username, password));
  } catch (e) {
    // A wrong guess costs the caller a moment, on top of the rate limit.
    if (e.code === 'bad_login') await new Promise((r) => setTimeout(r, 600));
    throw e;
  }
});

export const config = {
  path: '/api/write/login',
  rateLimit: { windowLimit: 12, windowSize: 60, aggregateBy: ['ip', 'domain'] },
};
