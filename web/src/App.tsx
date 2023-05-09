import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ErrorPage, LoginPage, HomePage } from "./pages";
import { EventDetails } from "./pages/EventDetail/EventDetails";

const router = createBrowserRouter([
  {
    path: 'login',
    element: <LoginPage/>
  }
  ,
  {
    path: '/', element: <HomePage/>,
    children: [
      {
        path: "/:id",
        element: <EventDetails />,
      },
    ],
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
