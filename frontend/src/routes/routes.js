import axios from 'axios'
const baseURL =  'https://sales-forecasting-web-app.onrender.com';
const predict = (newObject) => {
  return axios.post(`${baseURL}/predict`, newObject).then(res => res.data);
};

export default predict;  // export the function directly
