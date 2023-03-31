import fetch from 'node-fetch';

const response = await fetch('http://127.0.0.1:8000/chat/', {method: 'POST', body: 'a=1'});
const data = await response.json();