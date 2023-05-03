import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ErrorPage, LoginPage, HomePage } from "./pages";

const router = createBrowserRouter([
  {
    path: 'login',
    element: <LoginPage/>
  }
  ,
  {
    path: '/', element: <HomePage/>
  }
  ,
  {
    path: '*', element: <ErrorPage/>
  }
]);

function App() {
  return <RouterProvider router={router} ></RouterProvider>;
}

export default App;
