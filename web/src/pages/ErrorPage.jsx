import React from 'react'
import { Link } from 'react-router-dom'

export const ErrorPage = () => {
  return (
    <>
    <h1>Ups. Surgió un error.</h1>
    <h2>En construcción...</h2>
    <Link className='btn bg-danger ' to={'/'}>Ir al home</Link>
    </>
  )
}
