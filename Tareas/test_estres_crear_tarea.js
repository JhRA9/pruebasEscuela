import http from 'k6/http';
import { sleep, check } from 'k6';

export let options = {
  stages: [
    { duration: '1m', target: 100 },  
    { duration: '1m', target: 200 },   
    { duration: '1m', target: 400 },  
    { duration: '1m', target: 600 },  
    { duration: '1m', target: 800 },   
    { duration: '2m', target: 800 },   
  ],
  thresholds: {
    'http_req_failed': ['rate<0.05'],  
  },
};

export default function () {
  const url = 'http://localhost/proyectoEscuela/create.php';
  const payload = JSON.stringify({
    titulo: `Tarea Stress ${Math.random()}`,
    descripcion: 'Prueba de estrés',
    fecha_entrega: '2025-08-01',
    hora_entrega: '23:59:00',
    estado: 'Pendiente',
    id_materia: 3,
  });
  const params = { headers: { 'Content-Type': 'application/json' } };

  let res = http.post(url, payload, params);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'success true': (r) => r.json().success === true,
  });

  sleep(1);
}
