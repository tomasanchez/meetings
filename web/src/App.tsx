import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ErrorPage, LoginPage, HomePage } from "./pages";
import { EventDetails } from "./pages/EventDetail/EventDetails";
import { ProtectedRoute } from "./components/Guards/ProtectedRoute";

const router = createBrowserRouter([
  {
    path: "login",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: <HomePage />,
    children: [
      {
        path: "/:id",
        element: (
          <ProtectedRoute>
            <EventDetails />
          </ProtectedRoute>
        ),
      },
    ],
  },
  {
    path: "*",
    element: <ErrorPage />,
  },
]);

function App() {
  return <RouterProvider router={router}></RouterProvider>;
}

export default App;
