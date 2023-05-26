import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { SWRConfig } from 'swr/_internal'
import Swal from "sweetalert2";

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <SWRConfig value={{
      onError: (error) => {
        if(error.status !== 403 && error.status !== 404) {
          console.log(error)
          Swal.fire({
            title: 'Error',
            text: error.message,
            icon: 'error',
            confirmButtonText: 'OK'
          });
        }
      }
    }}>
      <App />
    </SWRConfig>
  </React.StrictMode>,
)
