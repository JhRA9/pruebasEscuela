import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
  stages: [
    { duration: '1m', target: 200 } 
    { duration: '1m', target: 400 }
    { duration: '1m', target: 600 } 
    { duration: '1m', target: 1000 }
    { duration: '2m', target: 1000 }
  ],
  thresholds: {
    'http_req_failed': ['rate<0.05'], 
  },
};

export default function () {
  const url = 'http://localhost/proyectoEscuela/login/index.php';
  const payload = JSON.stringify({ email: 'admin@admin.com', password: '123' });
  const params = { headers: { 'Content-Type': 'application/json' } };
  let res = http.post(url, payload, params);

  check(res, {
(r) => r.status === 200,
  });

  sleep(1);
}

