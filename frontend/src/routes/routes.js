import axios from 'axios'
const baseURL =  'http://127.0.0.1:8000';
const predict = (newObject) => {
  return axios.post(`${baseURL}/predict`, newObject).then(res => res.data);
};

export default predict;  // export the function directly
