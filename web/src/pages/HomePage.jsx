import React from "react";
import { Header } from "../components/Layout/Header";
import { Events } from "../components/Events/Events";


export const HomePage = () => {
  return (
    <>
      <Header />
      <main>
        <Events/>
      </main>
    </>
  );
};
