import axios from 'axios';

const api=axios.create({
  baseURL:import.meta.env.VITE_API_URL||'http://127.0.0.1:8000',
  headers:{'Content-Type':'application/json'},
  withCredentials:true
});
let refreshing=null;

api.interceptors.request.use(config=>{
  const token=sessionStorage.getItem('voxminds_access_token');
  if(token) config.headers.Authorization=`Bearer ${token}`;
  return config;
});

api.interceptors.response.use(r=>r,async error=>{
  const original=error.config;
  const isAuthRoute=original?.url?.includes('/api/auth/');
  if(error.response?.status===401 && !original?._retry && !isAuthRoute){
    original._retry=true;
    try{
      refreshing=refreshing||api.post('/api/auth/refresh').finally(()=>{refreshing=null});
      const r=await refreshing;
      sessionStorage.setItem('voxminds_access_token',r.data.access_token);
      sessionStorage.setItem('voxminds_user',JSON.stringify(r.data.user));
      original.headers.Authorization=`Bearer ${r.data.access_token}`;
      return api(original);
    }catch(e){
      sessionStorage.clear();
      window.location.href='/';
    }
  }
  return Promise.reject(error);
});
export default api;
