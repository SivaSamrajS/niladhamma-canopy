/* The writers' desk: list, read, publish and withdraw member posts. Every
   route needs a session from /api/write/login. */

import {
  Fail, body, getPost, guard, json, listPosts, publish, remove, requireSession, storeImage,
} from '../lib/write.mjs';

export default (req) => guard(async () => {
  requireSession(req);
  const url = new URL(req.url);
  const route = `${req.method} ${url.pathname.replace(/\/+$/, '')}`;
  switch (route) {
    case 'GET /api/write/posts':
      return json({ posts: await listPosts() });
    case 'GET /api/write/post':
      return json({ post: await getPost(url.searchParams.get('slug') || '') });
    case 'POST /api/write/image':
      return json(await storeImage(await body(req)));
    case 'POST /api/write/publish':
      return json(await publish(await body(req)));
    case 'POST /api/write/delete':
      return json(await remove((await body(req)).slug));
    default:
      throw new Fail(404, 'bad_request', 'No such route');
  }
});

export const config = {
  path: ['/api/write/posts', '/api/write/post', '/api/write/image',
    '/api/write/publish', '/api/write/delete'],
};
